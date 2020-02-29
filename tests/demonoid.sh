#!/bin/bash

set -e

cd /app

python demonoid.py | grep drive
