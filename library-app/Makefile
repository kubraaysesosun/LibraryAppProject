SHELL := /bin/bash

up:
	docker-compose up -d

kill:
	docker-compose kill

build:
	docker-compose build

ps:
	docker-compose ps

exec:
	docker-compose exec app $(args)

logs:
	docker-compose logs $(args) -f

mm:
	docker-compose exec app alembic revision --autogenerate -m "$(args)"

migrate:
	docker-compose exec app alembic upgrade head

downgrade:
	docker-compose exec app alembic downgrade $(args)

make_user_admin:
	docker-compose exec app python app/scripts/make_user_admin.py $(args)
