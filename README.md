# VIMEO
```
 Optimize Investigative Processes
```
# PRODUCTION SETUP
*VIMEO setup is Highly Sequential.Follow Steps below*
    `1.0 CODES`
    `2.0 DEPENDENCIES`
    `3.0 CMAKE`
    `4.0 OPENCV`
    `5.0 MONGO`
    `6.0 REDIS`
    `7.0 NGINX`
    
* System has been optised for Cpu Through Multithreading , Queuing and Multiprocessing.
# GOAL
```
 Extract Faces from offline videos and record results as m3u8 
```

# OBJECTIVES
```
Grab Video frames
Detect Faces
Extract Faces
Filter Faces
Extract TimeStamps
Stream video during Facial Extraction Process
Store High quality video for display and recording
Publish recognised and detected faces for analyis
Update database with the right data based on metrics
```
# APIS
```
 #START STOP CAMERA
```
# METRICS
```
TIME_STAMP
FRAME_RATE
FRAME_WIDTH
FRAME_HEIGHT
FACIAL_SCORE
THREAD_COUNT
```

# SUMMARY
```
| SERVER            | IP ADRRESS    | STORAGE | CPUS | MEMORY | PUBLIC PORT |  OS           |  INTERNAL PORTS       
| CONTAINER         | 192.168.8.203 |  1+ TB  | 16+  | 32+    |  214/229    |  UBUNTU 18.0X |  80/5010/27107/6379
```

# NOTICE
```
ALWAYS REMOVE SOURCE FILES FROM PRODUCTION SERVER UPON SUCCESSFUL DEPLOYMENT EXCEPT PYTHON SCRIPTS
```
