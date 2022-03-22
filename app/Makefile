NAME ?= rhodgesd


all: build run

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/iss_app:latest .

run:
	docker run --name  "iss_app_rhodges" -d -p 5011:5000 rhodgesd/iss_app:latest



