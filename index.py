#!/usr/bin/env python3
import os
import sys
import time
import random

def clear_screen(): # Для Linux
    os.system("clear")

def get_key(): # Считывает одну клавишу без необходимости нажимать Enter. Для Linux
    
    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def print_typewriter(text, delay=0.001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def show_loading():
    clear_screen()
    print_typewriter(
        "ОБРАБОТКА ЗАПРОСА ЦЕНТРАЛЬНЫМ ВЫЧИСЛИТЕЛЬНЫМ ЦЕНТРОМ БЭСМ-6"
    )
    print_typewriter(
        "." * random.randint(2, 4), 0.5
    )

def wait_for_return():
    print_typewriter(r"""
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
<span style="color: #006400;">Нажмите <a href="javascript:void(0);" onclick="ws.send('\r')">[Enter]</a> для возврата домой.</span>"""
    )
    while True:
        key = get_key()
        if key in ("\r", "\n"): # Enter в разных терминалах может определяться как \r или \n
            return "0"

def wait_for_test_id(test_ids):
    print_typewriter("""
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
<span style="color: #006400;">Нажмите одну из клавиш: """ + ", ".join(test_ids) + r"""</span>"""
    )
    while True:
        key = get_key()
        if key in test_ids:
            return test_ids[key]

def wait_for_test_id_or_return(test_ids):
    print_typewriter(r"""
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
<span style="color: #006400;">Нажмите <a href="javascript:void(0);" onclick="ws.send('\r')">[Enter]</a> для возврата домой
или одну из клавиш: """ + ", ".join(test_ids) + r"""</span>"""
    )
    while True:
        key = get_key()
        if key in test_ids:
            return test_ids[key]
        elif key in ("\r", "\n"): # Enter в разных терминалах может определяться как \r или \n
            return "0"





def main_menu():
    test_id = "0"
    while True:
        if test_id == "0":
        
            text = r"""
<span style="color: #32CD32;">
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">==========================================================================================================================================================</div>
ГОСУДАРСТВЕННЫЙ КОМИТЕТ СССР ПО АВТОМАТИЗАЦИИ И ПЕРЕРАСПРЕДЕЛЕНИЮ БЛАГ (ГОСКОМБЛАГ)
Центральная Система Учета и Взаимопомощи Трудящихся «МОЛОДЦЫ-УДАЛЬЦЫ»
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">==========================================================================================================================================================</div>
Текущая дата: 21 сентября 1986 года                          Время: 10:15:23
Статус узла: СВЯЗЬ УСТАНОВЛЕНА (ПП-7)                        Режим: ОТКРЫТЫЙ
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">==========================================================================================================================================================</div></span>

[ ИДЕОЛОГИЧЕСКАЯ УСТАНОВКА ДНЯ ]
«Кто не работает — тот не ест, но тот, кто автоматизировал труд,
 получает по потребностям в рамках утвержденных фондов материального поощрения!»

<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
ГЛАВНОЕ МЕНЮ СИСТЕМЫ (Нажмите цифру 1-5):
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>

 1. <a href="javascript:void(0);" onclick="ws.send('1')">[ОБЩИЙ ФОНД]</a>  Ознакомиться со свободными остатками излишков производства.
 2. <a href="javascript:void(0);" onclick="ws.send('2')">[ЗАЯВКА]</a>      Подать прошение на выделение материальных благ безвозмездно.
 3. <a href="javascript:void(0);" onclick="ws.send('3')">[ОБМЕН]</a>       Сдать излишки личного подсобного хозяйства в фонд «Ничего».
 4. <a href="javascript:void(0);" onclick="ws.send('4')">[ЖАЛОБЫ]</a>      Анонимный регистр учета граждан, получающих блага незаслуженно.
 5. <a href="javascript:void(0);" onclick="ws.send('5')">[СПРАВКА]</a>     Разъяснение Постановления ЦК КПСС о нетрудовых доходах.

<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
[ НОВОСТИ ПЛАНОВОЙ СЕТИ ]
* Стахановцы Н-ского металлургического комбината передали 500 тыс. нормо-часов.
* Внимание! Выдача дефицитных чеков «Посылторга» временно приостановлена."""

            clear_screen()
            print_typewriter(text)

            test_id = wait_for_test_id({"1":"1",
                                      "2":"2",
                                      "3":"3",
                                      "4":"4",
                                      "5":"5"})
            
        elif test_id == "1":
            show_loading()

            text = """
РАЗДЕЛ 1: ОБЩИЙ ФОНД ИЗЛИШКОВ
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
На складах Госкомблага обнаружены нераспределенные блага:
* Автомобили «Москвич-412» (без очереди) — 2 шт. (выделено ветеранам труда)
* Гарнитуры мебельные «жилая комната» — 14 шт.
* Ковры шерстяные (Узбекская ССР) — 45 шт.
* Чеки Внешпосылторга серии «Д» — ОШИБКА ДОСТУПА: ДАННЫЕ ЗАСЕКРЕЧЕНЫ."""

            clear_screen()
            print_typewriter(text)
            test_id = wait_for_return()

        elif test_id == "2":
            show_loading()

            text = f"""
РАЗДЕЛ 2: ОФОРМЛЕНИЕ БЕЗВОЗМЕЗДНОЙ ЗАЯВКИ
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
Ваш запрос на получение «Money for Nothing» зафиксирован.
Присвоен номер прошения: ЭВМ-{random.randint(10000, 99999)}
Статус: НА РАССМОТРЕНИИ В РАЙКОМЕ.

Приблизительное время ожидания в очереди: 4 года, 7 месяцев, 12 дней.
Вам необходимо занести в кабинет №12 справку с места работы и характеристику."""

            clear_screen()
            print_typewriter(text)
            test_id = wait_for_return()

        elif test_id == "3":
            show_loading()

            text = """
РАЗДЕЛ 3: СДАЧА ИЗЛИШКОВ
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
Товарищ! Помните: излишки личного хозяйства разрушают социалистическую мораль!
Заполните бумажную форму 4-Б и сдайте в заготовительную контору:

- Картофель сортовой (не менее 50 кг)
- Яблоки антоновские (для нужд детских садов)

Взамен вам будет начислено 0.00 руб. (социалистическая благодарность)."""

            clear_screen()
            print_typewriter(text)
            test_id = wait_for_return()

        elif test_id == "4":
            show_loading()

            text = """
РАЗДЕЛ 4: РЕГИСТР УЧЕТА ТУНЕЯДЦЕВ И ДАРМОЕДОВ
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
ВНИМАНИЕ! Сигналы граждан проверяются дружинниками в течение 24 часов.

Если ваш сосед слушает зарубежный рок, не работает и утверждает, что получает
«деньги ни за что» — немедленно введите его фамилию в Книгу Сигналов.

[ФУНКЦИЯ ДЕАКТИВИРОВАНА ДО ПРИБЫТИЯ СЛЕДОВАТЕЛЯ]"""

            clear_screen()
            print_typewriter(text)
            test_id = wait_for_return()

        elif test_id == "5":
            show_loading()

            text = """
РАЗДЕЛ 5: СПРАВОЧНАЯ ИНФОРМАЦИЯ
<div style="display: inline-block; max-width: 100%; overflow: hidden; white-space: nowrap; vertical-align: bottom; margin: 0; padding: 0;">----------------------------------------------------------------------------------------------------------------------------------------------------------</div>
Выдержка из Уголовного Кодекса РСФСР (Статья 209):

«Систематическое занятие бродяжничеством или попрошайничеством, а также ведение
в течение длительного времени иного тунеядского образа жизни —
наказывается лишением свободы на срок до одного года или исправительными работами».

Выдача средств в рамках системы «МОЛОДЦЫ-УДАЛЬЦЫ» тунеядством не является,
так как утверждена решением Политбюро ЦК КПСС.

 1. """ + r"""<a href="javascript:void(0);" onclick="ws.send('1')">[page 5.1]</a>""" + """ page 5.1.
 2. """ + r"""<a href="javascript:void(0);" onclick="ws.send('2')">[page 5.2]</a>""" + """ page 5.2.
 3. """ + r"""<a href="javascript:void(0);" onclick="ws.send('3')">[page 5.3]</a>""" + """ page 5.3.
 4. """ + r"""<a href="javascript:void(0);" onclick="ws.send('4')">[page 5.4]</a>""" + """ page 5.4.
 5. """ + r"""<a href="javascript:void(0);" onclick="ws.send('5')">[page 5.5]</a>""" + """ page 5.5.

blablabla"""

            clear_screen()
            print_typewriter(text)
            test_id = wait_for_test_id_or_return({"1":"2",
                                                "2":"3",
                                                "3":"4",
                                                "4":"5",
                                                "5":"1"})


if __name__ == "__main__":
    main_menu()
