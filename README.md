# Smart Dispenser Rest Network API and data analysis
> using Windows10, Python3.8, MySQL, Flask, SQL Alchemy, Marshmallow, Keras.

## Prerequisites
set up a mysql server and replace the line:  
```app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://janesh:password@localhost/testdatabase'```  
with your own modified version corresponding to your database settings:  
```app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@<server ip>/<database name>```

## Quick Start
``` bash
# install dependencies
$ pip3 install -r requirements.txt

# create database
$ create_db.py

# start server
$ server.py

# start client in another terminal (while server is running)
$ client.py

# execute data analysis (while server is running)
$ data_analysis.py

# run machine learning to predict days until dispenser fluid level is depleted
$ machine_learning.py
```

## View Data
To view the data stored on the mysql databse you can run the following sql query after inserting your database name:

``` bash
use <database name>;
select * from dispenser;
select * from dispenser_data;
```
## Optional

### Allow any device on LAN to connect to server API
You need to find the ip address of the machine the server is running on.  
Open a terminal and enter the following command:
``` bash
# for windows
$ ipconfig

# for linux
$ ifconfig
```
Find the IPv4 address for you wireless LAN and copy it, it will be formatted like this e.g. ```192.168.0.52```  
Head to the ```client.py``` file and find the one line that contains localhost at the bottom of the file.  
Replace localhost with the copied ip address.
Also replace the line at the top of the file in ```data_analysis.py```.  
  
 Any device currently connected to your local area network(LAN) via wifi will now be able to make requests to the server.
 
### Simulate multiple dispensers
Copy paste the client folder multiple times and run each client.py in their own terminal window.  
Ensure that server is currently running and that each new client folder copied has the config.json file set to it's default configuration:
``` bash
# config.json
{
    "created": "",
    "device_id": null,
    "location": "",
    "name": ""
}
```