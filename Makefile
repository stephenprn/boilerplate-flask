init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

server_dev:
	python3 -m flask run --host 0.0.0.0

db_dev:
	docker-compose up -d

start_dev: db_dev server_dev