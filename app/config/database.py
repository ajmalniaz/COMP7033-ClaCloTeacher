from pymongo import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS

client = MongoClient("mongodb+srv://19268023:test1234@cluster0.4myobrn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.teacher_db
fs = GridFS(db)
