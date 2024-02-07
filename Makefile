.PHONY: isort, test, lint, migrations

ifeq ($(OS),Windows_NT)
    OPEN := start
else
    UNAME := $(shell uname -s)
    ifeq ($(UNAME),Linux)
        OPEN := xdg-open
    endif
endif


isort:
	isort app
	isort parser

black:
	black app
	black parser

test:
	python manage.py test

lint:
	flake8 app
	flake8 parser

migrations:
	python manage.py makemigrations
	python manage.py migrate