.DEFAULT_GOAL := run

run:
		uvicorn app.main:app --reload
		
setup:
		python3 -m venv venv
		. venv/bin/activate
		pip install -r requirements.txt