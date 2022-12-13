import os
import re
import time
import cv2
import base64    
import signal
import string
import random
import requests
import psycopg2
import subprocess
import numpy as np
from pathlib import Path
from datetime import date
import simplejson as json
from psycopg2 import Error
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from collections import defaultdict, Iterable
from cv2 import VideoWriter, VideoWriter_fourcc
from flask import Flask, flash, request, redirect, render_template ,jsonify

app=Flask(__name__)


cors = CORS(app, resources={

    r"/*": {
        "origins": "*"

    }
})

app.secret_key = "secret key"
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER_ADVERT = os.path.join(path, '/var/www/html/advert')
UPLOAD_FOLDER_PROFILE = os.path.join(path, '/var/www/html/profile')
UPLOAD_FOLDER_BILLBOARD = os.path.join(path, '/var/www/html/billboard')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER_ADVERT ):
    os.mkdir(UPLOAD_FOLDER_ADVERT)

if not os.path.isdir(UPLOAD_FOLDER_PROFILE ):
    os.mkdir(UPLOAD_FOLDER_PROFILE)

if not os.path.isdir(UPLOAD_FOLDER_BILLBOARD ):
    os.mkdir(UPLOAD_FOLDER_BILLBOARD)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_BILLBOARD 
app.config['UPLOAD_FOLDER_ADVERT'] = UPLOAD_FOLDER_ADVERT 
app.config['UPLOAD_FOLDER_PROFILE'] = UPLOAD_FOLDER_PROFILE

# Supported File extensions
ALLOWED_EXTENSIONS_BILLBOARD  = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXTENSIONS_PROFILE    = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXTENSIONS_ADVERT     = set(['webp','m4v','vob', 'wmv', 'mov', 'mkv', 'webm', 'gif','mp4','avi','flv'])

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir)))

