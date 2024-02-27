#!/bin/bash

lsnrctl status
export  lsstatus=$?

if [ $lsstatus -gt 0 ]; then
  netca /orahome $ORACLE_HOME \
        /instype typical \
        /inscomp client,oraclenet,javavm,server,ano \
        /insprtcl tcp /cfg local /authadp NO_VALUE \
        /responseFile $ORACLE_HOME/network/install/netca_typ.rsp \
        /silent \
        /listenerparameters DEFAULT_SERVICE=XE  \
        /lisport 1521

  installState=$?
else
  installState=0
fi
exit $installState
