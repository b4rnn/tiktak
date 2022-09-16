# DATABASE

*Storage , Read , Write and Index.*

* PostgreSQL 14 CONTAINER CONSISTS OF*

   *`POSTGRESQL DATABASE`

# SETUP
```
Install postgre >= 9.4 as elastic search  is mandatory.
Older postgre versions wont work well with syncqing data to elasticsearch >=7.1.
```
# Dependencies
```
sudo apt-cache search postgresql | grep postgresql
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt -y update
```
# INSTALL
```
sudo apt -y install postgresql-14
```
# CONDITIONS 
```
#[ENABLE] redis-server service
   sudo systemctl enable postgresql
#[RESTART] redis-server service
   sudo systemctl restart postgresql
#[STOP] redis-server service
   sudo systemctl stop postgresql
#[STATUS] redis-server service
   sudo systemctl status postgresql
```
# VERSION
```
redis-server --version
```
# CONFIG 
```
sudo nano /etc/postgresql/14/main/postgresql.conf
#WRITE ACCESS LOGS LEVEL
   [BEFORE] wal_level = ??
   [AFTER]  wal_level = logical
#REPLICATION SLOTS
   [BEFORE] # max_replication_slots = ??
   [AFTER]  max_replication_slots = 1
#WRITE ACCESS LOGS SIZE
   [BEFORE] max_slot_wal_keep_size = ??
   [AFTER]  max_slot_wal_keep_size = 100GB
#RESTART
   sudo systemctl restart postgresql 
#STATUS
   sudo systemctl status postgresql 
```
# PORTS 
```
postgre --5432
sudo ufw allow 5432/tcp
sudo ufw allow 5432/udp
```
# STORAGE
```
create db called (pb) with username (postgres) and password (pbtest123)

execute psql  -U postgres -h 127.0.0.1 --password pb;

CREATE TABLE TRADE_F(
   id SERIAL PRIMARY KEY,
   businessid VARCHAR  NULL,
   amount VARCHAR NULL,
   date VARCHAR  NULL,
   status VARCHAR  NULL,
   timestamp VARCHAR NULL
);
```
