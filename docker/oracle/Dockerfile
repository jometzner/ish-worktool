#
# Copyright 2021 Intershop Communications AG.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
ARG PREBUILD_DATABASE=false
FROM oraclelinux:7-slim

LABEL maintainer="a-team@intershop.de"
LABEL oracleversion="XE 18c"

ARG PREBUILD_DATABASE=false
ARG INSTALL_FILE_1="https://download.oracle.com/otn-pub/otn_software/db-express/oracle-database-xe-18c-1.0-1.x86_64.rpm"
ARG PATCH_RPM_7="https://yum.oracle.com/repo/OracleLinux/OL7/latest/x86_64/getPackage/kernel-headers-3.10.0-1127.19.1.el7.x86_64.rpm"
ARG DEFAULT_PASSWORD="intershop"

USER root

ENV ORACLE_BASE=/opt/oracle \
    ORACLE_HOME=/opt/oracle/product/18c/dbhomeXE \
    ORACLE_SID=XE \
    ORACLE_DOCKER_INSTALL="true"

RUN groupadd -g 501 oinstall \
  && groupadd -g 502 dba \
  && groupadd -g 503 oper \
  && useradd -m -g oinstall -G oinstall,dba,oper -u 501 oracle \
  && echo "oracle:${DEFAULT_PASSWORD}" | chpasswd \
  && rpm --rebuilddb \
  && yum --enablerepo=ol7_latest clean metadata \
  && yum -y install file openssl lsof sudo sysstat tree wget which  \
  && echo "oracle ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
  && echo "Defaults !requiretty"  >> /etc/sudoers \
  && mkdir -p $ORACLE_BASE \
  && mkdir -p /home/oracle/bin \
  && chown -R oracle:oinstall $ORACLE_BASE \
  && chown -R oracle:oinstall /home/oracle/bin \
  && yum clean all \
  && rm -rf /var/cache/yum/* \
  && rm -rf /var/tmp/yum*

RUN yum -y localinstall $PATCH_RPM_7 \
  && yum clean all \
  && rm -rf /var/cache/yum/* \
  && rm -rf /var/tmp/yum*

RUN yum -y install oracle-database-preinstall-18c \
  && yum clean all \
  && rm -rf /var/cache/yum/* \
  && rm -rf /var/tmp/yum*

RUN yum -y localinstall $INSTALL_FILE_1 \
  && rm -rf $ORACLE_HOME/demo \
  && rm -rf $ORACLE_HOME/dmu \
  && rm -rf $ORACLE_HOME/md \
  && rm -rf $ORACLE_HOME/nls/demo \
  && rm -rf $ORACLE_HOME/odbc \
  && rm -rf $ORACLE_HOME/jdbc \
  && rm -rf $ORACLE_HOME/rdbms/public \
  && rm -rf $ORACLE_HOME/rdbms/demo \
  && rm -rf $ORACLE_HOME/R \
  && rm -rf $ORACLE_HOME/instantclient \
  && rm -rf $ORACLE_HOME/inventory \
  && rm -rf $ORACLE_HOME/javavm \
  && rm -rf $ORACLE_HOME/deinstall \
  && rm -rf $ORACLE_HOME/crs \
  && rm -f  $ORACLE_HOME/bin/asmcmd \
  && rm -f  $ORACLE_HOME/bin/asmcmdcore \
  && rm -f  $ORACLE_HOME/bin/bdschecksw \
  && rm -f  $ORACLE_HOME/bin/dbv \
  && rm -f  $ORACLE_HOME/bin/ldap* \
  && rm -f  $ORACLE_HOME/bin/dbfs_client \
  && rm -f  $ORACLE_HOME/bin/afdboot \
  && rm -f  $ORACLE_HOME/bin/exp \
  && rm -f  $ORACLE_HOME/bin/imp \
  && rm -f  $ORACLE_HOME/bin/*.exe \
  && rm -f  $ORACLE_HOME/bin/lcsscan \
  && rm -f  $ORACLE_HOME/bin/dgmgrl \
  && rm -f  $ORACLE_HOME/bin/nid \
  && rm -f  $ORACLE_HOME/bin/orion \
  && rm -f  $ORACLE_HOME/bin/procob \
  && rm -f  $ORACLE_HOME/bin/setasmgid \
  && rm -f  $ORACLE_HOME/bin/wrap \
  && rm -f  $ORACLE_HOME/bin/*0 \
  && rm -f  $ORACLE_HOME/bin/tnsping \
  && rm -f  $ORACLE_HOME/bin/tkprof \
  && rm -f  $ORACLE_HOME/bin/srvctl \
  && rm -f  $ORACLE_HOME/bin/wrc \
  && rm -rf $ORACLE_HOME/sdk \
  && echo "------------" \
  && rm -rf $ORACLE_HOME/lib/clntsh.map \
  && rm -rf $ORACLE_HOME/lib/libccme_*.so \
  && rm -rf $ORACLE_HOME/lib/libcrs18.so \
  && rm -rf $ORACLE_HOME/lib/libmkl_avx*.so \
  && rm -rf $ORACLE_HOME/lib/libmkl_gf_*.so \
  && rm -rf $ORACLE_HOME/lib/libmkl_intel_*.so \
  && rm -rf $ORACLE_HOME/lib/libmkl_vml_*.so \
  && rm -rf $ORACLE_HOME/lib/libopc.so \
  && rm -rf $ORACLE_HOME/lib/libosbws.so \
  && rm -rf $ORACLE_HOME/lib/libra.so \
  && rm -rf $ORACLE_HOME/lib/libshpkavx*.so \
  && echo "------------" \
  && rm -r  $ORACLE_HOME/lib/*_sparc64.* \
  && rm -r  $ORACLE_HOME/lib/*_windows64.* \
  && rm -r  $ORACLE_HOME/lib/ra_*.zip \
  && rm -f  $ORACLE_HOME/lib/*_installer.zip \
  && rm -f  $ORACLE_HOME/lib/*.zip \
  && echo "------------" \
  && strip --remove-section=.comment $ORACLE_HOME/bin/oracle \
  && strip --remove-section=.comment $ORACLE_HOME/bin/rman \
  && strip --remove-section=.comment $ORACLE_HOME/bin/tnslsnr \
  && yum clean all \
  && rm -rf /var/cache/yum/* \
  && rm -rf /var/tmp/yum*

## Set the default ports to be exposed for Oracle XE, e
# xmaple 1521 is default listener port
#
EXPOSE 1521 5500

COPY scripts/*.sh /home/oracle/bin/

RUN chown oracle:oinstall /home/oracle/bin/*.sh \
  && chmod 775 /home/oracle/bin/*.sh

##  Setting ORACLE_DOCKER_INSTALL=true, you should not have to remove memlock options below
#   but I found I still had to do this.
RUN sed -i -e "s/^.*memlock.*//g" /etc/security/limits.d/oracle-database-preinstall-18c.conf

