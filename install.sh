#!/bin/sh
#
#

set -e
find . -name "dist" -type d -exec rm -f {} \;
pip3 install --user uv
uv build
pip3 install --user dist/*.whl