def allowed_file_advert(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_ADVERT

def allowed_file_billboard(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_BILLBOARD 


def allowed_file_profile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PROFILE

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='gala',
                            user='postgres',
                            password='dataLake')
    return conn

#PORTALS
ADMIN_URL       = 'http://127.0.0.1/sws/admin/'
AGENT_URL       = 'http://127.0.0.1/sws/agent/'
CLIENT_URL      = 'http://127.0.0.1/sws/client/'
DEFAULT_URL     = 'http://127.0.0.1/sws/auth/login/'
ADVERT_URL      = 'http://127.0.0.1/advert/'
PROFILE_URL     = 'http://127.0.0.1/profile/'
BILLBOARD_URL   = 'http://127.0.0.1/billboard/'
CAMPAIGN_URL    = 'http://127.0.0.1/sws/client/campaigns/new/'

#CREATE PROFILE
@app.route('/api/profile/create/<roleId>' , methods=['POST'])
def CREATE_PROFILE(roleId):
    if request.method == 'POST':
        Role = roleId
        Status = "active"
        upload_result = {}
        uploaded_profile_path = " "
        try:
            #upload profile image
            files = request.files.to_dict()

            for file in files:
                if file and allowed_file_profile(files[file].filename):
                    profile_filename = files[file].filename
                    file_extension = os.path.splitext(profile_filename)[1]
                    profile_filename_as_timestamp=re.sub(r"\.", "", str(time.time()))
                    filename = str(profile_filename_as_timestamp)+file_extension
                    files[file].save(os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename))
                    uploaded_profile_path = str(UPLOAD_FOLDER_PROFILE) + "/" + filename
                else:
                    upload_result = {  "status": "UPLOAD FAILED . MEDIA TYPE NOT SUPPORTED."}
            #upload profile details
            upload_result = {  "status": uploaded_profile_path}
            if(upload_result): 
                today = date.today()
                sentence = "%.20f" % time.time()
                id= re.sub('(?<=\d)[,.](?=\d)','',sentence)
                Registration_date =today.strftime("%b-%d-%Y")
                try:
                    conn = get_db_connection()
                    # Open a cursor to perform database operations
                    cur = conn.cursor()  
                    cur.execute('INSERT INTO users (user_id, first_name , last_name, user_email, user_password, user_role, user_status, user_gender, user_telephone, user_date_of_birth, user_registration_date, user_image)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (id,request.form['Firstname'],request.form['Lastname'],request.form['Email'],request.form['Password'],Role,Status,request.form['Gender'],request.form['Telephone'],request.form['Dob'],Registration_date,uploaded_profile_path))
                    conn.commit()
                    
                    status = "PROFILE " + id +" CREATED SUCESSFULLY"
                    upload_result ={"status":status,"sessionid":id}
                except (Exception, Error) as error:
                    
                    err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                    upload_result ={"status":err}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
            
        except Error:
            upload_result = { "status":"Error"}
        return jsonify(upload_result)

#AUTH PROFILES
@app.route('/api/auth/profile' , methods=['POST'])
def AUTHENTICATE_PROFILE():
    if request.method == 'POST':
        RESULT = {}
        API_RESULT = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute("SELECT * FROM users WHERE user_email = %s ", (API_RESULT['username'],))
            conn.commit()
            test_record = cur.fetchone()
            if(API_RESULT['username'] == test_record[3]):
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()  
                    cur.execute("SELECT * FROM users WHERE user_email = %s AND user_password = %s", (API_RESULT['username'],API_RESULT['password']))
                    conn.commit()
                    user_records = cur.fetchone()
                    if(API_RESULT['password'] != user_records[4]):
                        RESULT = {"msg":"WRONG PASSWORD","uri":DEFAULT_URL,"status":"201"}
                    if(API_RESULT['username'] != user_records[3] and API_RESULT['password'] != user_records[4]):
                        RESULT = {"msg":"WRONG USERNAME AND PASSWORD","uri":DEFAULT_URL,"status":"201"}
                    if(API_RESULT['username'] == user_records[3] and API_RESULT['password'] == user_records[4]):
                        if (user_records[6] =='active'):
                            if (user_records[5] =='admin'):
                                RESULT = {"msg":"LOGIN SUCESSFULL","uri":ADMIN_URL,"status":"200" ,"id":user_records[12]}
                            if (user_records[5] =='agent'):
                                RESULT = {"msg":"LOGIN SUCESSFULL","uri":AGENT_URL,"status":"200" ,"id":user_records[12]}
                            if (user_records[5] =='client'):
                                RESULT = {"msg":"LOGIN SUCESSFULL","uri":CLIENT_URL,"status":"200" ,"id":user_records[12]}
                        if (user_records[6] !='active'):
                            MSG = "Account " + user_records[3] + " currently " + user_records[6] + ". Contact Admin "
                            RESULT = {"msg":MSG ,"uri":DEFAULT_URL,"status":"201"}
                except (Exception, Error) as error:
                    RESULT = {"msg":"WRONG EMAIL ADDRESS OR PASSWORD","uri":DEFAULT_URL,"status":"201"}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
            if(API_RESULT['username'] != test_record[3]):
                    RESULT = {"msg":"WRONG  EMAIL ADDRESS","uri":DEFAULT_URL,"status":"201"}
        except (Exception, Error) as error:
            #err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg":"WRONG EMAIL ADDRESS","uri":DEFAULT_URL ,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(RESULT)

#ACTIVATE PROFILES
@app.route('/api/profile/activate/<id>' , methods=['POST'])
def ACTIVATE_PROFILE(id):
    if request.method == 'POST':
        delete_result = {}
        try:
            conn = get_db_connection()
            # Open a cursor to perform database operations
            cur = conn.cursor()  
            cur.execute('UPDATE users set user_status = %s WHERE user_id = %s', (request.form['activate'],id))
            conn.commit()
            if(request.form['activate']=='active'):
                status = "USER " + id +" ACTIVATED SUCESSFULLY"
            
            if(request.form['activate']=='inactive'):
                status = "USER " + id +" DEACTIVATED SUCESSFULLY"

            if(request.form['activate']=='suspended'):
                status = "USER " + id +" SUSPENDED SUCESSFULLY"

            delete_result ={"status":status}
        except (Exception, Error) as error:
            
            err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            delete_result ={"status":err}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(delete_result)

#QUERY PROFILES
@app.route('/api/profile/query/all' , methods=['POST'])
def QUERY_PROFILES():
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        print(API_RESULT)
        if(API_RESULT['query']=="all"):
            data = requests.get('http://localhost:9200/idxudb/_search?size='+str(API_RESULT['limit']))
            response = data.json()
            elastic_docs = response["hits"]["hits"]
            for num, doc in enumerate(elastic_docs):
                try:
                    source_data = doc["_source"]
                    source_data.pop("_meta", None)
                    #source_data.pop("billboard_ip_address", None)
                    source_data["user_image"] = PROFILE_URL + os.path.basename(source_data['user_image'])
                    Query_List.append(source_data)
                except TypeError:
                    print('TypeError')
            Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
            RESULT = {"msg":Query_Result ,"status":"200"}
    return jsonify(Query_Result)

#QUERY PROFILE
@app.route('/api/profile/query' , methods=['POST'])
def QUERY_PROFILE():
    if request.method == 'POST':
        API_RESULT = request.get_json()
        RESULT ={}
        data = requests.get('http://localhost:9200/idxudb/_search?q='+API_RESULT['query'])
        response = data.json()
        Query_List = []
        elastic_docs = response["hits"]["hits"]
        for num, doc in enumerate(elastic_docs):
            try:
                source_data = doc["_source"]
                source_data.pop("_meta", None)
                source_data["user_image"] = PROFILE_URL + os.path.basename(source_data['user_image'])
                Query_List.append(source_data)
            except TypeError:
                Query_List=[]

        Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
        RESULT = {"msg":Query_Result ,"status":"200"}
    return jsonify(RESULT)

#UPDATE PROFILE
@app.route('/api/profile/update/<id>' , methods=['POST'])
def UPDATE_PROFILE(id):
    if request.method == 'POST':
        upload_result = {}
        uploaded_profile_path = " "
        try:
            #upload profile image
            files = request.files.to_dict()

            for file in files:
                if file and allowed_file_profile(files[file].filename):
                    profile_filename = files[file].filename
                    file_extension = os.path.splitext(profile_filename)[1]
                    profile_filename_as_timestamp=re.sub(r"\.", "", str(time.time()))
                    filename = str(profile_filename_as_timestamp)+file_extension
                    files[file].save(os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename))
                    uploaded_profile_path = str(UPLOAD_FOLDER_PROFILE) + "/" + filename
                else:
                    upload_result = {  "status": "UPLOAD FAILED . MEDIA TYPE NOT SUPPORTED."}
            #upload profile details
            upload_result = {  "status": uploaded_profile_path}
            if(upload_result): 
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()  
                    cur.execute('UPDATE users SET first_name = %s , last_name = %s, user_email = %s , user_password = %s, user_gender = %s, user_telephone = %s, user_date_of_birth = %s, user_image = %s WHERE user_id = %s',
                    (request.form['Firstname'],request.form['Lastname'],request.form['Email'],request.form['Password'],request.form['Gender'],request.form['Telephone'],request.form['Dob'],uploaded_profile_path,id))
                    conn.commit()
                    
                    status = "PROFILE " + id +" UPDATED SUCESSFULLY"
                    upload_result ={"status":status,"sessionid":id}
                except (Exception, Error) as error:
                    
                    err="ERROR OCURRED .. CONTACT ADMIN  " + str(error)
                    upload_result ={"status":err}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
            
        except Error:
            upload_result = { "status":"Error"}
        return jsonify(upload_result)

