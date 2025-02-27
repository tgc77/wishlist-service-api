
build-up-api:
	docker compose up --build

run-the-app-local:
	$(MAKE) run-api-clients
	$(MAKE) run-api-products
	$(MAKE) run-api-favorite-products
	$(MAKE) run-api-gateway

run-api-gateway:
	fastapi dev services/gateway/main.py --port 8080
	
run-api-clients:
	fastapi dev services/clients/main.py --port 8000

run-api-products: 
	fastapi dev services/products/main.py --port 8001

run-api-favorite-products: 
	fastapi dev service/favorite_products/main.py --port 8002

.PHONY: build-api run-all