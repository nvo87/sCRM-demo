COMPOSE=docker-compose -f docker-compose.yml
RUN=$(COMPOSE) exec -T app
RUN_DB=$(COMPOSE) exec -T db
DJANGO_SETTINGS_MODULE=config.settings


.PHONY: rebuild stop start restart manage tests psql

start:
	$(COMPOSE) up -d --build --remove-orphans

stop:
	 $(COMPOSE) down

rebuild:
	 $(COMPOSE) down && ${COMPOSE} up -d --build --remove-orphans

restart:
	 $(COMPOSE) stop && ${COMPOSE} up -d --remove-orphans

manage:
	 $(RUN) python ./manage.py $(filter-out $@,$(MAKECMDGOALS)) --settings=$(DJANGO_SETTINGS_MODULE)

tests:
	 $(RUN) pytest

psql:
	$(RUN_DB) psql -U postgres -w
