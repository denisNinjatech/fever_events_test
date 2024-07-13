.PHONY: venv install migrate celery_worker celery_beat run all

# Detect OS
UNAME := $(shell uname)

# Define commands based on OS
ifeq ($(UNAME), Linux)
	ACTIVATE = source venv/bin/activate
else ifeq ($(UNAME), Darwin)
	ACTIVATE = source venv/bin/activate
else ifeq ($(UNAME), MINGW32_NT)
	ACTIVATE = venv\Scripts\activate
else ifeq ($(UNAME), MINGW64_NT)
	ACTIVATE = venv\Scripts\activate
else ifeq ($(OS), Windows_NT)
	ACTIVATE = venv\Scripts\activate
else
	$(error Unsupported OS)
endif

venv:
	@echo "Setting up virtual environment..."
	python -m venv venv

env-setup:venv
	@echo "Setting up virtual environment, installing dependencies, running migrations..."
	$(ACTIVATE) && pip install -r requirements.txt

migration:
	$(ACTIVATE) && python migrations.py

celery-worker:
	@echo "starting Celery worker..."
	$(ACTIVATE) && celery -A fever_event worker --pool=solo -l info

celery-beat:
	@echo "starting Celery beat..."
	$(ACTIVATE) && celery -A fever_event beat --loglevel=info
	
api:
	@echo "starting FastAPI application..."
	$(ACTIVATE) && uvicorn fever_event.main:app --reload