# Makefile

.PHONY: all req lint format clean

# Variables
PIP := pip
RUFF := ruff

all: req lint format clean ## Run all tasks


req: ## Install the requirements
	$(PIP) install -r requirements.txt

lint: ## Run linter (ruff)
	$(RUFF) check .

format: ## Run code formatter (ruff)
	$(RUFF) check . --fix

clean: ## Clean up generated files
	rm -rf __pycache__
