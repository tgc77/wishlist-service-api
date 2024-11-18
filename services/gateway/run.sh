#!/bin/bash

export PYTHONPATH=../../$(pwd)

fastapi dev main.py --port 8080