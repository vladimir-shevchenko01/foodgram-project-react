#!/bin/sh

# Ждем, пока netcat не вернет успешный код выхода (успешное соединение)
while pg_isready -h db -p 5432; do
    sleep 5
    echo "Ожидание базы данных"
done
echo "База данных подключена"

# Продолжаем с остальными командами
echo "_____________Выполняем миграции_________________"
python manage.py makemigrations users recipes components
python manage.py migrate
echo "_____________Собираем статику_________________"
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput --first_name i --last_name m
echo "_____________загружаем фикстуры_________________"
python manage.py loaddata ingredients.json
python manage.py loaddata tags.json
echo "_____________фикстуры загружены_________________"

# Запускаем gunicorn после успешного завершения предыдущих команд
echo "_____________Запускаем gunicorn_________________"
gunicorn -w 2 -b 0:8000 foodgram.wsgi:application

echo "_____________gunicorn подключен_________________";
