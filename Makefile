build:
	poetry install
	poetry run python src/web/manage.py tailwind install
	poetry run python src/web/manage.py tailwind build
	poetry run python src/web/manage.py migrate

run:
	poetry run python src/web/manage.py runserver


create-superuser:
	poetry run python src/web/manage.py createsuperuser

