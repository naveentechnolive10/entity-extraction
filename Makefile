VIRTUAL_ENV=venv
DOCKER_IMAGE_NAME=entity-extraction

local_make: google_credentials $(VIRTUAL_ENV) local_run
	@echo "--------------| local_make is completed |---------------";

local_make_docker: docker_build local_docker_run
	@echo "--------------| local_make_docker is completed |---------------";

make_docker: docker_build docker_run
	@echo "--------------| make_docker is completed |---------------";


$(VIRTUAL_ENV):
	@echo "--------------| install is started |---------------";
	( \
        python3 -m venv $@; \
		. $(VIRTUAL_ENV)/bin/activate; \
		pip --no-cache-dir install -r requirements.txt; \
	)
	@echo "--------------| install is completed |---------------";

google_credentials:
	@echo "--------------| google_credentials command is started |---------------";
	( \
		$(if $(strip $(GOOGLE_APPLICATION_CREDENTIALS)), \
		export GOOGLE_APPLICATION_CREDENTIALS="$(GOOGLE_APPLICATION_CREDENTIALS)", \
		$(error "GOOGLE_APPLICATION_CREDENTIALS should be set before run this application. Follow README.md!!!")); \
	)
	@echo "--------------| google_credentials command is completed |---------------";

local_run:
	@echo "--------------| local_run command is started |---------------";
	( \
		. $(VIRTUAL_ENV)/bin/activate; \
		export FLASK_ENV=development; \
		python run.py; \
    )
	@echo "--------------| local_run command is completed |---------------";

docker_build:
	docker build -t $(DOCKER_IMAGE_NAME) . ;

local_docker_run:
	@echo "--------------| local_docker_run command is started |---------------";
	( \
		docker run -d -p 5000:5000 --env-file .env $(DOCKER_IMAGE_NAME); \
    )
	@echo "--------------| local_docker_run command is completed |---------------";

docker_run:
	@echo "--------------| docker_run command is started |---------------";
	( \
		docker run -d -p 5000:5000 --env-file .env $(DOCKER_IMAGE_NAME); \
	)
	@echo "--------------| docker_run command is completed |---------------";

docker_clean:
	@echo "--------------| docker_clean command is started |---------------";
	$(eval DOCKER_EXISTS = $(shell docker ps --filter ancestor=$(DOCKER_IMAGE_NAME) -q))
	$(eval IMAGE_EXISTS = $(shell docker images $(DOCKER_IMAGE_NAME) -a -q))
	$(if $(strip $(DOCKER_EXISTS)),docker stop `docker ps --filter ancestor=$(DOCKER_IMAGE_NAME) -q`, \
	@echo '--------- Container of $(DOCKER_IMAGE_NAME) image not exists.')
	$(if $(strip $(DOCKER_EXISTS)),docker rm `docker ps -a --filter ancestor=$(DOCKER_IMAGE_NAME) -q`, \
	@echo '--------- Container of $(DOCKER_IMAGE_NAME) image not exists.')
	$(if $(strip $(IMAGE_EXISTS)),docker rmi `docker images $(DOCKER_IMAGE_NAME) -a -q` --force, \
	@echo '--------- $(DOCKER_IMAGE_NAME) image not exists')
	@echo "--------------| docker_clean command is completed |---------------";

clean: docker_clean
	rm -rf $(VIRTUAL_ENV)
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete