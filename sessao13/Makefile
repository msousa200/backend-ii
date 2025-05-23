
.PHONY: setup-django setup-fastapi setup-challenge run-django run-fastapi run-challenge test-django test-fastapi test-challenge install-requirements docker-build docker-run docker-compose-up docker-compose-down


setup-django:
	cd django_hello && pip install -r requirements.txt && python manage.py migrate

setup-fastapi:
	cd fastapi_hello && pip install -r requirements.txt

setup-challenge:
	cd challenge/refactored && pip install -r requirements.txt

setup-all: setup-django setup-fastapi setup-challenge


docker-build:
	docker build -t django-hello ./django_hello
	docker build -t fastapi-hello ./fastapi_hello
	docker build -t challenge-app ./challenge/refactored

docker-run:
	docker run -d -p 8001:8000 --name django-hello django-hello
	docker run -d -p 8002:8000 --name fastapi-hello fastapi-hello
	docker run -d -p 8003:8000 --name challenge-app challenge-app

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down


run-django:
	cd django_hello && python manage.py runserver

run-fastapi:
	cd fastapi_hello && python run.py

run-challenge:
	cd challenge/refactored && python run.py


test-django:
	cd django_hello && python manage.py test

test-fastapi:
	cd fastapi_hello && pytest tests/test_app.py -v

test-challenge:
	cd challenge/refactored && pytest tests/test_api.py -v

test-all: test-django test-fastapi test-challenge


install-requirements:
	pip install -r django_hello/requirements.txt
	pip install -r fastapi_hello/requirements.txt
	pip install -r challenge/refactored/requirements.txt
