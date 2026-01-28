#!/bin/bash

rm -rf .venv || true


python3 -m venv .venv
source .venv/bin/activate

pip install "git+https://github.com/cicorias/azure-ai-content-understanding-python-1.git@make-pip-install-friendly"

# pip install -e /home/cicorias/g/learn/genai/ms/src/azure-ai-content-understanding-python
