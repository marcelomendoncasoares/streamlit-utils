install:
	pip install -e .[dev]
	pre-commit install

test:
	pytest -vv --cov

run:
	streamlit run .\_local_test_streamlit.py --server.headless true

.PHONY: install test run
