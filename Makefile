.PHONY: help build test run clean

# Default target
help:
	@echo "Available targets:"
	@echo "  setup     - Create virtual environment and install dependencies using uv"
	@echo "  setup-dev - Create virtual environment and install dependencies and dev-dependencies using uv"
	@echo "  build     - Builds the project using uv"
	@echo "  test      - Run the test suite"
	@echo "  run       - Run the decayCulator app"
	@echo "  clean     - Remove virtual environment and __pycache__"


setup:
	uv venv
	uv sync

setup-dev:
	make setup
	uv sync --dev

build:
	. uv pip install -e . && echo "✅ Build complete."

test:
	. .venv/bin/activate && pytest

run:
	. .venv/bin/activate && python decayculator/ui/app.py

clean:
	rm -rf .venv
	find . -type d -name '__pycache__' -exec rm -r {} +
