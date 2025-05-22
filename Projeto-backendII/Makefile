

.PHONY: help run test lint docker-build docker-up docker-down clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make run           - Rodar o servidor FastAPI localmente (uvicorn)"
	@echo "  make test          - Rodar todos os testes (pytest)"
	@echo "  make lint          - Rodar flake8 para linting do código"
	@echo "  make docker-build  - Build da imagem Docker"
	@echo "  make docker-up     - Subir stack com Docker Compose"
	@echo "  make docker-down   - Parar stack Docker Compose"
	@echo "  make clean         - Remover arquivos pyc, cache e logs temporários"

run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest --maxfail=1 --disable-warnings -v

lint:
	flake8 app/ main.py

up:
	docker-compose up --build

docker-build:
	docker build -t backendii:latest .

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache logs/*.log app/__pycache__ app/**/*.pyc
