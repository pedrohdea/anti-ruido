# Anti-Ruído — protótipo. `make` sobe o app local em http://localhost:8686
#
# Dependências de sistema: python3 (3.10+), ffmpeg
#   Ubuntu/Debian: sudo apt install python3 python3-venv ffmpeg
#   macOS:         brew install python ffmpeg

VENV := .venv
PY   := $(VENV)/bin/python

.PHONY: all run setup demo test clean

all: setup run

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PY) -m pip install --upgrade pip

setup: $(VENV)/bin/activate
	$(PY) -m pip install -q -r requirements.txt flask flask-cors

run:
	$(PY) app/server.py

demo: setup
	$(PY) -m anti_ruido.cli demo

test: setup
	$(PY) -m unittest discover -s tests -t . -v

clean:
	rm -rf $(VENV) app/data demo-out
