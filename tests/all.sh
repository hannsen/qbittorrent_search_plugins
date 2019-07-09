#!/bin/bash

set -e

cd /app

echo TEST ali213
python ali213.py | grep -e ark -e survival

#offline
#python demonoid.py | grep drive

echo TEST smallgames
python smallgames.py | grep ECO

#offline
#python threedm.py | grep Handball
