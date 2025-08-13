#!/bin/bash

source "$(dirname "$0")/.venv/bin/activate"

python3 create_tables.py

sleep 1

python3 insert_data.py