#CREATE BILLBOARD
@app.route('/api/billboard/create' , methods=['POST'])
def CREATE_BILLBOARD():
    if request.method == 'POST':
        try:
            #upload billboard image
            RESULT ={}
            upload_result = {}
            API_RESULT = request.get_json()
            
            uploaded_advert_path = " "
            filename_as_timestamp=re.sub(r"\.", "", str(time.time()))
            filename  = filename_as_timestamp+'.'+API_RESULT['extension']
            _filename = UPLOAD_FOLDER_BILLBOARD + "/" + filename
            with open(_filename,"wb") as f:
                f.write(base64.b64decode(API_RESULT['file']))
            API_RESULT.pop('file')
            print( API_RESULT)
            #upload billboard details
            upload_result = {  "status": _filename}
            if(upload_result): 
                sentence = "%.20f" % time.time()
                id= re.sub('(?<=\d)[,.](?=\d)','',sentence)
                try:
                    conn = get_db_connection()
                    # Open a cursor to perform database operations
                    cur = conn.cursor()  
                    cur.execute('INSERT INTO billboard (billboard_id, billboard_image , billboard_daily_views, billboard_sign_placement, billboard_traffic_direction, billboard_availability, billboard_duration, billboard_height, billboard_width, billboard_name, billboard_latitude, billboard_longitude, billboard_ip_address, billboard_screen_count , billboard_status , billboard_city , billboard_state , billboard_zip , billboard_county , billboard_country , billboard_vcpus)'
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s, %s, %s)',
                                (id,_filename,API_RESULT['daily_views'],API_RESULT['sign_placement'],API_RESULT['traffic_direction'],
                                API_RESULT['availability'],API_RESULT['duration'],API_RESULT['dimension_height'],API_RESULT['dimension_width'],API_RESULT['name'],API_RESULT['latitude'],
                                API_RESULT['longitude'],API_RESULT['ip_address'],API_RESULT['screen_count'],API_RESULT['status'],API_RESULT['city'],API_RESULT['state'],API_RESULT['zip'],API_RESULT['county'],API_RESULT['country'],API_RESULT['capacity']))

                    conn.commit()

                    #UPDATE LOCATIONS
                    cur.execute('INSERT INTO locations (location_id, city , state , zip, county ,country , names)''VALUES (%s, %s, %s, %s, %s, %s, %s)',(id,API_RESULT['city'],API_RESULT['state'],API_RESULT['zip'],API_RESULT['county'],API_RESULT['country'],API_RESULT['name']))
                    conn.commit()
                    
                    msg = "BILLBOARD " + id +" CREATED SUCESSFULLY"
                    BILLBOARD_URL_SUCESSFULL = ADMIN_URL + "?" + API_RESULT['id']
                    RESULT = {"msg":msg,"uri":BILLBOARD_URL_SUCESSFULL ,"status":"200"}
                except (Exception, Error) as error:
                    
                    msg="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                    RESULT = {"msg":msg,"uri":"#","status":"201"}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
            
        except Error:
            RESULT = {  "msg": "UPLOAD FAILED . MEDIA TYPE NOT SUPPORTED.","uri":"#","status":"201"}

        return jsonify(RESULT)

#DELETE BILLBOARD
@app.route('/api/billboard/delete/<id>' , methods=['POST'])
def DELETE_BILLBOARD(id):
    if request.method == 'POST':
        delete_result = {}
        try:
            conn = get_db_connection()
            # Open a cursor to perform database operations
            cur = conn.cursor()  
            cur.execute("DELETE FROM billboard WHERE billboard_id = %s", (id,))
            conn.commit()
            status = "BILLBOARD " + id +" DELETED SUCESSFULLY"
            
            delete_result ={"status":status}
        except (Exception, Error) as error:
            
            err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            delete_result ={"status":err}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(delete_result)

#ACTIVATE BILLBOARDS
@app.route('/api/billboard/activate/<id>' , methods=['POST'])
def ACTIVATE_BILLBOARDS(id):
    if request.method == 'POST':
        delete_result = {}
        try:
            conn = get_db_connection()
            # Open a cursor to perform database operations
            cur = conn.cursor()  
            cur.execute('UPDATE billboard set billboard_availability = %s WHERE billboard_id = %s', (request.form['availability'],id))
            conn.commit()
            if(request.form['availability']=='available'):
                status = "BILLBOARD " + id +" IS NOW AVAILABLE"
            
            if(request.form['availability']=='unavailable'):
                status = "USER " + id +" IS NOW UNAVAILABLE"

            if(request.form['availability']=='suspend'):
                status = "USER " + id +" OPERATIONS HAS BEEN SUSPENDED"

            delete_result ={"status":status}
        except (Exception, Error) as error:
            
            err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            delete_result ={"status":err}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(delete_result)

