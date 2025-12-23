# 0. Клонирование.

```bash
git clone https://github.com/Myortv/radistesttask
cd radistesttask
```

# 1. Настройка.

Вызовите `setup.sh`.

```bash
source ./setup.sh
```

Этот скрипт создаёт директорию с логами и предлагает промпт для ввода значений `.env`.

Альтернативно, вы можете:

```bash
mkdir logs
touch logs/logfile


cp .env.example .env
vim .env
```

# 2. Запуск.

```
docker compose build
docker compose up
```

Сваггер будет доступен по [localhost:8000/docs](http://localhost:8000/docs)

Вы будете видеть логи в консоли, также логи будут находится в `logs/`

# 3. Curl запросы для тестирования
Небольшие курл запросы, с простыми данными для тестирования. Для полных схем данных нужно смотреть сваггер.

> /api/client/list
```bash
curl -X 'GET' \
  'http://localhost:8000/api/client/list?pagination_limit=20&pagination_offset=0' \
  -H 'accept: application/json'
```

```bash
curl -X 'GET' \
  'http://localhost:8000/api/client/list?customer_name=name&customer_email=email%40email.com&customer_registration_date=2025-12-23&pagination_limit=20&pagination_offset=20' \
  -H 'accept: application/json'
```


> /api/client/
```bash
curl -X 'POST' \
  'http://localhost:8000/api/client/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer":
   {"firstName": "name"}
}'
```


> /api/order/list
```bash
curl -X 'GET' \
  'http://localhost:8000/api/order/list?customer_id=41&pagination_limit=20&pagination_offset=0' \
  -H 'accept: application/json'
```


> /api/order
```bash
curl -X 'POST' \
  'http://localhost:8000/api/order/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer": {
    "id": 40
  },
  "items": [
    {
      "initialPrice": 100,
      
      "comment": "string"
    }
  ],
  "number": "EE6969"
}'
```


> /api/payment
```bash
curl -X 'POST' \
  'http://localhost:8000/api/payment/?order_id=43' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 99,
  "comment": "comment comment",
  "type": "bank-card"
}'
```
**Результат можно проверить, если получить список ордеров со связанным заказом. Там будет поле оплат.**

# 4. Комментарии к проекту.

Проект довольно простой, но документация retailcrm довольно своеобразная. Формат описания входных и выходных данных очень неудобный.
Использование форм для сложных данных в целом довольно неудобно.

Например, чтобы создать заказ, нужно отправлять что-то вроде:

```python
>>> client.request(..., body={"payment": '{"order": {"id": 10}, "type": "bank-card"}'})
```

Где у нас значение payment уже собрано в json строку.
```python
>>> body = {"payment": '{"order": {"id": 10}, "type": "bank-card"}'}
>>> type(body['payment'])
<class 'str'>
```

Мне лично несколько раз приходилось открывать код [клиентской библиотеки](https://github.com/retailcrm/api-client-python), чтобы понять, в каком формате данные уходят на сервер.

По тому, как они предоставляют данные, довольно сложно ориентироваться -- сложно понять вложенность, или, например, считать что что-то является листом.
На мой вкус, было бы лучше привести реальные примеры того как эти данные уходят, ходя бы с curl-ом. С возможностью быстро взять этот запрос, скопировать и запустить в терминале, чтобы посмотреть как работает апи.

В целом всё :D
