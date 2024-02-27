#!/bin/bash -e

set -x

sqlplus -s /nolog <<EOF

-- Unlock the CTXSYS User
connect sys/intershop as sysdba

DROP USER oracle_ocm CASCADE;
DROP USER dbsnmp CASCADE;

DROP USER OLAPSYS CASCADE;
DELETE FROM sys.exppkgact$ WHERE package = 'DBMS_CUBE_EXP' AND schema= 'SYS';
DELETE FROM sys.exppkgact$ WHERE package = 'DBMS_AW_EXP'  AND schema= 'SYS';
COMMIT;

begin
  for rec in (
    SELECT object_name FROM dba_objects
    WHERE status <> 'VALID'
     AND object_type = 'SYNONYM'
     AND (object_name LIKE 'ALL_OLAP2%' OR object_name LIKE 'ALL_AW%')
  )
  loop
     execute immediate 'DROP PUBLIC SYNONYM "'||rec.object_name||'"';
  end loop;
end;
/

DROP USER ORDSYS CASCADE;
DROP USER ORDPLUGINS CASCADE;
DROP USER SI_INFORMTN_SCHEMA CASCADE;
DROP USER ORDDATA CASCADE;
COMMIT;

begin
  for rec in (
    SELECT object_name FROM dba_objects
    WHERE status <> 'VALID'
     AND object_type = 'JAVA CLASS'
     AND owner = 'MDSYS'
  )
  loop
     execute immediate 'DROP JAVA CLASS mdsys."'||rec.object_name||'"';
  end loop;
end;
/

begin
  for rec in (
    SELECT synonym_name
    FROM dba_synonyms
    WHERE table_owner = 'MDSYS'
  )
  loop
     execute immediate 'DROP PUBLIC SYNONYM "'||rec.synonym_name||'"';
  end loop;
end;
/

DROP USER GSMCATUSER CASCADE;
DROP USER GSMUSER CASCADE;

DROP USER lbacsys CASCADE;
@$ORACLE_HOME/rdbms/admin/dvremov

DROP USER mddata CASCADE;
@$ORACLE_HOME/md/admin/semremov.sql
COMMIT;

DROP USER appqossys CASCADE;
DROP USER dip CASCADE;
DROP USER ggsys CASCADE;

begin
  for rec in (
    SELECT object_name FROM dba_objects
    WHERE status <> 'VALID'
     AND object_type = 'SYNONYM'
     AND object_name like 'WLM%'
  )
  loop
     execute immediate 'DROP PUBLIC SYNONYM "'||rec.object_name||'"';
  end loop;
end;
/

start @$ORACLE_HOME/rdbms/admin/owmuinst.plb
start @$ORACLE_HOME/olap/admin/catnoaps.sql
start @$ORACLE_HOME/olap/admin/olapidrp.plb
start @$ORACLE_HOME/olap/admin/catnoxoq.sql

shutdown immediate;
startup
DROP USER mdsys CASCADE;

begin
  for rec in (
    SELECT object_type||' '||owner||'."'||object_name||'"' AS obj_name FROM dba_objects
    WHERE status <> 'VALID'
     AND owner IN ('SYS')
  )
  loop
     execute immediate 'DROP PUBLIC SYNONYM "'||rec.obj_name||'"';
  end loop;
end;
/

start @$ORACLE_HOME/rdbms/admin/catdph.sql
start @$ORACLE_HOME/rdbms/admin/prvtcxml.plb
start @$ORACLE_HOME/rdbms/admin/catdpb.sql
start @$ORACLE_HOME/rdbms/admin/dbmspump.sql
start @$ORACLE_HOME/rdbms/admin/utlrp.sql

quit
EOF