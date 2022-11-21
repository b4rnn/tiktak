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

CREATE TABLE BILLBOARD(
   id SERIAL PRIMARY KEY,
   billboard_id VARCHAR  NULL,
   billboard_image VARCHAR  NULL,
   billboard_daily_views VARCHAR  NULL,
   billboard_sign_placement VARCHAR  NULL,
   billboard_traffic_direction VARCHAR  NULL,
   billboard_availability VARCHAR NULL,
   billboard_duration VARCHAR  NULL,
   billboard_dimension VARCHAR NULL,
   billboard_name VARCHAR  NULL,
   billboard_latitude VARCHAR  NULL,
   billboard_longitude VARCHAR NULL,
   billboard_ip_address VARCHAR  NULL,
   billboard_status VARCHAR  NULL,
   billboard_screen_count VARCHAR  NULL,
   billboard_pid VARCHAR  NULL
);

CREATE TABLE ADVERT(
   id SERIAL PRIMARY KEY,
   advert_type VARCHAR  NULL,
   business_id VARCHAR  NULL,
   billboard_id VARCHAR  NULL,
   advert_width VARCHAR  NULL,
   advert_height VARCHAR  NULL,
   advert_budget VARCHAR  NULL,
   advert_demography VARCHAR  NULL,
   advert_duration VARCHAR  NULL,
   advert_media_type VARCHAR  NULL,
   advert_media_content VARCHAR  NULL,
   advert_display_position VARCHAR  NULL,
   advert_status VARCHAR  NULL
);

CREATE TABLE USERS(
   id SERIAL PRIMARY KEY,
   first_name VARCHAR  NULL,
   last_name VARCHAR  NULL,
   user_email VARCHAR  NULL,
   user_password VARCHAR  NULL,
   user_role VARCHAR  NULL,
   user_status VARCHAR  NULL,
   user_gender VARCHAR  NULL,
   user_telephone VARCHAR  NULL,
   user_date_of_birth VARCHAR  NULL,
   user_registration_date VARCHAR  NULL
);

CREATE TABLE USERLOGS(
   user_telephone VARCHAR  NULL,
   user_login_date VARCHAR  NULL,
   user_logout_date VARCHAR  NULL,
   user_device VARCHAR  NULL,
   user_location VARCHAR  NULL
);

CREATE TABLE ADVERTLOGS(
   advert_id VARCHAR  NULL,
   advert_started_on VARCHAR  NULL,
   advert_stopped_on VARCHAR  NULL,
   billboard_id VARCHAR  NULL,
   business_id VARCHAR  NULL,
   advert_status VARCHAR  NULL
);

CREATE TABLE BILLBOARDLOGS(
   billboard_id VARCHAR  NULL,
   billboard_started_on VARCHAR  NULL,
   billboard_stopped_on VARCHAR  NULL,
   billboard_process_id VARCHAR  NULL,
   billboard_status VARCHAR  NULL
);
```
# libpqxx-dev
```
sudo apt-get update -y
sudo apt-get install -y libpqxx-dev
```
# DIAGNOSTICS 
```
pg_lsclusters
14  down    5432 online postgres /var/lib/postgresql/14/main /var/log/postgresql/postgresql-14-main.log

sudo nano /etc/postgresql/14/main/postgresql.conf
sudo service postgresql restart
sudo pg_ctlcluster 14 main start
sudo netstat -nlp | grep 5432

pg_lsclusters
Ver Cluster Port Status Owner    Data directory              Log file
14  main    5432 online postgres /var/lib/postgresql/14/main /var/log/postgresql/postgresql-14-main.log
```
