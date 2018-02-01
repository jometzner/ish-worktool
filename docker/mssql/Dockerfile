FROM orbeon/mssql-server-linux-fts
ENV ACCEPT_EULA=Y
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y curl wget unixodbc locales && \
    wget https://packages.microsoft.com/ubuntu/16.04/prod/pool/main/m/mssql-tools/mssql-tools_14.0.5.0-1_amd64.deb && \
    wget https://packages.microsoft.com/ubuntu/16.04/prod/pool/main/m/msodbcsql/msodbcsql_13.1.6.0-1_amd64.deb && \
    apt-get update && \
    dpkg -i msodbcsql_13.1.6.0-1_amd64.deb && \
    dpkg -i mssql-tools_14.0.5.0-1_amd64.deb && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen
COPY icmdb.sql startup.sh /
RUN (export MSSQL_SA_PASSWORD=Intershop1111 && /opt/mssql/bin/sqlservr --reset-sa-password &) && \
    sleep 20 && \
    echo "start complete" && \
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Intershop1111 -q quit && \
    /opt/mssql-tools/bin/sqlcmd -b -S localhost -U sa -P Intershop1111 -i /icmdb.sql && \
    sleep 10 && \
    ps -j -C sqlservr --no-headers | awk "{print \$1}" | xargs kill && \
    sleep 10
EXPOSE 1433
CMD [ "bash", "/startup.sh" ]
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=8 CMD [ "/opt/mssql-tools/bin/sqlcmd", "-b", "-S", "localhost", "-U", "intershop", "-P", "intershop", "-q", "quit" ]
