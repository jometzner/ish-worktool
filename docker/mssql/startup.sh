#!/bin/bash

trap 'ps -j -C sqlservr --no-headers | awk "{print \$1}" | xargs kill' INT TERM

/opt/mssql/bin/sqlservr &

wait
