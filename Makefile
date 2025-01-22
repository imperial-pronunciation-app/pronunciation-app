test:
	sudo docker-compose --profile test up --build --abort-on-container-exit
dev:
	sudo docker-compose --profile dev up --build
down:
	sudo docker-compose down