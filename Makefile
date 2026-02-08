
# Makefile for Lega project

# Python virtual environment (optional/recommended practice)
# Assumes 'python' and 'pip' are available in PATH.

.PHONY: help install run start clean

# Default goal
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make install  - Install backend and frontend dependencies"
	@echo "  make run      - Run backend and frontend concurrently"
	@echo "  make start    - Install dependencies and then run"
	@echo "  make clean    - Remove build artifacts"

# Install dependencies for both backend and frontend
install:
	@echo "Installing backend dependencies..."
	pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd lega && npm install

# Run both backend and frontend concurrently
run:
	@echo "Starting backend and frontend..."
	# Using npx concurrently to run both processes in parallel
	# The -y flag ensures npx installs concurrently without prompting if missing
	npx -y concurrently -k -p "[{name}]" -n "BACKEND,FRONTEND" -c "blue.bold,green.bold" \
		"python app.py" \
		"cd lega && npm run dev"

# Convenience target to install and then run
start: install run

# Clean up build artifacts (optional)
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf lega/.next
