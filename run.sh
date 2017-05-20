#!/usr/bin/env bash

virtualenv .

source bin/activate

pip install -r packages.txt

python src/Main.py
