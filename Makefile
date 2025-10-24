# Makefile para Sistema de Noticias con IA
# Comandos rápidos para desarrollo

.PHONY: help install dev test clean docker-up docker-down

# Variables
PYTHON := python3
PIP := pip3
NPM := npm

# Color output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "========================================="
	@echo "  Sistema de Noticias con IA - Comandos"
	@echo "========================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${GREEN}%-20s${NC} %s\n", $$1, $$2}'
	@echo ""

install: ## Instalar todas las dependencias
	@echo "${GREEN}Instalando dependencias del backend...${NC}"
	cd backend && $(PYTHON) -m venv venv && . venv/bin/activate && $(PIP) install -r requirements.txt
	@echo "${GREEN}Instalando dependencias del frontend...${NC}"
	cd frontend && $(NPM) install
	@echo "${GREEN}✓ Instalación completada${NC}"

dev-backend: ## Ejecutar backend en modo desarrollo
	@echo "${GREEN}Iniciando backend FastAPI...${NC}"
	cd backend && . venv/bin/activate && uvicorn main:app --reload

dev-frontend: ## Ejecutar frontend en modo desarrollo
	@echo "${GREEN}Iniciando frontend React...${NC}"
	cd frontend && $(NPM) run dev

dev: ## Ejecutar backend y frontend simultáneamente (requiere tmux)
	@echo "${GREEN}Iniciando servidores...${NC}"
	tmux new-session -d -s noticias-ia 'cd backend && . venv/bin/activate && uvicorn main:app --reload' \; \
		split-window -h 'cd frontend && npm run dev' \; \
		attach

test-backend: ## Ejecutar tests del backend
	@echo "${GREEN}Ejecutando tests del backend...${NC}"
	cd backend && . venv/bin/activate && pytest -v

test-frontend: ## Ejecutar tests del frontend
	@echo "${GREEN}Ejecutando tests del frontend...${NC}"
	cd frontend && $(NPM) test

test: test-backend test-frontend ## Ejecutar todos los tests

lint-backend: ## Linter para Python
	@echo "${GREEN}Ejecutando linter Python...${NC}"
	cd backend && . venv/bin/activate && flake8 . --exclude=venv

lint-frontend: ## Linter para JavaScript
	@echo "${GREEN}Ejecutando linter JavaScript...${NC}"
	cd frontend && $(NPM) run lint

lint: lint-backend lint-frontend ## Ejecutar todos los linters

format-backend: ## Formatear código Python con black
	@echo "${GREEN}Formateando código Python...${NC}"
	cd backend && . venv/bin/activate && black .

format-frontend: ## Formatear código JavaScript con prettier
	@echo "${GREEN}Formateando código JavaScript...${NC}"
	cd frontend && $(NPM) run format

format: format-backend format-frontend ## Formatear todo el código

clean: ## Limpiar archivos temporales y cache
	@echo "${YELLOW}Limpiando archivos temporales...${NC}"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	cd frontend && rm -rf node_modules dist 2>/dev/null || true
	@echo "${GREEN}✓ Limpieza completada${NC}"

docker-build: ## Construir imágenes Docker
	@echo "${GREEN}Construyendo imágenes Docker...${NC}"
	docker-compose build

docker-up: ## Iniciar contenedores Docker
	@echo "${GREEN}Iniciando contenedores...${NC}"
	docker-compose up -d
	@echo "${GREEN}✓ Contenedores iniciados${NC}"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

docker-down: ## Detener contenedores Docker
	@echo "${YELLOW}Deteniendo contenedores...${NC}"
	docker-compose down

docker-logs: ## Ver logs de contenedores
	docker-compose logs -f

docker-restart: docker-down docker-up ## Reiniciar contenedores

seed-data: ## Cargar datos de ejemplo
	@echo "${GREEN}Cargando datos de ejemplo...${NC}"
	curl -X POST http://localhost:8000/api/noticias/seed
	@echo "\n${GREEN}✓ Datos cargados${NC}"

health-check: ## Verificar estado de los servicios
	@echo "${GREEN}Verificando servicios...${NC}"
	@curl -s http://localhost:8000/health | python -m json.tool
	@echo "${GREEN}✓ Backend funcionando${NC}"

backup: ## Crear backup del proyecto (sin node_modules y venv)
	@echo "${GREEN}Creando backup...${NC}"
	tar -czf backup-$$(date +%Y%m%d-%H%M%S).tar.gz \
		--exclude='node_modules' \
		--exclude='venv' \
		--exclude='__pycache__' \
		--exclude='.git' \
		.
	@echo "${GREEN}✓ Backup creado${NC}"

# Comandos de desarrollo rápido
quick-start: install dev ## Instalación e inicio rápido

deploy-prod: ## Deploy a producción (requiere configuración)
	@echo "${YELLOW}Desplegando a producción...${NC}"
	docker-compose -f docker-compose.prod.yml up -d --build
	@echo "${GREEN}✓ Deploy completado${NC}"

.DEFAULT_GOAL := help