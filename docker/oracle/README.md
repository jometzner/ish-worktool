## Description

Creating a Docker setup for running Oracle 18c Express Edition in a Docker container for Intershop development.

---
**NOTE**

This build allow you to create a custom Oracle XE database called XE, but it is not the default CDB, but a non-CDB.
Meaning it is not a container database - no pluggable databases are used.

1.  This docker image does not make use of persistent storage, the database is located in the image and is useful for testing/development.

2.  The password for all database standard users is `intershop`.

3.  The user schema is `intershop` and password is also `intershop`.

---

## Configuration & Startup of a container

Once built, you can run the container example:

```
docker run -p 1521:1521 -p 5500:5500 --name oracle-intershop oracle-intershop
```

Compose File
```
version: "3.4"
services:
  oracle-server:
    image: intershophub/oracle-intershop:latest
    container_name: oracle-intershop
    ports:
    - "1521:1521"
    - "5500:5500"
```

There are no parameters required.

## Connect Local Build Environment (ICM 7.10)

To connect your local ICM development environment with the local docker mssql database your configuration in the `environment.properties` of your development machine should look like this.

```
# Database configuration
databaseType = oracle
jdbcUrl = jdbc:oracle:thin:@host:1521:XE
databaseUser = intershop 
databasePassword = intershop
```

## Build the Container

Build the container image with OracleLinux 7 and Oracle 18c XE Release 18.4.0.0.0

```
docker build . --tag oracle-intershop
```

With an additional parameter `PREBUILD_DATABASE`, it is possible to create a container with a prepared database.

```
docker build . --tag oracle-intershop:prep --build-arg PREBUILD_DATABASE=true
```

It is also possible to change the user password of the Oracle user with the parameter `DEFAULT_PASSWORD`.

## License

Copyright 2014-2020 Intershop Communications.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
