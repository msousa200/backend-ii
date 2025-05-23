help: 
	# From https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



up: 
	docker-compose up -d

down: 
	docker-compose down

build: 
	docker-compose build

logs:
	docker-compose logs -f

clean:
	docker-compose down --volumes --remove-orphans

test: 
	docker-compose run api pytest

lint: 
	docker-compose run api ruff .