##
#  We now switch to the "oracle" user, up to this point all operations were performed as
#  the root user.  We also specify the work directory - which in this case is the default
#  oracle user home folder location
#
USER oracle
WORKDIR /home/oracle

##
#  Something really useful is to set current environment for the oracle user.
#  This is done using the ENV command. With this we specify the core parameters that will
#  make things simpler for the "oracle" unix account, example setting the PATH, ORACLE_HOME
#  ORACLE_SID etc.
#
ENV ORACLE_DOCKER_INSTALL=true \
  ORACLE_BASE=/opt/oracle \
  ORACLE_HOME=/opt/oracle/product/18c/dbhomeXE \
  PATH=/home/oracle/bin:/opt/oracle/product/18c/dbhomeXE/bin:$PATH \
  NLS_DATE_FORMAT="dd/mm/yyyy:hh24:mi:ss" \
  ORACLE_SID=XE

#  We clear bash history to keep things clean - this is optional
#  Prepare database files if necessary
#
RUN  history -c && if [ "$PREBUILD_DATABASE" == "true" ] ; then /home/oracle/bin/manage-init-xe.sh; fi

HEALTHCHECK --interval=1m --start-period=2m --retries=20 \
  CMD "/home/oracle/bin/check_status.sh"

##
#  The last instruction is to specify what will be executed when the container is created
#  from the image.  There is a few options, you could just start a bash shell and then
#  manually start the Oracle 18c XE database, or, you could call the custom manage-xe.sh
#  script with the "start" parameter to start the listener and XE database on container
#  creation (run time)
#
#  CMD ["/bin/bash"]
#
CMD ["/home/oracle/bin/manage-xe.sh", "-o", "start"]
