# Notebook
Реализация RESTful API для работы с записной книгой


Склонируйте репозиторий на свой компьютер:

```bash
git clone https://github.com/Nechepor/Notebook.git
```

1. Для локального запуска проекта:
   - в файле .env измените значение DEV_MODE на True
   - в файле docker-compose.yml закомментируйте web, чтобы выглядело так:
```yml  
version: "3"

services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data

  #web:
  #  image: python:3.10
  #  environment:
  #    DEV_MODE=${DEV_MODE}
  #  command: sh -c "pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
  #  volumes:
  #    - .:/app
  #  ports:
  #    - "8000:8000"
  #  depends_on:
  #    - db

volumes:
  postgres_data:
```  
   - откройте корневую папку проекта (где лежит docker-compose.yml)
```bash
cd /your/path/Notebook
```
   - Поднимите БД с помощью команды docker-compose up -d. При желании, можно изменить в файле название Бд, Юзера и пароль. Но тогда потребуются изменения в настройках проекта
   - находясь в той же директории выполните команду python manage.py migrate - накатятся все миграции на БД
   - python manage.py add_admin - Создается свой суперюзер на основе данных из .env, но можно и через python manage.py createsuperuser
   - запустите проект с помощью команды python manage.py runserver

2. Для запуска с помощью docker-compose:
   - Проверьте значение DEV_MODE в .env - должно быть False
   - Проверьте Чтобы docker-compose.yml не содержал в себе закомментированный web
   - Перейдите в директорию, куда склонировали проект.
   - Выполните команду docker-compose up. По дефолту, суперюзер будет с данными admin\password
