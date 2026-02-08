
# Makefile for Lega project

# Python configuration
# On Windows, 'py' is the recommended launcher for multiple versions.
PYTHON ?= py
VENV = .venv

# Detect OS for pathing
ifeq ($(OS),Windows_NT)
    VENV_BIN = $(VENV)\Scripts
    RM = rd /s /q
else
    VENV_BIN = $(VENV)/bin
    RM = rm -rf
endif

VENV_PYTHON = $(VENV_BIN)\python
VENV_PIP = $(VENV_BIN)\pip

.PHONY: help venv install run start clean

# Default goal
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make venv     - Create a virtual environment"
	@echo "  make install  - Install backend and frontend dependencies"
	@echo "  make run      - Run backend and frontend concurrently"
	@echo "  make start    - Create venv, install deps, and run"
	@echo "  make clean    - Remove build artifacts and venv"

# Create virtual environment
$(VENV):
	@echo "Creating virtual environment using $(PYTHON)..."
	$(PYTHON) -m venv $(VENV)

venv: $(VENV)

# Install dependencies
install: $(VENV)
	@echo "Installing backend dependencies..."
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd lega && npm install

# Run both backend and frontend concurrently
run:
	@echo "Starting backend and frontend..."
	# Using npx concurrently to run both processes in parallel
	npx -y concurrently -k -p "[{name}]" -n "BACKEND,FRONTEND" -c "blue.bold,green.bold" \
		"$(VENV_PYTHON) app.py" \
		"cd lega && npm run dev"

# Convenience target to setup and run
start: install run

# Clean up build artifacts and venv
clean:
	@echo "Cleaning up..."
	@if exist $(VENV) $(RM) $(VENV)
	@if exist __pycache__ $(RM) __pycache__
	@if exist lega\.next $(RM) lega\.next
