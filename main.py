from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

dict_tasks = dict()

class Tasks(BaseModel):
    name: str
    priority: int

@app.get("/")
async def read_root():
    return {"hello": "world"}

@app.get("/task")
async def list_tasks():
    return dict_tasks

@app.post("/task")
async def add_task(task: Tasks):

    if len(dict_tasks.keys()) > 0:
        dict_tasks[max(dict_tasks.keys()) + 1] = (task.name, task.priority)
        return {"nova task": task.name, "id": task.priority}
    else:
        dict_tasks[0] = (task.name, task.priority)
        return {"nova task": task.name, "id": task.priority}

@app.get("/task/{id}")
async def get_task_by_id(id: int):
    return dict_tasks.get(id)

@app.put("/task/{id}")
async def update_task_by_id(id: int, task: Tasks):
    if id in dict_tasks.keys():
        dict_tasks[id] = (task.name, task.priority)
        return (task.name, task.priority)
    else:
        raise HTTPException(status_code=404, detail="no task with id {}".format(id))

@app.delete("/task/{id}")
async def delete_task_by_id(id: int):
    if id in dict_tasks.keys():
        dict_tasks.pop(id)
        return {"deleted task with id": id}
    else:
        raise HTTPException(status_code=404, detail="no task with id {}".format(id))

@app.get("/healthcheck", status_code=200)
async def healthcheck():
    return