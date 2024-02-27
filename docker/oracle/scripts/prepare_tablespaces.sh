#!/bin/sh

sqlplus -s /nolog <<EOF
-- Intershop IS_* Tablespaces
connect sys/intershop as sysdba

DEFINE _ts_temp     = IS_TEMP
DEFINE _ts_user     = IS_USERS
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

-- START: intershop
EXEC DBMS_XDB.SETLISTENERLOCALACCESS(FALSE);
ALTER DATABASE ADD LOGFILE GROUP 4 ('$ORACLE_BASE/oradata/$ORACLE_SID/redo04.log') SIZE 10m;
ALTER DATABASE ADD LOGFILE GROUP 5 ('$ORACLE_BASE/oradata/$ORACLE_SID/redo05.log') SIZE 10m;
ALTER SYSTEM SWITCH LOGFILE;
ALTER SYSTEM SWITCH LOGFILE;
ALTER SYSTEM CHECKPOINT;
ALTER DATABASE DROP LOGFILE GROUP 1;
ALTER DATABASE DROP LOGFILE GROUP 2;

ALTER SYSTEM SET db_recovery_file_dest='';

-- Shrink Temp / SYSTEM Tablespace
alter database tempfile '$ORACLE_BASE/oradata/XE/temp01.dbf' resize 20M;
alter database datafile '$ORACLE_BASE/oradata/XE/system01.dbf' resize 853M;


-- Remove XDB
shutdown immediate
startup upgrade;
start $ORACLE_HOME/rdbms/admin/catxdbdv.sql
start $ORACLE_HOME/rdbms/admin/dbmsmeta.sql
start $ORACLE_HOME/rdbms/admin/dbmsmeti.sql
start $ORACLE_HOME/rdbms/admin/dbmsmetu.sql
start $ORACLE_HOME/rdbms/admin/dbmsmetb.sql
start $ORACLE_HOME/rdbms/admin/dbmsmetd.sql
start $ORACLE_HOME/rdbms/admin/dbmsmet2.sql
start $ORACLE_HOME/rdbms/admin/catmeta.sql
start $ORACLE_HOME/rdbms/admin/prvtmeta.plb
start $ORACLE_HOME/rdbms/admin/prvtmeti.plb
start $ORACLE_HOME/rdbms/admin/prvtmetu.plb
start $ORACLE_HOME/rdbms/admin/prvtmetb.plb
start $ORACLE_HOME/rdbms/admin/prvtmetd.plb
start $ORACLE_HOME/rdbms/admin/prvtmet2.plb
start $ORACLE_HOME/rdbms/admin/catmet2.sql

-- Remove Text
--@$ORACLE_HOME/ctx/admin/catnoctx.sql
--drop procedure sys.validate_context;
--drop user MDSYS cascade;
--start $ORACLE_HOME/rdbms/admin/utlrp.sql

-- After removing TEXT and APEX from the DB we can remove it from the Home
host rm -rf $ORACLE_HOME/apex
--host rm -rf $ORACLE_HOME/ctx

-- Here we execute the shrink Script to reduce the SYSAUX TS
--@/home/oracle/bin/shrink_sysaux.sql
--shutdown immediate;
--startup;

-- Create a Smaller UNDO. We add a new one and drop the old
create undo tablespace undotbs2 datafile '$ORACLE_BASE/oradata/XE/undotbs2.dbf' size 1M autoextend on next 10M maxsize 1G;
alter system set undo_tablespace='undotbs2';
shutdown immediate;
startup
drop tablespace undotbs1 including contents and datafiles;
shutdown immediate;
startup;
-- END: intershop

quit
EOF
