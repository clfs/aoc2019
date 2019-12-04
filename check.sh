#!/bin/bash
echo "==> mypy <=="
mypy .
echo "==> yapf <=="
yapf --recursive --diff .
echo "==> pylint <=="
pylint --disable=C0103,C0114,C0115,C0116 --score=no --jobs=0 *.py
