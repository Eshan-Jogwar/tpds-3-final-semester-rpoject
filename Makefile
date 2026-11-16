# ====================================================================
# CampusPulse: Makefile for Single-Command Docker Orchestration
# Course: TPDS-III (5th Semester CSD)
# ====================================================================

.DEFAULT_GOAL := help

APP_NAME := campuspulse-app
PORT := 5000

.PHONY: help
help: ## Show available commands
	@echo "CampusPulse Container Orchestration"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: up
up: ## Build and start the application in Docker (single command)
	@echo "==> Building and launching CampusPulse container..."
	docker compose up --build -d
	@echo "==> Waiting for container healthcheck..."
	@sleep 2
	@echo "==> CampusPulse is running!"
	@echo "    Student Portal:   http://localhost:$(PORT)/index.html"
	@echo "    Work Orders:      http://localhost:$(PORT)/admin.html"
	@echo "    Analytics:        http://localhost:$(PORT)/analytics.html"
	@echo "    API Healthcheck:  http://localhost:$(PORT)/api/v1/health"

.PHONY: run
run: up ## Alias for 'make up'

.PHONY: down
down: ## Stop and remove running containers
	@echo "==> Stopping CampusPulse container..."
	docker compose down

.PHONY: stop
stop: down ## Alias for 'make down'

.PHONY: restart
restart: ## Restart running containers
	@echo "==> Restarting CampusPulse..."
	docker compose restart

.PHONY: logs
logs: ## Stream container logs in real time
	docker compose logs -f

.PHONY: status
status: ## Show running container status
	docker compose ps

.PHONY: test
test: ## Test the running container endpoint health and data response
	@echo "==> Testing container healthcheck endpoint..."
	@curl -sSf http://localhost:$(PORT)/api/v1/health | grep -q "healthy" && echo "✔ Healthcheck endpoint OK" || (echo "✖ Healthcheck failed" && exit 1)
	@echo "==> Testing facilities API endpoint..."
	@curl -sSf http://localhost:$(PORT)/api/v1/facilities | grep -q "success" && echo "✔ Facilities endpoint OK" || (echo "✖ Facilities failed" && exit 1)
	@echo "==> Testing analytics KPIs API endpoint..."
	@curl -sSf http://localhost:$(PORT)/api/v1/analytics/kpis | grep -q "total_tickets" && echo "✔ Analytics KPIs endpoint OK" || (echo "✖ Analytics failed" && exit 1)
	@echo "==> All container verification checks passed successfully!"

.PHONY: clean
clean: ## Stop container and purge persistent data volume
	@echo "==> Purging containers and volumes..."
	docker compose down -v
	@echo "==> Clean complete."
