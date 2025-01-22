test:
	sudo docker-compose --profile test up --build --abort-on-container-exit
dev:
	docker-compose --profile dev up --build