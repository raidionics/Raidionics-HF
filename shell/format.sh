#!/bin/bash
isort --sl src/ app.py
black --line-length 80 src/ app.py
flake8 src/ app.py
