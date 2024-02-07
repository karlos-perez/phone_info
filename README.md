## Определение оператора и региона по номеру телефона

По данным Реестра российской системы и плана нумерации



### Настрока парсера загрузки данных

Установить через cronab выполнение парсера ночью

```shell
crontab -e

0 2 * * * python3 /opt/phone_number/parser/main.py
```

### Django

Админка django по адресу: http://.../adminKa/
Документация по API: http://.../api/swagger/

### Запуск проекта

```shell
# Создаем виртуальное окружение
python3.11 -m venv venv

# Устанваливаем зависимости
pipenv install

# Делаем миграции в БД
python3 manage.py makemigrations
python3 manage.py migrate

или

make migrations

# Создаем суперпользователя (нужен для админки)
python3 manage.py createsuperuser

# Запускаем парсер для первоначальной наполнении БД
python3 ./parse/main.py
```