.PHONY: install run test clean lint

install:
	pip install -r requirements.txt

run:
	streamlit run app.py

test:
	python3 -m unittest discover tests

clean:
	rm -rf __pycache__
	rm -rf utils/__pycache__
	rm -rf tests/__pycache__
	rm -rf production_data/*
	rm -rf secure_backups/*
	touch production_data/.gitkeep
	touch secure_backups/.gitkeep
	rm -f incident_log.json
	rm -f ransomware.key

lint:
	# Placeholder for linting command if user installs flake8/black
	@echo "Running syntax check..."
	python3 -m py_compile app.py utils/*.py
