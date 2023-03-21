# Flask SQLAlchemy REST API boilerplate

This is a boilerplate to create a REST API based on Flask framework including following features:
- User authentication with `flask-jwt-extended` (including `/login`, `/register` and authentication-required routes)
- Query parameters / body validators with `marshmallow`
- Postgres SQL database queries with repository pattern implemented with `SQLAlchemy`
- Postgres SQL migrations with `alembic`

This project also includes:
- Dependencies management with `pip`
- Postgres SQL database set-up with `docker`
- Pre-commit hooks including `autoflake`, `isort` and `black` stages

## Development set-up

1. Create `.env` file based on `.env.template` and source it:
```
source .env
```

2. Create virtual environment, source it and install dev dependencies
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r dev_requirements.txt
```

3. Start docker db and start local server
```
make start_dev
```

4. Install pre-commit hooks
```
pre-commit install
```

## Development run local server (once set-up is done)

1. Source `.env` and Python virtual env:
```
source .env
source venv/bin/activate
```

2. Start docker db and start local server
```
make start_dev
```

## TODO

[ ] generate auto-doc
[ ] alembic
[ ] tests
[ ] permission layer
[ ] rename packages without "s"