#UPDATE BILLBOARD
@app.route('/api/billboard/update/<id>' , methods=['POST'])
def UPDATE_BILLBOARD(id):
    if request.method == 'POST':
        update_result = {}
        updated_advert_path = " "
        try:
            #update billboard image
            files = request.files.to_dict()

            for file in files:
                if file and allowed_file_billboard(files[file].filename):
                    advert_filename = files[file].filename
                    file_extension = os.path.splitext(advert_filename)[1]
                    advert_filename_as_timestamp=re.sub(r"\.", "", str(time.time()))
                    filename = str(advert_filename_as_timestamp)+file_extension
                    files[file].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    updated_advert_path = str(UPLOAD_FOLDER_BILLBOARD) + "/" + filename
                else:
                    update_result = {  "status": "update failed media file not supported"}
            #update billboard details
            update_result = {  "status": updated_advert_path}
            if(update_result): 
                try:
                    conn = get_db_connection()
                    # Open a cursor to perform database operations
                    cur = conn.cursor()
                    cur.execute('UPDATE billboard SET billboard_image = %s , billboard_daily_views = %s , billboard_sign_placement = %s , billboard_traffic_direction = %s , billboard_availability = %s , billboard_duration = %s , billboard_dimension = %s , billboard_name = %s , billboard_latitude = %s , billboard_longitude= %s , billboard_ip_address = %s , billboard_screen_count = %s , billboard_status = %s WHERE billboard_id = %s ', (updated_advert_path,request.form['daily_views'],request.form['sign_placement'],request.form['traffic_direction'],
                     request.form['availability'],request.form['duration'],request.form['dimension'],request.form['name'],request.form['latitude'],request.form['longitude'],request.form['ip_address'],request.form['screen_count'],request.form['status'],id))

                    conn.commit()
                    
                    status = "billboard " + id +" updated sucessfully"
                    update_result ={"status":status}
                except (Exception, Error) as error:
                    
                    err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                    update_result ={"status":err}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
            
        except Error:
            update_result = { "status":"Error"}
        return jsonify(update_result)

#START / STOP BILLBOARD
@app.route('/api/billboard/controls/start' , methods=['POST'])
def START_STOP_ADVERT():
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        print(API_RESULT)
        try:
            conn = get_db_connection()
            # Validate Billboard
            cur = conn.cursor()  
            cur.execute("SELECT * FROM billboard WHERE billboard_id = %s", (API_RESULT['id'],))
            conn.commit()
            billboard_records = cur.fetchone()
            if(billboard_records[13] == API_RESULT['status'] ):
                if(billboard_records[13] == 'ON'):
                    RESULT = {"msg" : " BILLBOARD ALREADY RUNNING . KINDLY TURN OFF THEN ON TO UPDATE FURTHER CHANGES ","status":"200","mode":API_RESULT['status']}

                if(billboard_records[13] == 'OFF'):
                    RESULT = {"msg" : " BILLBOARD ALREADY STOPPED . KINDLY TURN ON THEN OFF TO UPDATE FURTHER CHANGES ","status":"200","mode":API_RESULT['status']}

            if(billboard_records[13] != API_RESULT['status']):
                try:
                    if(API_RESULT['status'] == 'ON'):
                        WIDTH = "1920"
                        HEIGHT = "1080"
                        URL =  billboard_records[12]+'/api/edge/controls/start'
                        print(URL)
                        
                        PAYLOAD = {'screen': API_RESULT['screen'] , 'signal':'START' ,'width': WIDTH , 'height': HEIGHT ,'status': True}
                        res = requests.post(URL, json=PAYLOAD)
                        
                        if(res.text!=''):
                            print("{} --------  {}".format(" PID IS ",res.text))
                            #UPDATE DB
                            try:
                                conn = get_db_connection()
                                cur = conn.cursor()
                                cur.execute('UPDATE billboard SET  billboard_status = %s ,billboard_pid = %s WHERE billboard_id = %s ', (API_RESULT['status'],res.text ,API_RESULT['id']))
                                conn.commit()
                                
                                msg = "BILLBOARD " + billboard_records[9] + " IS NOW " + API_RESULT['status']
                                RESULT = {"msg" : msg,"status":"200","mode":API_RESULT['status']}

                            except (Exception, Error) as error:
                                
                                msg="EDGE DEVICE IS OFFLINE "
                                RESULT = {"msg" : msg,"status":"201","mode":API_RESULT['status']}
                            finally:
                                if (conn):
                                    cur.close()
                                    conn.close()

                    if(API_RESULT['status'] == 'OFF'):
                        URL =  billboard_records[12]+'/api/edge/controls/start'
                        PAYLOAD = {'signal':billboard_records[15] ,'status': False}
                        res = requests.post(URL, json=PAYLOAD)
                        if(res.text=='200'):
                            #UPDATE DB
                            try:
                                conn = get_db_connection()
                                cur = conn.cursor()
                                cur.execute('UPDATE billboard SET  billboard_status = %s,billboard_pid = %s WHERE billboard_id = %s ', (API_RESULT['status'],'',API_RESULT['id']))
                                conn.commit()
                                
                                msg = "BILLBOARD " + billboard_records[9] + " IS NOW " + API_RESULT['status']
                                RESULT = {"msg" : msg,"status":"200","mode":API_RESULT['status']}
                            except (Exception, Error) as error:
                                
                                msg="EDGE DEVICE IS OFFLINE "
                                RESULT = {"msg" : msg,"status":"201","mode":API_RESULT['status']}
                            finally:
                                if (conn):
                                    cur.close()
                                    conn.close()

                except (Exception, Error) as error:
                    
                    msg="EDGE DEVICE IS OFFLINE "
                    RESULT = {"msg" : msg,"status":"201","mode":API_RESULT['status']}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
        except (Exception, Error) as error:
            print(error)
            msg="ERROR OCURRED .. CONTACT ADMIN  "
            RESULT = {"msg" : msg,"status":"201","mode":API_RESULT['status']}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(RESULT)

