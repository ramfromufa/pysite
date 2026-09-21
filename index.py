#!/usr/bin/env python3
"""Async Flask terminal page for moneyfornothing.su.

Run locally with:
    pip install "Flask[async]"
    python index.py

Put a reverse proxy (nginx, Caddy, etc.) in front of this process for the
moneyfornothing.su domain and serve it over HTTPS.
"""

from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ГОСКОМБЛАГ // ПП-7</title>
  <style>
    :root { color-scheme: dark; }
    * { box-sizing: border-box; }
    html, body { min-height: 100%; margin: 0; }
    body {
      background: #000;
      color: #39ff14;
      font-family: "Courier New", Courier, monospace;
      font-size: clamp(14px, 1.6vw, 19px);
      text-shadow: 0 0 5px #19ff00;
      overflow: hidden;
    }
    body::after {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background: repeating-linear-gradient(
        to bottom, transparent 0, rgba(50, 255, 20, .035) 1px,
        transparent 2px, transparent 4px
      );
      opacity: .7;
    }
    #terminal {
      min-height: 100vh;
      padding: 3vh 4vw;
      white-space: pre-wrap;
      word-break: break-word;
      outline: none;
      animation: flicker 4s infinite;
    }
    .cursor {
      display: inline-block;
      width: .65em;
      height: 1.05em;
      margin-left: .15em;
      vertical-align: -.15em;
      background: #39ff14;
      box-shadow: 0 0 8px #19ff00;
      animation: blink .85s steps(1, end) infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }
    @keyframes flicker {
      0%, 18%, 22%, 63%, 64%, 96%, 100% { opacity: 1; }
      20%, 62%, 97% { opacity: .88; }
    }
  </style>
</head>
<body>
  <main id="terminal" tabindex="0" aria-live="polite"></main>
  <script>
    const terminal = document.getElementById('terminal');
    const width = 80;
    const line = (char = '=') => char.repeat(width);
    const header = `================================================================================
ГОСУДАРСТВЕННЫЙ КОМИТЕТ СССР ПО АВТОМАТИЗАЦИИ И ПЕРЕРАСПРЕДЕЛЕНИЮ БЛАГ (ГОСКОМБЛАГ)
Центральная Система Учета и Взаимопомощи Трудящихся «МОЛОДЦЫ-УДАЛЬЦЫ»
================================================================================
Текущая дата: 21 сентября 1986 года                    Статус узла: СВЯЗЬ УСТАНОВЛЕНА
Режим: ОТКРЫТЫЙ                                           ПП-7 / MONEY FOR NOTHING
================================================================================

[ ИДЕОЛОГИЧЕСКАЯ УСТАНОВКА ДНЯ ]
«Кто не работает — тот не ест, но тот, кто автоматизировал труд,
получает по потребностям в рамках утвержденных фондов материального поощрения!»

--------------------------------------------------------------------------------
ГЛАВНОЕ МЕНЮ СИСТЕМЫ (нажмите любую клавишу; Enter не требуется):
--------------------------------------------------------------------------------
  1. [ОБЩИЙ ФОНД]  Свободные остатки излишков производства.
  2. [ЗАЯВКА]      Прошение на выделение материальных благ безвозмездно.
  3. [ОБМЕН]       Излишки личного подсобного хозяйства в фонд «Ничего».
  4. [ЖАЛОБЫ]      Регистр граждан, получающих блага незаслуженно.
  5. [СПРАВКА]     Постановление ЦК КПСС о нетрудовых доходах.

--------------------------------------------------------------------------------
[ НОВОСТИ ПЛАНОВОЙ СЕТИ ]
* Стахановцы передали 500 тыс. нормо-часов.
* Выдача дефицитных чеков «Посылторга» временно приостановлена.
--------------------------------------------------------------------------------`;

    const responses = {
      '1': `РАЗДЕЛ 1: ОБЩИЙ ФОНД ИЗЛИШКОВ\n${line('-')}\nНа складах Госкомблага обнаружены нераспределенные блага:\n* Автомобили «Москвич-412» — 2 шт. (выделено ветеранам труда)\n* Гарнитуры мебельные «жилая комната» — 14 шт.\n* Ковры шерстяные (Узбекская ССР) — 45 шт.\n* Чеки Внешпосылторга серии «Д» — ОШИБКА ДОСТУПА: ДАННЫЕ ЗАСЕКРЕЧЕНЫ.`,
      '2': `РАЗДЕЛ 2: ОФОРМЛЕНИЕ БЕЗВОЗМЕЗДНОЙ ЗАЯВКИ\n${line('-')}\nВаш запрос на получение «Money for Nothing» зафиксирован.\nПрисвоен номер прошения: ЭВМ-${Math.floor(10000 + Math.random() * 90000)}\nСтатус: НА РАССМОТРЕНИИ В РАЙКОМЕ.\n\nПриблизительное время ожидания: 4 года, 7 месяцев, 12 дней.`,
      '3': `РАЗДЕЛ 3: СДАЧА ИЗЛИШКОВ\n${line('-')}\nТоварищ! Излишки личного хозяйства разрушают социалистическую мораль!\nСдайте в заготовительную контору картофель и яблоки.\nВзамен будет начислено 0.00 руб. (социалистическая благодарность).`,
      '4': `РАЗДЕЛ 4: РЕГИСТР УЧЕТА ТУНЕЯДЦЕВ И ДАРМОЕДОВ\n${line('-')}\nВНИМАНИЕ! Сигналы граждан проверяются дружинниками в течение 24 часов.\n[ФУНКЦИЯ ДЕАКТИВИРОВАНА ДО ПРИБЫТИЯ СЛЕДОВАТЕЛЯ]`,
      '5': `РАЗДЕЛ 5: СПРАВОЧНАЯ ИНФОРМАЦИЯ\n${line('-')}\nВыдержка из Уголовного Кодекса РСФСР (Статья 209):\n«Систематическое занятие бродяжничеством или попрошайничеством...\nнаказывается лишением свободы на срок до одного года или исправительными работами».\n\nВыдача средств системой «МОЛОДЦЫ-УДАЛЬЦЫ» тунеядством не является.`,
    };

    function show(text) {
      // textContent replaces the complete previous screen and avoids HTML injection.
      terminal.textContent = text;
      const cursor = document.createElement('span');
      cursor.className = 'cursor';
      cursor.setAttribute('aria-hidden', 'true');
      terminal.appendChild(cursor);
    }

    function keyLabel(event) {
      if (event.key === ' ') return 'ПРОБЕЛ';
      if (event.key.length === 1) return event.key;
      return `[${event.key}]`;
    }

    document.addEventListener('keydown', (event) => {
      event.preventDefault();
      const key = event.key.toLowerCase();
      const response = responses[key];
      show(response || `СИГНАЛ «${keyLabel(event)}» ПРИНЯТ.\n\nКОД НЕ ПРЕДУСМОТРЕН ДЛЯ ДАННОГО ТЕРМИНАЛА.\nНажмите любую клавишу для нового запроса.`);
    });

    show(header);
    window.addEventListener('load', () => terminal.focus());
    document.addEventListener('click', () => terminal.focus());
  </script>
</body>
</html>"""


@app.get("/")
async def index():
    """Return the terminal UI without requiring an HTML form."""
    return await render_template_string(PAGE)


if __name__ == "__main__":
    # The domain should normally be terminated by nginx/Caddy and proxied here.
    app.run(host="127.0.0.1", port=8000, debug=False)
