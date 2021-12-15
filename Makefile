install:
	poetry install

dev: 
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest -v app/*

prod:
	poetry run gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

exportdeps:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

build:
	docker build -t apig .

run:
	docker run --name=apig --env-file=.env -p 8000:80 -it apig

deploy:
	sh ./push.sh

setup-localstack:
	docker-compose up -d && sh ./localstack-entrypoint.sh

run-stack:
	SERVICES=lambda,sqs DEBUG=1 poetry run localstack start
