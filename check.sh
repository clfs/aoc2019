#!/bin/bash
echo "==> mypy <=="
mypy --strict .
echo "==> yapf <=="
yapf --recursive --diff .
echo "==> pylint <=="
pylint --disable=C0103,C0114,C0115,C0116,C0301 --score=no --jobs=0 *.py
