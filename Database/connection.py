import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

class Connections:
 @staticmethod
 def connect_database():
 
  try:
   conn = mysql.connector.connect (
     host = "localhost",
     user = os.getenv("MY_USER"),
     password = os.getenv("MY_PASSWORD"),
     database = "Bank_Cyber_Database"
     )
   cursor = conn.cursor()
   print ("Connected to database")
   return conn, cursor
  except Exception as e:
   raise e


