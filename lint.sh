#!/usr/bin/env bash

# run format
black .

# run pylint
pylint .

# run mypy
mypy .
