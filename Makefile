.PHONY: test run finch-build sam-build clean help

help:
	@echo "VayuRakshak AI - Build & Run Utility"
	@echo "Author: Bhomesh Razdan (Lead Architect)"
	@echo "Commands:"
	@echo "  make test        - Run Python test suite"
	@echo "  make run         - Launch local REST API & Command Center on port 8080"
	@echo "  make finch-build - Build OCI container using AWS Finch"
	@echo "  make sam-validate- Validate SAM serverless template"

test:
	python3 -m unittest discover tests

run:
	python3 -m src.server 8080

finch-build:
	finch build -f aws/finch/Containerfile -t vayurakshak-ai:latest .

sam-validate:
	sam validate -t aws/template.yaml

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
