NAME = pac-man.py

.PHONY: all install run debug lint clean

all: install

install:
	pip install -r requirements.txt || pip install flake8 mypy pytest

run:
	python3 $(NAME) config.json

debug:
	python3 -m pdb $(NAME) config.json

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

clean:
	rm -rf __pycache__ */__pycache__ .mypy_cache .pytest_cache
