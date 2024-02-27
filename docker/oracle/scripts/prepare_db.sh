#!/bin/bash -e

sqlplus -s /nolog <<EOF

-- Unlock the CTXSYS User
connect sys/intershop as sysdba

ALTER user ctxsys account unlock;
ALTER user ctxsys identified by ctxsys;

-- Grants with Grant Option for CTXSYS User and Lock CTXSYS Again
connect ctxsys/ctxsys;

GRANT EXECUTE ON CTX_DDL TO sys    WITH GRANT OPTION;
GRANT EXECUTE ON CTX_DDL TO system WITH GRANT OPTION;

connect sys/intershop as sysdba

ALTER user ctxsys account lock;

-- Increase open_cursors and processes and Disable sec_case_sensitive_logon
connect sys/intershop as sysdba

ALTER SYSTEM SET processes                = 180    scope = spfile;
ALTER SYSTEM SET open_cursors             = 500    scope = both;

show parameter processes
show parameter open_cursors

-- Set Default Password Security Profile Parameters to Unlimited Within 11gR2
ALTER profile DEFAULT limit FAILED_LOGIN_ATTEMPTS   UNLIMITED;
ALTER profile DEFAULT limit PASSWORD_GRACE_TIME     UNLIMITED;
ALTER profile DEFAULT limit PASSWORD_LIFE_TIME      UNLIMITED;
ALTER profile DEFAULT limit PASSWORD_LOCK_TIME      UNLIMITED;

-- Fix ORA-12012 error on auto execute of job SYS.ORA$AT_OS_OPT_SY_
EXEC dbms_stats.init_package();

quit
EOF

