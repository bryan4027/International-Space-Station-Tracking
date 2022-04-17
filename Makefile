all: build run push

images:
	docker images | grep bryan4027
ps:
	docker ps -a | grep bryan4027
build:
	docker build -t bryan4027/iss_tracking10:1.3 .
run:
	docker run --name "iss_tracking10" -it -p 5001:5000 bryan4027/iss_tracking10:1.3
push:
	docker push bryan4027/iss_tracking0:1.3	
