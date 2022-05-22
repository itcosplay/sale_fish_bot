# бот по продаже рыбы
Бот продает рыбу ипользуюя api [moltin](https://www.elasticpath.com/)

найти в telegram: @pi_tasty_bot

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

## Запускаем бота локально с использованием Docker
Предварительно должен быть установлен и работать Docker. 

* клонируем репозиторий
```
git clone git@github.com:itcosplay/sale_fish_bot.git
```

* добавляем файл .env в корень проекта со необходимыми переменными

* собираем контейнер
```
docker build -t sale-fish-bot .
```

* запускаем контейнер
```
docker run --rm sale-fish-bot
```

## Стремительный деплой на heroku с использованием Docker
Предварительно должен быть установлен и работать Docker.  
Предварительно должен быть установлен Heroku, а так же мы должны быть залогинены в нем.
* клонируем репозиторий
```
git clone git@github.com:itcosplay/sale_fish_bot.git
```
* переходим в папку с репозиторием и создаем приложение heroku. Запоминаем имя приложения, которое выдаст нам heroku
```
heroku create
```
* устанавливаем переменные окружения.
```
heroku config:set YOUR_ENV_VAR=VALUE
```
* логинимся в heroku container
```
heroku container:login
```
* создаем и пушим образ в heroku register
```
heroku container:push --app <your-app-name-from-heroku> worker
```
* создаем релиз (запускаем приложение на heroku)
```
heroku container:release --app <your-app-name-from-heroku> worker
```
* делаем так, чтобы бот не падал через минуту
```
heroku ps:scale worker=1
```
* при желании, можно насладиться логами
```
heroku logs --tail --app floating-hamlet-23367
```


## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
