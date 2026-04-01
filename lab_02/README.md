
# Лабораторная работа №2

**Номер варианта:** 10

---

# Цель работы

Изучить методы отправки и анализа HTTP-запросов с использованием инструментов telnet и curl.
Освоить базовую настройку и анализ работы веб-сервера nginx в качестве обратного прокси.
Изучить и применить на практике архитектурный стиль REST для создания веб-сервисов на языке Python.

---

# Краткие теоретические сведения

**HTTP (HyperText Transfer Protocol)** — это протокол передачи данных между клиентом и сервером.
Клиент отправляет HTTP-запрос, а сервер возвращает ответ с кодом состояния (например, 200 OK, 404 Not Found, 201 Created).

**REST (Representational State Transfer)** — это архитектурный стиль взаимодействия компонентов распределённой системы.
В REST используются стандартные HTTP-методы:

* GET — получение данных
* POST — создание ресурса
* PUT — обновление
* DELETE — удаление

**Nginx** — это высокопроизводительный веб-сервер, который может использоваться как:

* сервер статического контента
* обратный прокси (reverse proxy)
* балансировщик нагрузки

---

# Описание задания (вариант 10)

В рамках варианта необходимо:

* выполнить анализ HTTP-запроса методом POST
* реализовать REST API для управления товарами
* настроить nginx как обратный прокси
* реализовать кеширование ответов (200 OK) на 2 минуты
* протестировать систему с помощью curl

---

# Ход выполнения

---

## Часть 1. Анализ HTTP-запросов

Был выполнен POST-запрос к тестовому API:

```bash
curl -i -X POST https://reqres.in/api/users \
-H "Content-Type: application/json" \
-d '{"name": "Anna", "job": "student"}'
```

Сервер вернул ответ со статусом:

* **201 Created** — ресурс успешно создан

В ответе также были возвращены дополнительные данные: идентификатор пользователя и время создания.

📷 Скриншот выполнения запроса:
![Скрин 1](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_1)

---

## Часть 2. Реализация REST API на Flask

Было разработано веб-приложение на Flask для управления списком товаров.

### Реализованные методы API:

* `GET /api/products` — получение списка товаров
* `GET /api/products/<id>` — получение товара по идентификатору
* `POST /api/products` — добавление нового товара

---

### Листинг кода приложения (app.py)

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Milk", "price": 80, "stock": 10},
    {"id": 2, "name": "Bread", "price": 50, "stock": 20}
]

next_id = 3


@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


@app.route('/api/products', methods=['POST'])
def create_product():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    new_product = {
        "id": next_id,
        "name": data.get("name"),
        "price": data.get("price"),
        "stock": data.get("stock")
    }

    products.append(new_product)

    next_id += 1

    return jsonify(new_product), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

### Тестирование API

Получение списка товаров:

```bash
curl http://127.0.0.1:5000/api/products
```

📷 Скриншот:
![Скрин 2](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_2)

---

Создание нового товара:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name": "Apple", "price": 120, "stock": 30}' \
http://127.0.0.1:5000/api/products
```

📷 Скриншот:
![Скрин 3](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_3)

---

Повторное получение списка:

```bash
curl http://127.0.0.1:5000/api/products
```

📷 Скриншот:
![Скрин 4](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_4)

---

Получение товара по id:

```bash
curl http://127.0.0.1:5000/api/products/1
```

📷 Скриншот:
![Скрин 5](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_5)

---

## Часть 3. Настройка Nginx

Был установлен и запущен веб-сервер nginx.

Проверка работы выполнялась через браузер по адресу:

```
http://localhost
```

📷 Скриншот:
![Скрин 6](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_6)

---

### Настройка reverse proxy и кеширования

В конфигурационный файл nginx был добавлен следующий блок:

```nginx
location /api/ {

    proxy_cache api_cache;
    proxy_cache_valid 200 2m;
    add_header X-Cache-Status $upstream_cache_status;

    proxy_pass http://127.0.0.1:5000;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

📷 Скриншот конфигурации:
![Скрин config](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_CONFIG)

---

## Часть 4. Тестирование системы

Первый запрос через nginx:

```bash
curl -i http://localhost/api/products
```

Ответ:

```
X-Cache-Status: MISS
```

📷 Скриншот:
![Скрин 7](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_7)

---

Повторный запрос:

```bash
curl -i http://localhost/api/products
```

Ответ:

```
X-Cache-Status: HIT
```

📷 Скриншот:
![Скрин 8](ВСТАВИТЬ_ССЫЛКУ_НА_СКРИН_8)

---

# Вывод

В ходе выполнения лабораторной работы были изучены:

* методы отправки HTTP-запросов с использованием curl
* анализ кодов состояния HTTP
* разработка REST API на Flask
* настройка веб-сервера nginx
* реализация обратного прокси
* применение кеширования для повышения производительности

Созданный веб-сервис корректно обрабатывает запросы, а nginx успешно проксирует и кеширует ответы, что подтверждено результатами тестирования.


