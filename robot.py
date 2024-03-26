import threading


class Counter:
    def __init__(self):
        self.active = False
        self.value = 0
        self.timer = None

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
        self.value = begin
        self.active = True
        self.count()

    def end(self):
        # Остановка робота
        self.active = False
        if self.timer:
            self.timer.cancel()
