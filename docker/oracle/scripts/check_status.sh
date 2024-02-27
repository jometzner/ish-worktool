#!/bin/sh

RETVAL=`sqlplus -silent sys/intershop as sysdba <<EOF
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
SELECT INSTANCE_NAME, STATUS, DATABASE_STATUS FROM V$INSTANCE WHERE INSTANCE_NAME='XE' AND STATUS='OPEN';
EXIT;
EOF`

if [[ ! -z "$RETVAL" ]]; then
	exit 0
else
	ext 1
fi