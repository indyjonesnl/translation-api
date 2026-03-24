.PHONY: build up down start stop help ps logs

build:
	docker build -t translate-api .

start:
	docker compose start

stop:
	docker compose stop

up:
	docker compose up -d

down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f

test:
	curl -X POST http://localhost:8000/translate \
    -H "Content-Type: application/json" \
    -d '{"app.main.button_header": "Clicking this button will persist the advertisement."}'