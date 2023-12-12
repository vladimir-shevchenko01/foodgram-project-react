<h1 align="center">Социальная сеть <a href="https://prettycat.ddns.net/" target="_blank">Foodgram.</a></h1>

  Foodgram сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяет  создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Проект Foodgram.
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
<img src ="https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/node.js%20-%2343853D.svg?&style=for-the-badge&logo=node.js&logoColor=white"/>
<img src="https://img.shields.io/badge/react%20-%2320232a.svg?&style=for-the-badge&logo=react&logoColor=%2361DAFB"/>
<img src="https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
<img src="https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/>
<img src="https://img.shields.io/badge/github%20actions%20-%232671E5.svg?&style=for-the-badge&logo=github%20actions&logoColor=white"/>

[![Generic badge](https://img.shields.io/badge/TELEGRAM-notification-blue.svg)](https://telegram.org/)

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/vladimir-shevchenko01/foodgram-project-react.git
   cd foodgram
   ```

2. Создайте файл `.env` и заполните его собственными данными:
   ```
   # Секреты DB
   POSTGRES_USER=[имя_пользователя_базы]
   POSTGRES_PASSWORD=[пароль_к_базе]
   POSTGRES_DB=[имя_базы_данных]
   DB_PORT=[порт_соединения_к_базе]
   DB_HOST=[db]
   ```

3. Создайте Docker-образы:
   ```
   cd frontend
   docker build -t [username]/foodgram_frontend .
   cd ../backend
   docker build -t [username]/foodgram_backend .
   cd ../nginx
   docker build -t [username]/foodgram_gateway . 
   ```

4. Загрузите образы на DockerHub:
   ```
   docker push [username]/foodgram_frontend
   docker push [username]/foodgram_backend
   docker push [username]/foodgram_gateway
   ```

## Развертывание на удаленном сервере

1. Подключитесь к удаленному серверу:
   ```
   ssh -i [путь_до_файла_с_SSH_ключом]/[название_файла_с_SSH_ключом] [имя_пользователя]@[ip_адрес_сервера]
   ```

2. Создайте на сервере директорию с именем `foodgram`:
   ```
   mkdir foodgram
   ```

3. Установите Docker Compose на сервере:
   ```
   sudo apt update
   sudo apt install curl
   curl -fSL https://get.docker.com -o get-docker.sh
   sudo sh ./get-docker.sh
   sudo apt-get install docker-compose
   ```

4. Скопируйте файлы `docker-compose.production.yml` и `.env` в директорию `foodgram/` на сервере:
   ```
   scp -i [путь_до_SSH]/[SSH_имя] docker-compose.production.yml [имя_пользователя]@[ip_сервера]:/home/[имя_пользователя]/foodgram/docker-compose.production.yml
   ```

5. Запустите Docker Compose в режиме демона:
   ```
   sudo docker-compose -f docker-compose.production.yml up -d
   ```

6. Выполните миграции, соберите статические файлы бэкенда и скопируйте их в `/backend_static/static/`:
   ```
   sudo docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
   sudo docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic
   sudo docker-compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
   ```

7. Откройте конфигурационный файл Nginx в редакторе Nano:
   ```
   sudo nano /etc/nginx/sites-enabled/default
   ```

8. Добавьте настройки `location` в секции `server`:
   ```
   location / {
       proxy_set_header Host $http_host;
       proxy_pass http://127.0.0.1:9000;
   }
   ```

9. Проверьте правильность конфигурации и перезапустите Nginx:
   ```
   sudo nginx -t
   sudo service nginx reload
   ```

Теперь foodgram развернут на удаленном сервере.