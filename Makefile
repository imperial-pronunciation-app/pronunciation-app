test:
	docker-compose --profile test up --build --abort-on-container-exit
dev:
	docker-compose --profile dev up --build
down:
	docker-compose down