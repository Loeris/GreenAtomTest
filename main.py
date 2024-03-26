import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from robot import Counter
from HTMLs import html_root, html_start

app = FastAPI()
robot = Counter()


@app.get("/")
def root():
    # Стартовая страница
    # Остановка робота
    robot.end()
    return HTMLResponse(html_root)


@app.get("/start")
def start(begin: int = 0):
    # Запуск робота
    # begin - число, с которого робот начнёт считать
    robot.start(begin)
    return HTMLResponse(html_start)


if __name__ == "__main__":
    # Запуск сервера
    uvicorn.run(app, host="127.0.0.1", port=8000)
