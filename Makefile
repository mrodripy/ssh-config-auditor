.PHONY: help build test audit clean

# Colores para mejor visualización
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m

help: ## Muestra esta ayuda
	@echo "SSH Configuration Auditor - Comandos disponibles:"
	@echo ""
	@echo "$(YELLOW)USO:$(NC) make [comando]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Construye la imagen Docker
	@echo "$(YELLOW)[+] Construyendo imagen Docker...$(NC)"
	docker build -t ssh-auditor:latest .

run: build ## Ejecuta el auditor con ayuda (muestra opciones)
	@echo "$(YELLOW)[+] Ejecutando ayuda del auditor...$(NC)"
	docker run --rm ssh-auditor:latest --help

test: build ## Prueba con archivo de muestra insecure_sshd_config
	@echo "$(YELLOW)[+] Ejecutando prueba con archivo de muestra...$(NC)"
	docker run --rm -v $(PWD)/samples:/data ssh-auditor:latest /data/insecure_sshd_config

audit: build ## Audita la configuración SSH del sistema local (Linux)
	@echo "$(YELLOW)[+] Auditando configuración SSH del sistema...$(NC)"
	docker run --rm -v /etc/ssh:/data:ro ssh-auditor:latest /data/sshd_config

audit-file: build ## Audita un archivo específico (usa: make audit-file FILE=mi_config.conf)
	@if [ -z "$(FILE)" ]; then \
		echo "$(YELLOW)[!] Especifica un archivo: make audit-file FILE=ruta/a/config.conf$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)[+] Auditando $(FILE)...$(NC)"
	docker run --rm -v $(PWD):/data ssh-auditor:latest /data/$(FILE)

json-report: build ## Genera reporte JSON del archivo de muestra
	@echo "$(YELLOW)[+] Generando reporte JSON...$(NC)"
	@mkdir -p reports
	docker run --rm \
		-v $(PWD)/samples:/data:ro \
		-v $(PWD)/reports:/reports \
		ssh-auditor:latest \
		/data/insecure_sshd_config \
		-o json \
		-f /reports/audit_$$(date +%Y%m%d_%H%M%S).json
	@echo "Reporte guardado en: reports/audit_*.json"

clean: ## Elimina la imagen Docker local
	@echo "$(YELLOW)[+] Limpiando imagen Docker...$(NC)"
	docker rmi ssh-auditor:latest 2>/dev/null || true

version: ## Muestra versión de Docker y del auditor
	@echo "$(YELLOW)[+] Docker version:$(NC)"
	@docker --version
	@echo "$(YELLOW)[+] Auditor info:$(NC)"
	@docker run --rm ssh-auditor:latest --help | head -5

.DEFAULT_GOAL := help
