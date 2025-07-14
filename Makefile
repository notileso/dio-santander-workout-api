run:
	@uv run fastapi dev

run-postgres:
	@docker compose -f docker-compose.postgres.yml up -d

stop-postgres:
	@docker compose -f docker-compose.postgres.yml down -v

create-migrations:
	@PYTHONPATH=$PYTHONPATH:${pwd} alembic revision --autogenerate -m $(m)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:${pwd} alembic upgrade head

downgrade-migrations:
	@PYTHONPATH=$PYTHONPATH:${pwd} alembic downgrade -1 head