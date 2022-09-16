# FLASK

post , get and multithreading.
*API CONTAINER CONSISTS OF*

   *
    `FLASK`
    `UWSGI`

# SETUP
# Dependencies
```
sudo apt-get install python3-dev python3-numpy python3-pip

```
# python 3.5 +
```
#update & upgrade
    sudo apt update
    sudo apt install software-properties-common
#repo
    sudo add-apt-repository ppa:deadsnakes/ppa
    Press [ENTER] to continue or Ctrl-c to cancel adding it.
#install
    sudo apt install python3.7
#check
    python3.7 --version
```
# pip 
```
#install
    python3 -m pip install --upgrade pip
#upgrade
    pip3 install --upgrade setuptools
```
# BROADCAST
```
cd DATABASE 
pip3 install -r requirements.txt
sudo vi /etc/nging/sites-enabled/default

#paste text[from default]
    
#test nginx server
    sudo nginx -t
    sudo systemctl restart nginx
    sudo systemctl status nginx

cd back to   projcet FOLDER 
    python3 app.py

#test using postman (127.0.0.1:5007)
```
