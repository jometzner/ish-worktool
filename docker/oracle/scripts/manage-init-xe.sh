#!/bin/bash -e

set -x

/home/oracle/bin/check_space.sh \
&& /home/oracle/bin/create_listener.sh \
&& /home/oracle/bin/create_db.sh \
&& /home/oracle/bin/prepare_user.sh