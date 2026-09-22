#!/usr/bin/env python3
import asyncio
import os
import pty
import sys
import struct
import fcntl
import termios
import websockets

async def terminal_handler(websocket):
    master_fd, slave_fd = pty.openpty()
    
    # Размер терминала 80x24
    buf = struct.pack('HHHH', 24, 80, 0, 0)
    fcntl.ioctl(master_fd, termios.TIOCSWINSZ, buf)

    # Делаем master_fd неблокирующим для корректной работы с asyncio
    os.set_blocking(master_fd, False)

    proc = await asyncio.create_subprocess_exec(
        sys.executable, '/app/index.py',
        stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
        close_fds=True
    )
    os.close(slave_fd)

    loop = asyncio.get_running_loop()
    
    # Создаем асинхронный reader для pty-дескриптора вместо os.read
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader, loop=loop)
    await loop.connect_read_pipe(lambda: protocol, os.fdopen(master_fd, 'rb'))

    # Поток 1: Чтение вывода скрипта -> отправка в браузер через WebSocket
    async def pipe_output():
        try:
            while proc.returncode is None:
                # Асинхронное неблокирующее чтение
                data = await reader.read(4096)
                if not data:
                    break
                
                # Декодируем входящие байты терминала
                text = data.decode('utf-8', errors='ignore')
                
                # Перехватываем управляющие коды очистки экрана \x1b[H, \x1b[2J, \x1b[3J
                if "\x1b[H" in text or "\x1b[2J" in text or "\x1b[3J" in text:
                    # Посылаем маркер очистки экрана, а системные коды вырезаем
                    await websocket.send("[CMD_CLEAR]")
                    text = text.replace("\x1b[H", "").replace("\x1b[2J", "").replace("\x1b[3J", "")
                
                if text:
                    await websocket.send(text)
        except Exception:
            pass
        finally:
            try:
                await websocket.close()
            except Exception:
                pass

    # Поток 2: Прием клавиш из браузера -> запись в скрипт
    async def pipe_input():
        try:
            async for message in websocket:
                if proc.returncode is not None:
                    break
                # os.write на неблокирующем дескрипторе может вернуть ошибку, 
                # но для ввода небольших порций текста с клавиатуры это допустимо.
                os.write(master_fd, message.encode('utf-8'))
        except Exception:
            pass

    # Поток 1: Чтение вывода скрипта -> отправка в браузер через WebSocket
    output_task = asyncio.create_task(pipe_output())
    # Поток 2: Прием клавиш из браузера -> запись в скрипт
    input_task = asyncio.create_task(pipe_input())
    # Поток 3: Явное ожидание завершения самого процесса (исправлено!)
    proc_task = asyncio.create_task(proc.wait())

    # Теперь передаем только объекты Task, что полностью легально
    done, pending = await asyncio.wait(
        [output_task, input_task, proc_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Отменяем оставшиеся задачи
    for task in pending:
        task.cancel()
    
    # Гарантированно завершаем процесс и освобождаем ресурсы
    if proc.returncode is None:
        try:
            proc.kill()
            # Ждем завершения убитого процесса, чтобы избежать зомби-процессов
            await proc.wait() 
        except ProcessLookupError:
            pass
            
    try:
        os.close(master_fd)
    except OSError:
        pass

async def main():
    async with websockets.serve(terminal_handler, "0.0.0.0", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
