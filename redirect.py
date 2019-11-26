from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import json

ip = os.getenv("redirect_ip")

addr = 'http://' + ip + ':5000'

app = FastAPI()

dict_tasks = dict()

class Tasks(BaseModel):
    name: str
    priority: int

@app.get("/")
async def read_root():
    redirect = requests.get(url = addr + '/')
    return redirect.json()

@app.get("/task")
async def list_tasks():
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')
    redirect = requests.get(url = addr + '/task')
    return redirect.json()

@app.post("/task")
async def add_task(task: Tasks):
    data = {
        "name": task.name, 
        "priority": task.priority
    }
    requests.post(url = addr + '/task', data = json.dumps(data))
