DECLARE @DataPath NVARCHAR(MAX);
DECLARE @LogPath NVARCHAR(MAX);
DECLARE @DBName SYSNAME = N'DB';
DECLARE @UserID SYSNAME = N'intershop';
DECLARE @Password NVARCHAR(128) = N'intershop';
/* Recovery Model, Possible values: FULL, SIMPLE, BULK_LOGGED, default is FULL*/
DECLARE @Recovery NVARCHAR(30) = 'SIMPLE'

DECLARE @Sql NVARCHAR(MAX);

SET @DataPath = CONVERT(NVARCHAR(MAX), SERVERPROPERTY('InstanceDefaultDataPath'));
SET @LogPath = CONVERT(NVARCHAR(MAX), SERVERPROPERTY('InstanceDefaultLogPath'));

print 'Creating database: ' + QUOTENAME(@DBName);
SET @Sql = 'CREATE DATABASE
            ' + @DBName + '
            CONTAINMENT = NONE
            ON PRIMARY (
                NAME = ''' + @DBName + '''
                , FILENAME = ''' + CONCAT(@DataPath, N'', @DBName, N'.mdf') + '''
                , SIZE = 8MB
                , MAXSIZE = UNLIMITED
                , FILEGROWTH = 64MB )
            LOG ON (
                NAME = ''' + CONCAT(@DBName, N'_log') + '''
                , FILENAME = ''' + CONCAT(@LogPath, N'', @DBName, N'_log.ldf') + '''
                , SIZE = 8MB
                , MAXSIZE = UNLIMITED
                , FILEGROWTH = 64MB )
            COLLATE Latin1_General_100_CI_AS';
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;

print 'Enabling full-text search...';
SET @Sql = QUOTENAME(@DBName) + '.[dbo].[sp_fulltext_database] @action = ''enable''';
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;

print 'Creating user: ' + QUOTENAME(@UserID);
SET @Sql = 'CREATE LOGIN
            ' + QUOTENAME(@UserID) + '
            WITH
                PASSWORD = ''' + REPLACE(@Password, '''', '''''') + '''
                , DEFAULT_DATABASE = [master]
                , DEFAULT_LANGUAGE = [us_english]
                , CHECK_EXPIRATION = OFF
                , CHECK_POLICY = OFF';
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;

print 'Setting default database ...';
SET @Sql = 'ALTER LOGIN ' + QUOTENAME(@UserID) + ' WITH DEFAULT_DATABASE = ' + QUOTENAME(@DBName);
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;
SET @Sql = 'ALTER AUTHORIZATION ON DATABASE::' + @DBName + ' TO ' + @UserID
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;

print 'Setting Read Committed Snapshot ...';
SET @Sql = 'ALTER DATABASE ' + QUOTENAME(@DBName) + ' SET READ_COMMITTED_SNAPSHOT ON'
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;

print 'Setting Recovery Model ...';
SET @Sql = 'ALTER DATABASE ' + QUOTENAME(@DBName) + ' SET RECOVERY ' + @Recovery
print 'Executing SQL: ' + @Sql;
EXECUTE sp_executesql @Sql;
