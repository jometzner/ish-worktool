#!/bin/bash -e
# Description:
#   Basic sample script to manage XE database options
#
# For debugging uncomment below
# set -x

############
#  Function to echo usage
############
usage ()
{
  program=`basename $0`
cat <<EOF
Usage:
   ${program} [-o start|stop] [-h]

   Options:
     -o start or -o stop will start or stop the XE database and listener
EOF
exit 1
}


###########################################
#  Function to change database environments
###########################################
set_env ()
{
   REC=`grep "^${1}" /etc/oratab | grep -v "^#"`
   if test -z $REC
   then
     echo "Database NOT in ${v_oratab}"
     exit 1
   else
     echo "Database in ${v_oratab} - setting environment"
     export ORAENV_ASK=NO
     export ORACLE_SID=${1}
     . oraenv >> /dev/null
     export ORAENV_ASK=YES
   fi

}

####################################
#  Function to setup parameter variables
####################################
setup_parameters ()
{
  ## Set Other ENV
  set_env XE
  TNS_ADMIN=${ORACLE_HOME}/network/admin
  EDITOR=vi
  NLS_DATE_FORMAT="dd/mm/yyyy:hh24:mi:ss"

  if [ -e ${TNS_ADMIN}/listener.ora ]; then
    sed -i -e "s/^.*HOST.*/\ \ \ \ \ \ \ (ADDRESS = (PROTOCOL = TCP)(HOST = $HOSTNAME)(PORT = 1521))/" ${TNS_ADMIN}/listener.ora
  fi

  if [ -e ${TNS_ADMIN}/tnsnames.ora ]; then
    sed -i -e "s/^.*HOST.*/\ \ \ \ \ \ \ (ADDRESS = (PROTOCOL = TCP)(HOST = $HOSTNAME)(PORT = 1521))/" ${TNS_ADMIN}/tnsnames.ora
  fi
  ## Echo back the hostname and IP
  ##
  echo $HOSTNAME - $(echo $(ip addr show dev eth0 | sed -nr 's/.*inet ([^ ]+).*/\1/p') | cut -f 1 -d '/')
}


enableDBExpress ()
{
set_env XE
echo "update settings to allow DBExpress Access"
sqlplus / as sysdba << EOF
  exec dbms_xdb_config.setlistenerlocalaccess(false);
  exec dbms_xdb_config.setglobalportenabled(true);
  exit
EOF
echo ".. Done"
}
###################
###################
## Main
###################
###################

if test $# -lt 2
then
  usage
fi

## Get all values
while test $# -gt 0
do
   case ${1} in
   -o)
           shift
           v_option=${1}
           ;;
   -h)
           usage
           ;;
   *)      usage
           ;;
   esac
   shift
done

if [ -n "$(ls -A /opt/oracle/oradata 2>/dev/null)" ]; then
  echo "DB files are available in /opt/oracle/oradata ..."

  setup_parameters

  ######
  ######
  # execute what is needed


  case ${v_option} in
   "start")
            sudo /etc/init.d/oracle-xe-18c start
            enableDBExpress
            echo "DATABASE IS READY TO USE!" #being compatible with testcontainers
            tail -F -n 0 /opt/oracle/diag/rdbms/xe/XE/trace/alert_XE.log
            ;;
   "stop")
            sudo /etc/init.d/oracle-xe-18c stop
            tail -50 /opt/oracle/diag/rdbms/xe/XE/trace/alert_XE.log
            ;;
  esac
else
  /home/oracle/bin/manage-init-xe.sh

  enableDBExpress
  echo "DATABASE IS READY TO USE!" #being compatible with testcontainers
  tail -F -n 0 /opt/oracle/diag/rdbms/xe/XE/trace/alert_XE.log
fi


