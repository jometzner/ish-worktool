#!/bin/sh

RETVAL=`sqlplus -silent sys/intershop as sysdba <<EOF
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
select USERNAME from all_users where USERNAME='INTERSHOP';
EXIT;
EOF`

if [[ ! -z "$RETVAL" ]]; then
  echo "User INTERSHOP still exists"
else
  sqlplus -s /nolog <<EOF
  -- Intershop Database User
  connect sys/intershop as sysdba

  DEFINE _us         = intershop
  DEFINE _pw         = intershop
  DEFINE _ts_temp    = IS_TEMP
  DEFINE _ts_user    = IS_USERS

  DEFINE _ts_indx     = IS_INDX
  DEFINE _ts_indx_ctx = IS_INDX_CTX
  DEFINE _ts_size     = 100M
  DEFINE _uni_size    = 2M
  DEFINE _sys_ts      = SYSTEM

  -- Determine the file system path for the system tablespace and
  -- create the Intershop tablespace files within this location.

  COL system_ts_path NEW_VALUE path
  SELECT regexp_substr(df.name, '^(.*)[\\/]') AS system_ts_path
  FROM v\$tablespace ts
  JOIN v\$datafile df ON (df.ts#=ts.ts#)
  WHERE UPPER(ts.name) = '&_sys_ts';

  CREATE TEMPORARY TABLESPACE &_ts_temp TEMPFILE '&path.&_ts_temp._01.dbf'
  SIZE &_ts_size AUTOEXTEND ON NEXT &_ts_size MAXSIZE UNLIMITED
  EXTENT MANAGEMENT LOCAL UNIFORM SIZE &_uni_size;

  CREATE TABLESPACE &_ts_user DATAFILE '&path.&_ts_user._01.dbf'
  SIZE &_ts_size AUTOEXTEND ON NEXT &_ts_size MAXSIZE UNLIMITED
  EXTENT MANAGEMENT LOCAL SEGMENT SPACE MANAGEMENT AUTO;

  CREATE TABLESPACE &_ts_indx DATAFILE '&path.&_ts_indx._01.dbf'
  SIZE &_ts_size AUTOEXTEND ON NEXT &_ts_size MAXSIZE UNLIMITED
  EXTENT MANAGEMENT LOCAL SEGMENT SPACE MANAGEMENT AUTO;

  CREATE TABLESPACE &_ts_indx_ctx DATAFILE '&path.&_ts_indx_ctx._01.dbf'
  SIZE &_ts_size AUTOEXTEND ON NEXT &_ts_size MAXSIZE UNLIMITED
  EXTENT MANAGEMENT LOCAL SEGMENT SPACE MANAGEMENT AUTO;

  CREATE USER &_us
    IDENTIFIED BY &_pw
    DEFAULT TABLESPACE &_ts_user
    TEMPORARY TABLESPACE &_ts_temp
    PROFILE DEFAULT ACCOUNT UNLOCK;

  ALTER USER &_us DEFAULT ROLE ALL;

  GRANT CONNECT                       TO &_us;
  GRANT RESOURCE                      TO &_us;
  GRANT CTXAPP                        TO &_us;
  GRANT UNLIMITED TABLESPACE          TO &_us;
  GRANT CREATE CLUSTER                TO &_us;
  GRANT CREATE DATABASE LINK          TO &_us;
  GRANT CREATE SEQUENCE               TO &_us;
  GRANT CREATE SYNONYM                TO &_us;
  GRANT CREATE TABLE                  TO &_us;
  GRANT CREATE VIEW                   TO &_us;
  GRANT CREATE PROCEDURE              TO &_us;
  GRANT CREATE TRIGGER                TO &_us;
  GRANT CREATE TYPE                   TO &_us;
  GRANT CREATE SNAPSHOT               TO &_us;
  GRANT ANALYZE ANY                   TO &_us;
  GRANT EXECUTE ON CTX_DDL            TO &_us;
  GRANT EXECUTE ON DBMS_STREAMS_ADM   TO &_us;

  quit
EOF

fi
