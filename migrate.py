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