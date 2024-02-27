#!/bin/bash

dbca -silent -createDatabase -gdbName XE \
    -templateName XE_Database.dbc \
    -createAsContainerDatabase false \
    -sid XE \
    -emConfiguration DBEXPRESS \
    -emExpressPort 5500 \
    -J-Doracle.assistants.dbca.validate.DBCredentials=false \
    -sampleSchema false \
    -automaticMemoryManagement false \
    -initParams memory_target='0M',sga_target='2G',pga_aggregate_target='0M',pga_aggregate_limit='0M' \
    -storageType FS \
    -datafileDestination /opt/oracle/oradata \
    -useOMF false \
    -enableArchive false \
    -systemPassword intershop \
    -sysPassword intershop \
    -recoveryAreaDestination NONE

installState=$?

if [ $installState -eq 0 ]; then
    /home/oracle/bin/drop_user.sh && /home/oracle/bin/prepare_db.sh && /home/oracle/bin/prepare_tablespaces.sh
    installState=$?
fi

exit $installState
