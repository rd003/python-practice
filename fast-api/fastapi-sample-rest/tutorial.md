# Tutorial

Source: Learned from chai code (Hitesh chaudhary)

- Create virtual env

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install these packages

```bash
pip install fastapi uvicorn
```

- Create requirements.txt with `pip freeze > requirements.txt`

- Create a file main.py

```py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tea(BaseModel):
    id:int
    name:str
    origin:str

teas: List[Tea] = []

@app.get("/")
def read_root():
    return {"message":"Welcome to tea house"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def add_tea(tea:Tea):
    teas.append(tea)
    return tea

@app.put("/teas/{tea_id}")
def update_tea(tea_id:int,updated_tea:Tea):
    for index,tea in enumerate(teas):
        if tea.id==tea_id:
            teas[index]= updated_tea
            return updated_tea
    return {"error":"tea not found"} 

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id:int):
    for index, tea in enumerate(teas):
        if tea.id==tea_id:
            deleted=teas.pop(index)
            return deleted           
    return {"error":"tea not found"}    
```

## Run the app

- `uvicorn main:app --reload`
- Open the app in browser with swagger : `http://127.0.0.1:8000/docs`