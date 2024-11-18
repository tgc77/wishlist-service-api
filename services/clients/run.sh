#!/bin/sh

export PYTHONPATH=../../$(pwd)

fastapi dev main.py --port 8000