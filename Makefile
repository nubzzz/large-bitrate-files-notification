.PHONY: all

TAG=$(shell git rev-parse HEAD | head -c8)

build:
		export TAG=$(TAG) && \
		docker-compose build --no-cache

up:
		docker-compose up

down:
		docker-compose down

push:
		export TAG=$(TAG) && \
		docker-compose push

all: build push
