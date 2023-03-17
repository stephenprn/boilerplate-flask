init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

init_dev:
	python3 -m venv venv
	. venv/bin/activate
	python3 -m pip install -r dev_requirements.txt

server_dev:
	python3 -m flask run --host 0.0.0.0

db_dev:
	docker-compose up -d

env_dev:
	. venv/bin/activate
	. .env

start_dev: env_dev db_dev server_dev