#!/bin/bash

set -e

cd /app

python smallgames.py | grep -i ECO
