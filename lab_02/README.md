
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

## Архитектура системы

```mermaid
graph LR

User[Пользователь / curl] --> Nginx[Nginx (порт 80)]
Nginx -->|proxy_pass| Flask[Flask API (порт 5000)]
Flask --> Data[Список продуктов (в памяти)]

Nginx --> Cache[Кеш nginx]
Cache --> Nginx
```

---

# Ход выполнения

---
Вот короткий вариант без лишнего анализа — просто вставляй 👇

---

## Часть 1. Анализ HTTP-запросов

Был выполнен POST-запрос к API сервиса reqres:

```bash
curl -i -X POST https://reqres.in/api/users \
-H "Content-Type: application/json" \
-H "x-api-key: test123" \
-d '{"name":"Ivan","job":"student"}'
```

Сервер вернул ответ со статусом:

* **403 Forbidden**

В заголовках ответа присутствует информация о сервере и типе содержимого, а в теле ответа указана ошибка:

```json
"error": "invalid_api_key"
```

📷 Скриншот выполнения запроса:
<img width="1707" height="1082" alt="image" src="https://github.com/user-attachments/assets/b4bbbfce-ad0a-42a8-bead-063997f489ff" />


---


## Часть 2. Реализация REST API на Flask

Было разработано веб-приложение на Flask для управления списком товаров.

### Реализованные методы API:

* `GET /api/products` — получение списка товаров
* `GET /api/products/<id>` — получение товара по идентификатору
* `POST /api/products` — добавление нового товара

---

### Тестирование API

Получение списка товаров:

```bash
curl http://127.0.0.1:5000/api/products
```

📷 Скриншот:
<img width="1811" height="822" alt="image" src="https://github.com/user-attachments/assets/1f0af296-a95d-4346-aa8f-632cd7e115cc" />


---

Создание нового товара:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name": "Apple", "price": 120, "stock": 30}' \
http://127.0.0.1:5000/api/products
```

📷 Скриншот:
<img width="1731" height="345" alt="image" src="https://github.com/user-attachments/assets/9a070204-f08f-4915-b101-97d7113e641d" />


---

Повторное получение списка:

```bash
curl http://127.0.0.1:5000/api/products
```

📷 Скриншот:
<img width="878" height="618" alt="image" src="https://github.com/user-attachments/assets/ade3aa13-cc5d-4a5d-9f48-537723abc1ad" />


---

Получение товара по id:

```bash
curl http://127.0.0.1:5000/api/products/1
```

📷 Скриншот:
<img width="873" height="224" alt="image" src="https://github.com/user-attachments/assets/c26ccde2-a975-4cd7-a4ee-cea2a41ed6f8" />


---

## Часть 3. Настройка Nginx

Был установлен и запущен веб-сервер nginx.

Проверка работы выполнялась через браузер по адресу:

```
http://localhost
```

📷 Скриншот:
<img width="2770" height="620" alt="image" src="https://github.com/user-attachments/assets/f3d3e6d8-77bc-45b1-93d7-b5dd0a1a43d4" />

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
<img width="874" height="732" alt="image" src="https://github.com/user-attachments/assets/1fd134f2-4413-4221-8f3c-ea23cf6fe5a4" />




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
<img width="885" height="857" alt="image" src="https://github.com/user-attachments/assets/464469bc-7367-40f8-af7e-68a19b304d7c" />


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


