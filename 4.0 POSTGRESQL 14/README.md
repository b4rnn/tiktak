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
#[ENABLE]  postgre service
   sudo systemctl enable postgresql
#[RESTART]  postgre service
   sudo systemctl restart postgresql
#[STOP]  postgre service
   sudo systemctl stop postgresql
#[STATUS]  postgre service
   sudo systemctl status postgresql
```
# VERSION
```
 postgre --version
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
sudo -u postgres psql

ALTER USER postgres PASSWORD 'dataLake';

#create db called (gala) with username (postgres) and password (dataLake)

CREATE DATABASE gala;

execute psql  -U postgres -h 127.0.0.1 --password gala;

CREATE TABLE TRAFFIC(
   id SERIAL PRIMARY KEY,
   timestamp VARCHAR  NULL,
   camera_id VARCHAR  NULL,
   car_model VARCHAR NULL,
   car_color VARCHAR  NULL,
   car_make VARCHAR  NULL,
   car_location VARCHAR NULL,
   latitude VARCHAR NULL,
   longitude VARCHAR NULL,
   car_count INT  NULL,
   car_route VARCHAR  NULL,
   car_speed INT  NULL,
   car_class VARCHAR  NULL,
   car_image VARCHAR NULL,
   detection_time VARCHAR  NULL,
   detection_day VARCHAR  NULL,
   detection_month VARCHAR  NULL,
   detection_year VARCHAR  NULL,
   car_heat_signal VARCHAR  NULL,
   car_number_plate VARCHAR  NULL
);

CREATE TABLE PARKING(
   id SERIAL PRIMARY KEY,
   timestamp VARCHAR  NULL,
   camera_id VARCHAR  NULL,
   car_model VARCHAR NULL,
   car_color VARCHAR  NULL,
   car_make VARCHAR  NULL,
   car_location VARCHAR NULL,
   latitude VARCHAR NULL,
   longitude VARCHAR NULL,
   car_count INT  NULL,
   car_image VARCHAR NULL,
   car_class VARCHAR  NULL,
   car_slot_id VARCHAR  NULL,
   detection_time VARCHAR  NULL,
   detection_day VARCHAR  NULL,
   detection_month VARCHAR  NULL,
   detection_year VARCHAR  NULL,
   car_number_plate VARCHAR  NULL
);

CREATE TABLE PERSON(
   id SERIAL PRIMARY KEY,
   timestamp VARCHAR  NULL,
   camera_id VARCHAR  NULL,
   latitude VARCHAR NULL,
   longitude VARCHAR NULL,
   person_age VARCHAR NULL,
   person_gender VARCHAR  NULL,
   person_race VARCHAR  NULL,
   person_religion VARCHAR NULL,
   person_location INT  NULL,
   detection_time VARCHAR  NULL,
   detection_day VARCHAR  NULL,
   detection_month VARCHAR  NULL,
   detection_year VARCHAR  NULL,
   person_emotion VARCHAR  NULL,
   person_face VARCHAR  NULL,
   person_count VARCHAR  NULL,
   person_height VARCHAR  NULL,
   person_item VARCHAR  NULL
);

CREATE TABLE WEATHER(
   id SERIAL PRIMARY KEY,
   timestamp VARCHAR  NULL,
   sensor_id VARCHAR  NULL,
   latitude VARCHAR NULL,
   longitude VARCHAR NULL,
   weather_status VARCHAR NULL,
   weather_time VARCHAR  NULL,
   weather_day VARCHAR NULL,
   weather_month VARCHAR  NULL,
   weather_year VARCHAR  NULL,
   weather_location VARCHAR  NULL
);

CREATE TABLE GSM(
   id SERIAL PRIMARY KEY,
   timestamp VARCHAR  NULL,
   sensor_id VARCHAR  NULL,
   sensor_location VARCHAR  NULL,
   sms VARCHAR NULL,
   imei VARCHAR  NULL,
   day VARCHAR NULL,
   month VARCHAR  NULL,
   year VARCHAR  NULL,
   latitude VARCHAR  NULL,
   longitude VARCHAR NULL,
   device VARCHAR  NULL,
   distance VARCHAR  NULL
);

```
# libpqxx-dev
```
sudo apt-get update -y
sudo apt-get install -y libpqxx-dev
```
