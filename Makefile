PROJECT_ID:=project-id

.PHONY: all
all: dev

.PHONY: deploy
deploy:
	gcloud app deploy --project $(PROJECT_ID) -q

.PHONY: cron
cron:
	gcloud app deploy cron.yaml --project $(PROJECT_ID) -q

.PHONY: test
test:
	coverage run -m pytest -srP; coverage report; coverage html; # open htmlcov/index.html

.PHONY: dev
dev:
	gcloud app deploy app.dev.yaml --project $(PROJECT_ID) -q

.PHONY: prod
prod:
	gcloud app deploy app.prod.yaml --project $(PROJECT_ID) -q

.PHONY: dispatch
dispatch:
	gcloud app deploy dispatch.yaml --project $(PROJECT_ID) -q

.PHONY: browse
browse:
	gcloud app browse --project $(PROJECT_ID)

.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations

.PHONY: env_local
env_local:
	source .env.local

.PHONY: migrate
migrate:
	python manage.py migrate
