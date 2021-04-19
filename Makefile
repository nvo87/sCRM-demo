RUN=docker-compose exec -T app
REPORT_DIR=./reports
MSG_TEMPLATE='\"{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}\"'
DJANGO_SETTINGS_MODULE=config.settings


.PHONY: rebuild stop start restart manage tests pylint pycodestyle lint precommit psql makemigrations migrate


start:
	docker-compose up -d --build --remove-orphans

stop:
	 docker-compose down

rebuild: stop start

restart:
	 docker-compose stop && docker-compose up -d --remove-orphans

manage:
	 $(RUN) python ./manage.py $(filter-out $@,$(MAKECMDGOALS)) --settings=$(DJANGO_SETTINGS_MODULE)

makemigrations:
	$(RUN) python ./manage.py makemigrations

migrate:
	$(RUN) python ./manage.py migrate

tests:
	mkdir -p ${REPORT_DIR} && \
	$(RUN) pytest

pycodestyle:
		mkdir -p ${REPORT_DIR} && \
		$(RUN) sh -c "pycodestyle ./ " \
		| tee ${REPORT_DIR}/pycodestyle.report

pylint:
		mkdir -p ${REPORT_DIR} && \
		$(RUN) sh -c "pylint ./**/*.py --rcfile=../.pylintrc -j 0 --msg-template=${MSG_TEMPLATE}" \
		| tee ${REPORT_DIR}/pylint.report

lint: pycodestyle pylint

precommit: tests lint

psql:
	$(RUN_DB) psql -U postgres -w
