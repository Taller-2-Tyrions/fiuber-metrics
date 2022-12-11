from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
port = os.getenv("MONGO_PORT")
uri = os.getenv("MONGO_URI")

client = MongoClient(uri, port)
db = client["metrics"]
