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

@app.get("/healthcheck", status_code=200)
async def healthcheck():
    return

# @app.get("/task/{id}")
# async def get_task_by_id(id: int):
#     return dict_tasks.get(id)

# @app.put("/task/{id}")
# async def update_task_by_id(id: int, task: Tasks):
#     if id in dict_tasks.keys():
#         dict_tasks[id] = (task.name, task.priority)
#         return (task.name, task.priority)
#     else:
#         raise HTTPException(status_code=404, detail="no task with id {}".format(id))

# @app.delete("/task/{id}")
# async def delete_task_by_id(id: int):
#     if id in dict_tasks.keys():
#         dict_tasks.pop(id)
#         return {"deleted task with id": id}
#     else:
#         raise HTTPException(status_code=404, detail="no task with id {}".format(id))