#QUERY BILLBOARDS
@app.route('/api/billboard/query/all' , methods=['POST'])
def QUERY_BILLBOARDS():
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        if(API_RESULT['query']=="all"):
            data = requests.get('http://localhost:9200/idxbdb/_search?size='+str(API_RESULT['limit']))
            response = data.json()
            Query_List = []
            elastic_docs = response["hits"]["hits"]
            for num, doc in enumerate(elastic_docs):
                try:
                    source_data = doc["_source"]
                    source_data.pop("_meta", None)
                    source_data.pop("billboard_ip_address", None)
                    source_data["billboard_image"] = BILLBOARD_URL + os.path.basename(source_data['billboard_image'])
                    Query_List.append(source_data)
                except TypeError:
                    print('TypeError')
            Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
            #print(Query_Result)
            RESULT = {"msg":Query_Result ,"status":"200"}
    return jsonify(RESULT)

#QUERY BILLBOARD
@app.route('/api/billboard/query/<query>' , methods=['POST'])
def QUERY_BILLBOARD(query):
    if request.method == 'POST':
        _response ={}
        data = requests.get('http://localhost:9200/idxbdb/_search?q='+query+'&size='+str(request.form['limit']))
        response = data.json()
        Query_List = []
        elastic_docs = response["hits"]["hits"]
        for num, doc in enumerate(elastic_docs):
            try:
                source_data = doc["_source"]
                source_data.pop("_meta", None)
                source_data.pop("billboard_ip_address", None)
                source_data["billboard_image"] = "IP_ADRRESS/" + os.path.basename(source_data['billboard_image'])
                Query_List.append(source_data)
            except TypeError:
                print('TypeError')

        Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
    return jsonify(Query_Result)

#SELECT BILLBOARD
@app.route('/api/billboard/select' , methods=['POST'])
def SELECT_BILLBOARD():
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        data = requests.get('http://localhost:9200/idxbdb/_search?q='+API_RESULT['query'])
        response = data.json()
        Query_List = []
        elastic_docs = response["hits"]["hits"]
        for num, doc in enumerate(elastic_docs):
            try:
                source_data = doc["_source"]
                source_data.pop("_meta", None)
                #source_data.pop("billboard_ip_address", None)
                source_data["billboard_image"] = BILLBOARD_URL + os.path.basename(source_data['billboard_image'])
                Query_List.append(source_data)
            except TypeError:
                print('TypeError')
        Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
        RESULT = {"msg":Query_Result ,"status":"200"}
    return jsonify(RESULT)

#QUERY BILLBOARD BY LOCATION
@app.route('/api/billboard/query/location' , methods=['POST'])
def QUERY_BILLBOARD_LOCATION():
    if request.method == 'POST':
        _response ={}
        data = requests.get('http://localhost:9200/idxbdb/_search?&size='+str(request.form['limit'])+'&q='+str(request.form['latitude'])+'&q='+str(request.form['longitude']))
        response = data.json()
        Query_List = []
        elastic_docs = response["hits"]["hits"]
        for num, doc in enumerate(elastic_docs):
            try:
                source_data = doc["_source"]
                source_data.pop("_meta", None)
                source_data.pop("billboard_ip_address", None)
                source_data["billboard_image"] = "IP_ADRRESS/" + os.path.basename(source_data['billboard_image'])
                Query_List.append(source_data)
            except TypeError:
                print('TypeError')
        Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
    return jsonify(Query_Result)

#QUERY BILLBOARD BY AUTOCOMPLETE
@app.route('/api/billboard/query/autocomplete' , methods=['POST'])
def QUERY_BILLBOARD_AUTOCOMPLETE():
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        data = requests.get('http://localhost:9200/idxblocdb/_search?q='+str(API_RESULT['query'])+'&size='+str(API_RESULT['limit']))
        response = data.json()
        elastic_docs = response["hits"]["hits"]
        for num, doc in enumerate(elastic_docs):
            try:
                source_data = doc["_source"]
                source_data.pop("_meta", None)
                Query_List.append(source_data)
            except TypeError:
                print('TypeError')
        Query_Result = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
        print(Query_Result)
        RESULT = {"msg":Query_Result ,"status":"200"}
    return jsonify(RESULT)

