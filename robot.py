import threading
import sqlite3


class Counter:
    def __init__(self):
        self.active = False # Флаг, включающий/выключающий робота
        self.value = 0 # Значение, которое выведет робот
        self.timer = None
        self.conn = sqlite3.connect("robot.db", check_same_thread=False) # Соединение с БД
        self.cursor = self.conn.cursor() # Курсор для взаимодействия с БД
        self.sessionID = 0 # ID последней вставленной в БД строки, для последующего обновления этой строки

    def create_table(self):
        # Создание таблицы для хранения информации о запусках
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    startTime TEXT,
    endTime TEXT,
    startNumber INTEGER
    )
    ''')
        self.conn.commit()

    def count(self):
        # Тело робота
        print(self.value)
        self.value += 1
        if self.active:
            # Устанавливает таймер, который через секунду снова запустит эту функцию
            self.timer = threading.Timer(1.0, self.count)
            self.timer.start()

    def start(self, begin: int):
        # Запуск робота
        self.cursor.execute(f'''
    INSERT INTO Sessions (startTime, startNumber)
    VALUES (TIME(), {begin})''')
        self.sessionID = self.cursor.lastrowid
        self.conn.commit()
        self.value = begin
        self.active = True
        self.count()

    def end(self):
        # Остановка робота
        self.cursor.execute(f'''
    UPDATE Sessions
    SET endTime = TIME()
    WHERE id={self.sessionID}''')
        self.conn.commit()
        self.sessionID += 1
        self.active = False
        if self.timer:
            self.timer.cancel()

    def clear(self):
        # Очистка истории запусков
        self.cursor.execute("DROP TABLE Sessions")
        self.create_table()

    def show(self):
        # Показ истории запусков

        # Получение информации из БД
        self.cursor.execute('''
    SELECT id, startTime, endTime, startNumber, JULIANDAY(endTime) - JULIANDAY(startTime) AS difference
    from Sessions''')
        # Создание html файла
        html = """<title>История запусков</title>
        <style>
            /* CSS styles for centering the button */
            body {
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
            }

            button {
              font-size: 24px;
              padding: 10px 20px;
            }
          </style>"""
        html += """<button onclick="window.location.href='/clear'">Очистить историю</button>"""
        html += "<table>\n"
        html += ("<tr><th>ID</th><th>Время запуска</th><th>Время остановки</th><th>Стартовое "
                 "число</th><th>Длительность работы</th></tr>\n")
        # Вставка полученной из БД информации в html файл
        for item in self.cursor.fetchall():
            id, startTime, endTime, begin, difference = item
            html += "<tr>"
            html += f"<td>{id}</td>"
            html += f"<td>{startTime}</td>"
            html += f"<td>{endTime}</td>"
            html += f"<td>{begin}</td>"
            html += f"<td>{f"{24 * 60 * 60 * difference:.0f} секунд"}</td>"
            html += "</tr>\n"

        html += "</table>"
        html += """<button onclick="window.location.href='/'">Вернуться</button>"""
        return html
