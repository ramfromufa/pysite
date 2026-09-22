FROM python:3.11-slim

# Настройка виртуального терминала и запрет буферизации
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm

WORKDIR /app

# Устанавливаем системные утилиты терминала (включая clear) и websockets
RUN apt-get update && apt-get install -y --no-install-recommends \
    ncurses-base \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir websockets

# Копируем скрипты
COPY index.py /app/index.py
COPY server.py /app/server.py

RUN chmod +x /app/index.py /app/server.py

# Запуск от безопасного пользователя (не root)
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "/app/server.py"]
