NAME = pac-man.py
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: all install run debug lint clean venv shell lint-strict build

all: install

venv:
	test -d $(VENV) || python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

run: venv
	$(PYTHON) $(NAME) config.json

build: venv
	$(PYTHON) -m PyInstaller --noconfirm --clean PacMan.spec

debug: venv
	$(PYTHON) -m pdb $(NAME) config.json

lint: venv
	$(VENV)/bin/flake8 --exclude=.venv,venv,__pycache__ .
	$(VENV)/bin/mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude '^\.venv/' .

lint-strict: venv
	$(VENV)/bin/flake8 --exclude=.venv,venv,__pycache__ .
	$(VENV)/bin/mypy --strict --exclude '^\.venv/' .

clean:
	rm -rf __pycache__ */__pycache__ .mypy_cache .pytest_cache $(VENV)

shell: venv
	bash --rcfile $(VENV)/bin/activate
