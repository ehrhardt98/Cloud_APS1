from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymongo
import os

ip = os.getenv("mongodb_ip")

addr = "mongodb://" + ip + ":27017/"
mongo_client = pymongo.MongoClient(addr)
db = mongo_client['cloud_database']
tasks = db['tasks']

app = FastAPI()

class Tasks(BaseModel):
    name: str
    priority: int

@app.get("/")
async def read_root():
    return {"hello": "world"}

@app.get("/task")
async def list_tasks():
    ret = {}
    ret['Values'] = []
    for i in tasks.find(): # .sort( {'priority': 1} ):
        ret['Values'].append(
            {
                'id': str(i["_id"]), 
                'name': i["name"], 
                'priority': i["priority"]
            }
        )
    return ret

@app.post("/task")
async def add_task(task: Tasks):
    ret = {
        'name': task.name,
        'priority': task.priority,
    }
    tasks.insert(ret)
