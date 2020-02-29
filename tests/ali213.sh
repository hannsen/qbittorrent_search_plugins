#!/bin/bash

set -e

cd /app

python ali213.py | grep -i -e ark -e survival
