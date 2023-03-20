# Flask SQLAlchemy API boilerplate

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

## Development run local server

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
