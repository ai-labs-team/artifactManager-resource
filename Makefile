DOCKER_NAME=artifact-manager-resource
DOCKER_REPO=lukaszz/${DOCKER_NAME}
DOCKER_VERSION=0.0.6

all:
	@pip freeze > requirements.txt
	@docker build . -t ${DOCKER_REPO}:${DOCKER_VERSION}
	@docker push ${DOCKER_REPO}:${DOCKER_VERSION}

test:
	@cd src; pytest;
