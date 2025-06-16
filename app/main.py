from fastapi import FastAPI

app = FastAPI(root_path="/cheap_api")

@app.get("/")
def hello():
    return {"msg": "Hello FastAPI with Poetry"}
