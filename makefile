# https://gist.github.com/miguelmota/c13bd2f5cc5493c82689c40117846571
# Windows		:	mingw32-make
# linux/macOS	:	make
.phony: ecr-login

IMG_NAME = testapp
MAP_PORT = 5000
CONTAINER_ID:=


##################################
# aws ecr deployment
##################################

PROFILE = lablearner
AWS_REGION := us-east-1
ECR_REPO_NAME := testecr
IMAGE_TAG := v1

# No change
AWS_ACCOUNT_ID=$(shell aws sts get-caller-identity --query Account --output text --profile $(PROFILE))
REG=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
REPO=$(REG)/$(ECR_REPO_NAME)

help:
	@echo "Get help"

# Login to ECR - Not working now for some reason -> do a separate command
ecr-login: 
	aws ecr get-login-password --region $(AWS_REGION) --profile $(PROFILE) | docker login --username AWS --password-stdin $(REG)

# Build and tag docker image
ecr-build:
	docker build -f Dockerfile --no-cache -t $(REPO):$(IMAGE_TAG) .

# Push docker image ecr-login
ecr-push: 
	docker push $(REPO):$(IMAGE_TAG)


##################################
# Local deployment
##################################

local-build:
	docker build -f Dockerfile --no-cache -t $(IMG_NAME) .
local-run:
	docker run -p $(MAP_PORT):$(MAP_PORT) -it $(IMG_NAME)
local-check:
	docker exec -it $(CONTAINER_ID) sh

clean-all:
	docker stop $(shell docker ps -aq)
	docker rm -f $(shell docker ps -aq)
	docker rmi -f $(shell docker images -aq)
	docker system prune -a --force
	docker network prune --force
	docker volume prune --force
	docker container prune --force
	docker image prune --force

clean-others:
	docker network prune --force
	docker volume rm $(shell docker volume ls -q -f dangling=true)
	docker volume prune --force

clean-container:
	docker stop $(shell docker ps -aq)
	docker rm -f $(shell docker ps -aq)
	docker container prune --force

clean-images:
	docker rmi -f $(shell docker images -aq)

