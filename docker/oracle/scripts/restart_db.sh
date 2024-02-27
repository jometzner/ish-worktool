#!/bin/sh

sqlplus -s /nolog <<EOF
-- restart database
connect sys/intershop as sysdba
 
shutdown immediate
startup
quit
EOF
