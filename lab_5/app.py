import time
import redis
from flask import Flask
from datetime import datetime

app = Flask(__name__)

cache = redis.Redis(host='localhost', port=6379)

def get_hit_count():
    retries = 5

    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
    <h1 style="color:green">Бизнес-стенд "Инновации"</h1>

    <p>Посетителей сегодня: <strong>{count}</strong></p>

    <p>Время сервера: <strong>{current_time}</strong></p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)