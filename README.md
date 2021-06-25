# SQL2NoSQL Example with MySQL and MongoDB
<p align="center">
    <img src="https://i.ibb.co/VDNZpvZ/logo-transparent.png" width="450">
</p>
<p align="center" style="font-size:200px;">
    Migrate data from SQL to NoSQL easily
</p>
<div align="center" style="display:inline;">
<img src="https://img.shields.io/badge/python-%203.6%20|%203.7%20|%203.8%20|%203.9%20-blue" />
<img src="https://img.shields.io/badge/black-v21.6b0-blue" />
<img src="https://img.shields.io/github/downloads/facundopadilla/sql2nosql/total?style=plastic" />
<img src="https://img.shields.io/pypi/v/sql2nosql" />
</div>


## SQL2NoSQL Installation
```python
pip install sql2nosql --upgrade
```

## Introduction
This example creates two databases using **Docker,** in this case, we will use **MySQL** and **MongoDB**.

For the MySQL client we will use '**mysql.connector**', and for MongoDB, we will use '**PyMongo**'.

For the environment variables (which are inside the **docker-environment.env** file), we will use a package called '**python-dotenv**'.

And well, obviously, to migrate this data, we will use '**sql2nosql**'.

----
## Basic usage

To start, let's install the requirements for Python (I recommend using virtual environments, I like **virtualenv** a lot)
```python
pip install -r requirements.txt
```
Next, if we need to test the migration (this is exactly why we decided to use Docker), we can execute the following command (if you want to edit the environment variables, you can do it from the 'docker-environment.env' file)

```
docker-compose --env-file ./docker-environment.env up --no-build -d
# the '--no-build' option is to not save the image and the '-d' option is to run the container in the background.
```

If you want to use the Makefile (only for lazy people with Linux, like me)

```
make up
```

Once this is done, you will have two containers named 'mysql_sql2nosql' and 'mongo_sql2nosql' running on host '0.0.0.0' with port '33060' for MySQL and '27018' for MongoDB.  If you want to see that they are actually created, use the following command: `docker ps`

You indicate the SQL and NoSQL database connection data in a dictionary, and the "client"/"engine" you normally use for this conversion (I recommend **PyMongo** for MongoDB).  (Remember that you can edit all this from the 'docker-environment.env' file).

Now it's time for the fun part, migrating :)

We are going to use '**python-dotenv**' to have the same data that is in the container, we are going to read the file 'docker-environment.env' just using this package.

```python
from sql2nosql import Migrator
from dotenv import dotenv_values

environ = dotenv_values("docker-environment.env")

sql_config = {
    "host": environ["HOST"],
    "port": int(environ["MYSQL_EXPOSE"]),
    "username": "root",
    "password": environ["MYSQL_ROOT_PASSWORD"],
    "database": environ["MYSQL_DATABASE"]
}

nosql_config = {
    "host": environ["HOST"],
    "port": int(environ["MONGO_EXPOSE"]),
    "username": environ["MONGO_USER"],
    "password": environ["MONGO_PASSWORD"]
}

c = Migrator(
    sql_config=sql_config,
    nosql_config=nosql_config,
    sql_client="mysql.connector",
    nosql_client="pymongo"
    )

c.migrate_data(tables=["customers", "employees", "offices"])
```
----
## How to view the migrated data

For this, we are going to enter the MongoDB container, for this we are going to execute the following command:
```
docker exec -it mongo_sql2nosql bash
```

For lazy people like me
```
make mongo_bash
```

Once inside the Mongo container, we are going to execute the following:

```
mongo -u sql2nosql -p
# Enter the password, which is '1234'.
```

To view the databases in Mongo, run the following command:

```
show databases;
```

To select our database (which is called 'classicmodels'), we execute the following command:

```
use classicmodels;
```

To view the collections in that database:
```
show collections;
```

And finally, to view the migrated data:

```
db.<collection_name>.find().pretty()
# Example: db.customers.find().pretty()
```

Enjoy! :)



https://user-images.githubusercontent.com/64610246/123432085-60c5ee00-d5a0-11eb-9f4c-e03d015b35e0.mp4

