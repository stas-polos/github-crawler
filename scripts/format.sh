#!/bin/bash
set -e
echo "mypy check:"
mypy --namespace-packages --explicit-package-bases src
echo "ruff formatter reformatting:"
ruff format src tests
echo "ruff linter reformatting:"
ruff check --fix src tests
