# SETUP
```
    pip3 install pgsync
```
# INDEX DB
```
    bootstrap --config /PATH_TO/schema.json
    pgsync
```
# LIST indices [ELASTICSEARCH]
```
     curl -X GET "localhost:9200/_cat/indices?pretty"

```
# GET SPECIFIC INDEX [ELASTICSEARCH]
```
    curl -XGET "https://localhost:9200/_idxbedb" -d'
    curl -XGET "https://localhost:9200/<index name>" -d'
```
# DELETE SPECIFIC INDEX 
```
    curl -XDELETE localhost:9200/idxtedb
    curl -XDELETE localhost:9200/<index name>
```
# DELETE SPECIFIC INDEX [POSTGRES]
```
    rm.postgre_idxtedb
    rm .<database name>_<index name>
```
