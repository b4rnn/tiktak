# SETUP
```
    sudo apt-get install kibana
```
# CONFIG
```
   sudo nano /etc/kibana/kibana.yml
   #INDEXER
    elasticsearch.hosts: ["http://localhost:9200"]
   #PORT
    server.port: 5601
   #ENABLE
    sudo systemctl enable kibana
   #START
    sudo systemctl start kibana
   #STOP
    sudo systemctl stop kibana
   #RESTART
    sudo systemctl restart kibana
```
