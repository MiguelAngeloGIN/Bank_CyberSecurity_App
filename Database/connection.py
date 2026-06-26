import os
from dotenv import load_dotenv, dotenv_values
import mysql.connector

class Connections:
 @staticmethod
 def connect_database():
  load_dotenv()
  try:
   conn = mysql.connector.connect (
     host = "localhost",
     user = os.getenv("MY_USER"),
     password = os.getenv("MY_PASSWORD"),
     database = "Bank_Database"
     )
   cursor = conn.cursor()
   print ("Connected to database")
   return conn, cursor
  except Exception as e:
   print (e)
   return


Connections.connect_database()