.PHONY: postgres redis

postgres:
	docker-compose up postgres pgadmin
redis:
	docker-compose up redis
