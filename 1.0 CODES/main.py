import os
import re
import json
import time
import redis
import psycopg2
import requests
from time import sleep
from Queue import Queue
from psycopg2 import Error
from threading import Thread
from datetime import datetime
r = redis.Redis(host='localhost', port=6379, db=0)
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

queue = Queue()

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='pb',
                            user='postgres',
                            password='pbtest123')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    end_date=str(request.args.get('end_date', None))
    return {}

def pubsub_task(i, q):
    while True:
        query = q.get()
        
        if query:
            sleep(3)
            print(query)
            _response ={}
            data = requests.get('http://localhost:9200/idxtfdb/_search?q='+query+'&size=1')
            response = data.json()
            _response_list = []
            elastic_docs = response["hits"]["hits"]
            for num, doc in enumerate(elastic_docs):
                try:
                    source_data = doc["_source"]
                    source_data.pop('_meta', None)
                    _response_list.append(source_data)
                except TypeError:
                    print('TypeError')
            #_response_List = [i for n, i in enumerate(_response_list) if i not in _response_list[n + 1:]]
            print(source_data['businessid'])
            r.publish(source_data['businessid'], json.dumps(source_data))
        q.task_done()
        

@app.route('/create/', methods=('GET', 'POST'))
def create():
    #if request.data:
    #if request.is_json:
    data = request.get_json()
    print(request.data)
    print(str(request.args.get('date', None)))
    res = {}
    sentence = "%.20f" % time.time()
    time_stamp = re.sub('(?<=\d)[,.](?=\d)','',sentence)
    try:
        conn = get_db_connection()

        # Open a cursor to perform database operations
        cur = conn.cursor()

        cur.execute('INSERT INTO trade_f (timestamp, date, status, amount, businessid)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (str(time_stamp),
                    str(request.args.get('date', None)),
                    str(request.args.get('status', None)),
                    str(request.args.get('amount', None)),
                    str(request.args.get('businessid', None)))
                    )

        conn.commit()
        
        queue.put(time_stamp)
        status = "record inserted sucessfully"
        res ={"status":status}
    except (Exception, Error) as error:
        
        err="Error while connecting to PostgreSQL" + str(error)
        res ={"status":err}
    finally:
        if (conn):
            cur.close()
            conn.close()
    
    return res

if __name__ == "__main__":
    thread = Thread(target=pubsub_task , args=(1, queue, ))
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0',port=5000,debug=False)
