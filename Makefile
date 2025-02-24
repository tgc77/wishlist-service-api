
build-up-api:
	docker compose up --build

run-all: run-api-clients run-api-products run-api-favorite-products run-api-gateway

run-api-gateway:
	fastapi dev services/gateway/main.py --port 8080
	
run-api-clients: run-api-gateway
	fastapi dev services/clients/main.py --port 8000

run-api-products: run-api-gateway
	fastapi dev services/products/main.py --port 8001

run-api-favorite-products: run-api-gateway
	fastapi dev service/favorite_products/main.py --port 8002

.PHONY: build-api run-all