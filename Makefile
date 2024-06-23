# Makefile

.PHONY: all req test lint format

# Variables
PIP := pip
RUFF := ruff

all: req lint format ## Run all tasks


req: ## Install the requirements
	$(PIP) install -r requirements.txt

lint: ## Run linter (ruff)
	$(RUFF) check .

format: ## Run code formatter (ruff)
	$(RUFF) check . --fix

clean: ## Clean up generated files
	rm -rf __pycache__
