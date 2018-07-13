Установка микросервисов.

1.Запускаем MongoDB
2.В файле config.py прописываем свои параметры
3. Запускаем файл init_microservises.py в папке initialize, он создаст коллекции и правила валидации для них.

Запуск микросервисов
Запустите файлы offers.py и/или users.py


Примеры запросов.

Регистрация нового пользователя:
curl -X POST http://0.0.0.0:8000/user/registry/ -H "Content-Type: application/json" -d
'{"username": "username", "password": "password", "created_at": 01072018}'

Авторизация пользователя:
curl -X POST http://0.0.0.0:8000/user/auth/ -H "Content-Type: application/json" -d
'{"username": "username", "password": "password"}'

Получение информации об offer:
curl -X POST http://0.0.0.0:8000/offer/ -H "Content-Type: application/json" -d '{"offer_id": 1}'
