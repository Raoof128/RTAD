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
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black .