#CREATE A CAMPAIGN
@app.route('/api/campaign/create' , methods=['POST'])
def CREATE_CAMPAIGN(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        print(API_RESULT)
        sentence = "%.20f" % time.time()
        campaign_id= re.sub('(?<=\d)[,.](?=\d)','',sentence)
        try:
            conn = get_db_connection()
            # Open a cursor to perform database operations
            cur = conn.cursor()  
            cur.execute('INSERT INTO campaigns (campaign_id, campaign_status, campaign_name,campaign_category,campaign_owner_id)'
                        'VALUES (%s, %s, %s, %s, %s)',
                        (campaign_id,'ONGOING',API_RESULT['name'],API_RESULT['category'],API_RESULT['id']))

            conn.commit()

            msg = "CAMPAIGN " + API_RESULT['name'] +" CREATED SUCESSFULLY ."
            RESULT = {"msg" : msg,"status":"200","uri":CAMPAIGN_URL,"id":campaign_id}

        except (Exception, Error) as error:
            
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201","sessionId":API_RESULT['id']}
        finally:
            if (conn):
                cur.close()
                conn.close()

        return jsonify(RESULT)

@app.route('/api/campaign/locations' , methods=['POST'])
def CAMPAIGN_LOCATIONS(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        print(API_RESULT)
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('UPDATE campaigns SET business_id = %s WHERE campaign_id = %s AND campaign_owner_id = %s',
            (API_RESULT['billboard_id'],API_RESULT['campaign_id'],API_RESULT['uid']))
            conn.commit()
            
            msg ="BILLBOARD SAVED SUCESSFULLY " 
            RESULT = {"msg" : msg,"status":"200","sessionId":API_RESULT['uid']}
        except (Exception, Error) as error:
            
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()
            
    return jsonify(RESULT)

@app.route('/api/campaign/budget' , methods=['POST'])
def CAMPAIGN_BUDGET(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        print(API_RESULT)
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('UPDATE campaigns SET daily_budget = %s ,campaign_start_date = %s, campaign_end_date = %s WHERE campaign_id = %s AND campaign_owner_id = %s',
            (API_RESULT['budget'],API_RESULT['start'],API_RESULT['end'],API_RESULT['campaign_id'],API_RESULT['uid']))
            conn.commit()
            
            msg ="BILLBOARD BUDGET SAVED SUCESSFULLY " 
            RESULT = {"msg" : msg,"status":"200","sessionId":API_RESULT['uid']}
        except (Exception, Error) as error:
            
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()
            
    return jsonify(RESULT)

@app.route('/api/campaign/schedule' , methods=['POST'])
def CAMPAIGN_SCHEDULE(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('UPDATE campaigns SET schedule = %s  WHERE campaign_id = %s AND campaign_owner_id = %s',
            (API_RESULT['schedule'],API_RESULT['campaign_id'],API_RESULT['uid']))
            conn.commit()
            
            msg ="SCHEDULE SAVED SUCESSFULLY " 
            RESULT = {"msg" : msg,"status":"200","sessionId":API_RESULT['uid']}
        except (Exception, Error) as error:
            
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()

    return jsonify(RESULT)

@app.route('/api/campaign/query' , methods=['POST'])
def CAMPAIGN_QUERY(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        DISPLAY = []
        API_RESULT = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('SELECT * FROM campaigns  WHERE campaign_id = %s AND campaign_owner_id = %s',(API_RESULT['campaign_id'],API_RESULT['uid']))
            conn.commit()
            campaign_records = cur.fetchone()
            if(campaign_records[0]==API_RESULT['campaign_id']):
                cur.execute('SELECT billboard_screen_count , billboard_width , billboard_height,billboard_name FROM billboard WHERE billboard_id = %s',(campaign_records[2],))
                conn.commit()
                billboard_records = cur.fetchone()
                msg ="BILLBOARD SAVED SUCESSFULLY "
                if(billboard_records[0]== '1'):
                    DISPLAY.append(['FILL'])
                    RESULT = {"msg" : msg,"status":"200","count":billboard_records[1],"display":DISPLAY}
                if(billboard_records[0]=='2'):
                    DISPLAY.append(['LEFT','RIGHT'])
                    RESULT = {"msg" : msg,"status":"200","count":billboard_records[2],"display":DISPLAY}
                if(billboard_records[0]=='3'):
                    DISPLAY.append(['LEFT','RIGHT','BOTTOM','TOP','CENTER'])
                    RESULT = {"msg" : msg,"status":"200","count":billboard_records[2],"display":DISPLAY}
                if(billboard_records[0]=='4'):
                    DISPLAY.append(['LEFT','RIGHT','BOTTOM-LEFT','BOTTOM-RIGHT','BOTTOM-CENTER','TOP-CENTER','BOTTOM','TOP'])
                    RESULT = {"msg" : msg,"status":"200","count":billboard_records[2],"display":DISPLAY}
        except (Exception, Error) as error:
            print(error)
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(RESULT)

@app.route('/api/campaign/design' , methods=['POST'])
def CAMPAIGN_DESIGN(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        uploaded_advert_path = " "
        filename_as_timestamp=re.sub(r"\.", "", str(time.time()))
        _filename = UPLOAD_FOLDER_ADVERT+ "/" + filename_as_timestamp+'.'+API_RESULT['extension']
        with open(_filename,"wb") as f:
            f.write(base64.b64decode(API_RESULT['file']))

        API_RESULT.pop('file')
        videoPoster = UPLOAD_FOLDER_ADVERT+ "/" + filename_as_timestamp+'.jpg'

        if(API_RESULT['extension']=='jpg' or API_RESULT['extension']=='png' or API_RESULT['extension']=='jpeg'):
            
            width = 3840
            height = 2400
            FPS = 120
            seconds = 11
            img = cv2.imread(_filename)
            height, width, c = img.shape
            fourcc      = cv2.VideoWriter_fourcc(*'vp80')
            videoFile   = UPLOAD_FOLDER_ADVERT+ "/" + filename_as_timestamp+'.webm'
            video       = VideoWriter(videoFile, fourcc, float(FPS), (width, height))
            i = 0
            
            while i < (FPS*seconds):
                i += 1
                
                # divided the image into left and right part
                # like list concatenation we concatenated
                # right and left together
                l = img[:, :(i % width)]
                r = img[:, (i % width):]
            
                img1 = np.hstack((r, l))
                video.write(img1)
                # this function will concatenate
                # the two matrices
            video.release()
            if(videoFile):
                try:
                    try:
                        conn = get_db_connection()
                        cur = conn.cursor() 
                        cur.execute('SELECT * FROM campaigns  WHERE campaign_id = %s AND campaign_owner_id = %s',(API_RESULT['campaign_id'],API_RESULT['uid']))
                        conn.commit()
                        campaign_records = cur.fetchone()
                        if(campaign_records[0]==API_RESULT['campaign_id']):
                            print(campaign_records[10])
                            conn = get_db_connection()
                            cur = conn.cursor()  
                            cur.execute('UPDATE campaigns SET campaign_media_position = %s, campaign_media_content = %s ,campaign_media_type = %s ,campaign_poster = %s WHERE campaign_id = %s AND campaign_owner_id = %s',
                            (API_RESULT['media_position'],videoFile,'image',_filename, API_RESULT['campaign_id'],API_RESULT['uid']))
                            conn.commit()
                            if(campaign_records[10] != ''):
                                os.remove(campaign_records[10])
                            
                            msg ="CAMPAIGN FILE SAVED SUCESSFULLY " 
                            RESULT = {"msg" : msg,"status":"200","sessionId":API_RESULT['uid']}
                    except (Exception, Error) as error:
                
                        msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                        RESULT = {"msg" : msg,"status":"201"}

                    finally:
                        if (conn):
                            cur.close()
                            conn.close()
                except (Exception, Error) as error:
                    
                    msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                    RESULT = {"msg" : msg,"status":"201"}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()

        if(API_RESULT['extension']=='mp4' or API_RESULT['extension']=='avi' or API_RESULT['extension']=='webm'):
            try:
                count = 0
                myFrameNumber = 50
                cap = cv2.VideoCapture(_filename)

                # get total number of frames
                totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

                # check for valid frame number
                if myFrameNumber >= 0 & myFrameNumber <= totalFrames:
                    # set frame position
                    cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)
                while True:
                    ret, frame = cap.read()
                    cv2.imwrite(videoPoster,frame)
                    break
                cap.release()
                try:
                    conn = get_db_connection()
                    cur = conn.cursor() 
                    cur.execute('SELECT * FROM campaigns  WHERE campaign_id = %s AND campaign_owner_id = %s',(API_RESULT['campaign_id'],API_RESULT['uid']))
                    conn.commit()
                    campaign_records = cur.fetchone()
                    if(campaign_records[0]==API_RESULT['campaign_id']):
                        print(campaign_records[10])
                        conn = get_db_connection()
                        cur = conn.cursor()  
                        cur.execute('UPDATE campaigns SET campaign_media_position = %s, campaign_media_content = %s ,campaign_media_type = %s ,campaign_poster = %s WHERE campaign_id = %s AND campaign_owner_id = %s',
                        (API_RESULT['media_position'],_filename,'video',videoPoster,API_RESULT['campaign_id'],API_RESULT['uid']))
                        conn.commit()
                        if(campaign_records[10] != ''):
                            os.remove(campaign_records[10])
                        
                        msg ="CAMPAIGN FILE SAVED SUCESSFULLY " 
                        RESULT = {"msg" : msg,"status":"200","sessionId":API_RESULT['uid']}
                except (Exception, Error) as error:
            
                    msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                    RESULT = {"msg" : msg,"status":"201"}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
            except (Exception, Error) as error:
                
                msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
                RESULT = {"msg" : msg,"status":"201"}
            finally:
                msg ="ERROR OCURRED .. CONTACT ADMIN "
                RESULT = {"msg" : msg,"status":"201"}
    
    return jsonify(RESULT)

@app.route('/api/campaign/review' , methods=['POST'])
def CAMPAIGN_REVIEW(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        advert_records = []
        design_records = []
        budget_records = []
        schedule_records = []
        API_RESULT = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('SELECT * FROM campaigns  WHERE campaign_id = %s AND campaign_owner_id = %s',(API_RESULT['campaign_id'],API_RESULT['uid']))
            conn.commit()
            campaign_records = cur.fetchone()
            if(campaign_records[0]==API_RESULT['campaign_id']):
                data = requests.get('http://localhost:9200/idxbdb/_search?q='+campaign_records[2])
                response = data.json()
                billboard_records = []
                elastic_docs = response["hits"]["hits"]
                for num, doc in enumerate(elastic_docs):
                    try:
                        source_data = doc["_source"]
                        source_data.pop("_meta", None)
                        #source_data.pop("billboard_ip_address", None)
                        source_data["billboard_image"] = BILLBOARD_URL + os.path.basename(source_data['billboard_image'])
                        Query_List.append(source_data)
                    except TypeError:
                        print('TypeError')
                billboard_records = [i for n, i in enumerate(Query_List) if i not in Query_List[n + 1:]]
                if(billboard_records):
                    DESIGN_MEDIA_URL  = ADVERT_URL + Path(campaign_records[10]).name
                    DESIGN_POSTER_URL = ADVERT_URL + Path(campaign_records[14]).name
                    schedule_records.append(re.sub("\"", "", campaign_records[6][0]))
                    advert_records.append({"name":campaign_records[8], "status":campaign_records[7], "category":campaign_records[12]})
                    design_records.append({"source_file":DESIGN_MEDIA_URL, "channel":campaign_records[13], "poster" : DESIGN_POSTER_URL})
                    budget_records.append({"daily_budget":campaign_records[3], "start_date":campaign_records[4], "end_date":campaign_records[5]})
                    msg ="BILLBOARD BUDGET SAVED SUCESSFULLY " 
                    RESULT = {"msg" : msg,"status":"200","location":billboard_records,"budget":budget_records,"schedule":schedule_records,"design":design_records,"campaign":advert_records}
        except (Exception, Error) as error:
            print(error)
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(RESULT)

@app.route('/api/campaign/submit' , methods=['POST'])
def CAMPAIGN_SUBMIT(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        Query_List = []
        API_RESULT = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('UPDATE campaigns SET campaign_status = %s  WHERE campaign_id = %s AND campaign_owner_id = %s',
            (API_RESULT['status'],API_RESULT['campaign_id'],API_RESULT['uid']))
            conn.commit()
            
            msg ="REVIEW SAVED SUCESSFULLY " 
            RESULT = {"msg" : msg,"status":"200","sessionId":API_RESULT['uid']}
        except (Exception, Error) as error:
            
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()

    return jsonify(RESULT)

@app.route('/api/campaign/status' , methods=['POST'])
def CAMPAIGN_STATUS(bid=None, uid=None):
    if request.method == 'POST':
        RESULT ={}
        DISPLAY = []
        API_RESULT = request.get_json()
        try:
            conn = get_db_connection()
            cur = conn.cursor()  
            cur.execute('SELECT * FROM campaigns  WHERE  campaign_owner_id = %s',(API_RESULT['uid'],))
            conn.commit()
            campaign_records = cur.fetchall()
            advert_records = []
            for campaign_record in campaign_records:
                DESIGN_MEDIA_URL  = ADVERT_URL + Path(campaign_record[10]).name
                DESIGN_POSTER_URL = ADVERT_URL + Path(campaign_record[14]).name
                advert_records.append({"source_file":DESIGN_MEDIA_URL, "channel":campaign_record[13], "poster" : DESIGN_POSTER_URL,"name":campaign_record[8], "status":campaign_record[7], "category":campaign_record[12]})
            msg ="SUCCESS "
            RESULT = {"msg" : msg, "status":"200" , "advert": advert_records}
        except (Exception, Error) as error:
            msg ="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            RESULT = {"msg" : msg,"status":"201"}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(RESULT)
    
#CREATE ADVERT
@app.route('/api/advert/create/<id>' , methods=['POST'])
def CREATE_ADVERT(id):
    if request.method == 'POST':
        upload_result = {}
        uploaded_advert_path = " "
        sentence = "%.20f" % time.time()
        try:
            conn = get_db_connection()
            # Validate Billboard
            cur = conn.cursor()  
            cur.execute("SELECT * FROM billboard WHERE billboard_id = %s", (id,))
            billboard_records = cur.fetchone()
            if(billboard_records[12]):
                sentence = "%.20f" % time.time()
                _id= re.sub('(?<=\d)[,.](?=\d)','',sentence)
                try:
                    #UPLOAD TEMPORARY ADVERT IMAGE
                    files = request.files.to_dict()
                    for file in files:
                        if file and allowed_file_advert(files[file].filename):
                            advert_filename = files[file].filename
                            file_extension = os.path.splitext(advert_filename)[1]
                            advert_filename_as_timestamp=re.sub(r"\.", "", str(time.time()))
                            filename = str(advert_filename_as_timestamp)+file_extension
                            files[file].save(os.path.join(app.config['UPLOAD_FOLDER_ADVERT'], filename))
                            uploaded_advert_path = str(UPLOAD_FOLDER_ADVERT) + "/" + filename
                        else:
                            upload_result = {  "status": "UPLOAD FAILED . MEDIA TYPE NOT SUPPORTED."}
                    upload_result = {  "status": uploaded_advert_path}
                    #upload billboard details
                    if(upload_result):
                        URL = 'http://'+ billboard_records[12] + '/api/edge/ads/submit'
                        PAYLOAD = {'uploaded_file': open(uploaded_advert_path,'rb')}
                        res = requests.post(URL, files=PAYLOAD)
                        if(res.ok):
                            EDGE_DEVICE=json.loads(res.text)
                            try: 
                                print(EDGE_DEVICE)
                                conn = get_db_connection()
                                cur = conn.cursor() 
                                cur.execute('INSERT INTO advert (business_id, advert_type , billboard_id, advert_width, advert_height, advert_budget, advert_demography, advert_duration, advert_media_type,  advert_media_content, advert_display_position, advert_status)'
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (_id,request.form['type'],id,EDGE_DEVICE["WIDTH"],EDGE_DEVICE["HEIGHT"],request.form['budget'],request.form['demography'],request.form['duration'],request.form['media_type'],EDGE_DEVICE["MEDIAFILE"],request.form['display_position'],'PENDING'))
                                conn.commit()

                                status = " ADVERT CAMPAIGN SUBMITTED . KINDLY WAIT FOR APRROVAL WITHIN 24 HRS "
                                upload_result ={"status":status}
                                
                                #REMOVE TEMPORARY IMAGE
                                os.remove(uploaded_advert_path)

                            except (Exception, Error) as error:
                                print("{} {}".format("DO NOT CLOSE VVV",str(error)))
                    
                                err="ERROR CREATING ADVERT .. CONTACT ADMIN " + str(error)
                                upload_result ={"status":err}
                            finally:
                                if (conn):
                                    cur.close()
                                    conn.close()
                except (Exception, Error) as error:
                    
                    err="ERROR CREATING ADVERT .. CONTACT ADMIN " + str(error)
                    upload_result ={"status":err}
                finally:
                    if (conn):
                        cur.close()
                        conn.close()
                        print("{} {}".format("DO NOT CLOSE","-------- CONNECTION ---------YET "))
        except (Exception, Error) as error:
            
            err="ERROR OCURRED .. CONTACT ADMIN " + str(error)
            upload_result ={"status":err}
        finally:
            if (conn):
                cur.close()
                conn.close()
    return jsonify(upload_result)

#submit/withdraw and advert
@app.route('/api/schedular/ads/submit' , methods=['POST'])
def schedular():
    status={}
    if request.method == 'POST':
        #validate billboard status
        request_data=request.get_json()
        print(request_data)
        if request_data.get('status') == True:
            start_metrics ="{}".format(request_data.get('query'))
            print(start_metrics)
            status = {'result':'ad scheduled sucessfull'}
            subprocess.run(["/home/titanx/Documents/GHALA/stroberi/Ads/build/SCHEDULAR",start_metrics])
        if request_data.get('status') == False:
            start_metrics ="{}".format(request_data.get('query'))
            status = {'result':'advert stopped . A reschedule is needed for further advertising'}
            subprocess.run(["/home/titanx/Documents/GHALA/stroberi/Ads/build/UNSCHEDULAR",start_metrics])
    return status
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5008,use_reloader=True)
