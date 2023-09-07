from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient

class TaskModel(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


app = FastAPI()
client = TestClient(app)

task_holder = {}
last_inserted_id = 0


@app.get("/tasks/")
async def get_all_tasks():
    global task_holder
    temp_list = list()
    for x in task_holder:
        temp_list.append(task_holder[x])
    return temp_list

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    global task_holder
    if str(task_id) not in task_holder:
        raise HTTPException(status_code=404, detail="Item not found")
    return task_holder[str(task_id)]

@app.post("/tasks/")
async def create_task(task: TaskModel):
    global task_holder
    global last_inserted_id
    last_inserted_id = last_inserted_id + 1
    task.id = last_inserted_id
    if task.title == "":
        raise HTTPException(status_code=400, detail="Bad request")
    if task.description == "":
        raise HTTPException(status_code=400, detail="Bad request")
    task_holder[str(last_inserted_id)] = task
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int,task: TaskModel):
    global task_holder
    if str(task_id) not in task_holder:
        raise HTTPException(status_code=404, detail="Item not found")
    if task.title == "":
        raise HTTPException(status_code=400, detail="Bad request")
    if task.description == "":
        raise HTTPException(status_code=400, detail="Bad request")
    task_holder[str(task_id)] = task
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global task_holder
    if str(task_id) not in task_holder:
        raise HTTPException(status_code=404, detail="Item not found")
    task = task_holder[str(task_id)]
    task_holder.pop(str(task_id))
    return task

def test_get_all_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200

def test_get_task():
    response =  client.get("/tasks/-1")
    assert response.status_code == 404

def test_create_task():
    response =  client.post("/tasks/",json={"id":0,"title":"test123","description":"ytest","completed":False})
    assert response.status_code == 200

def test_update_task():
    response =  client.put("/tasks/-1",json={"id":0,"title":"test123","description":"ytest","completed":False})
    assert response.status_code == 404

def test_delete_task():
    response =  client.delete("/tasks/-1") 
    assert response.status_code == 404
