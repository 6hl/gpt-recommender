.PHONY: format
format:
	python -m pyright ./src
	python -m ruff check . --fix
	python -m black .

.PHONY: docker-build
docker-build:
	docker build . -f Dockerfile --tag gpt-recommender

.PHONY: docker-run
docker-run:
	docker run -p 8080:8080 -v ./logs:/app/logs -d gpt-recommender

.PHONY: docker-cleanup
docker-cleanup:
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -a -q -f status=exited)