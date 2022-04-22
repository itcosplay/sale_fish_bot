# бот по продаже рыбы
Бот продает рыбу ипользуюя api [moltin](https://www.elasticpath.com/)


Возможности бота:
- Формирует корзину пользователя;
- Записывает email пользователя в CRM для связи.

## Необходимое окружение
|переменная|описание|тип
|----------|--------|--------------
|`TG_BOT_TOKEN`|Токен для бота [telegram](https://core.telegram.org/bots#6-botfather)|string
|`STORE_ID`|id магазина [ElasticPath](https://euwest.cm.elasticpath.com/)|string
|`CLIENT_ID`|id клиента [ElasticPath](https://euwest.cm.elasticpath.com/)|string
|`CLIENT_SECRET`|секретный ключ клиента [ElasticPath](https://euwest.cm.elasticpath.com/)|string


Все переменные окружения должны храниться в файле .env в корне проекта.

## Как установить
* Клонируем репозиторий
* Добавляем файл .env с необходимыми переменными
* Создаем виртуальное окружение
* Устанавливаем зависимости
```
pip install -r requirements.txt
```

## Запуск
Запуск бота в telegram:
```
python bot.py
```

## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
