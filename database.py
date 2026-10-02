import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv(override=True)


def get_db_connection():
  return mysql.connector.connect(
    host=os.environ["MYSQLHOST"],
    port=int(os.environ.get("MYSQLPORT") or 3306),
    user=os.environ["MYSQLUSER"],
    password=os.environ["MYSQLPASSWORD"],
    database=os.environ["MYSQLDATABASE"],
)