build:
	poetry install
	poetry run python src/web/manage.py tailwind install
	poetry run python src/web/manage.py tailwind build
	poetry run python src/web/manage.py migrate

run:
	poetry run python src/web/manage.py runserver 0.0.0.0:8000


create-superuser:
	poetry run python src/web/manage.py createsuperuser

