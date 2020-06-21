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
$ pip3 install requirements.txt

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

# View Data
To view the data stored on the mysql databse you can run the following sql query after inserting your database name:

``` bash
use <database name>;
select * from dispenser;
select * from dispenser_data;
```
