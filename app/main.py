from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/cheap_api")

origins = [
    "http://localhost",
    "http://localhost:8081", 
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 白名单
    allow_credentials=True,
    allow_methods=["*"],    # 允许所有方法
    allow_headers=["*"],    # 允许所有头部
)

@app.get("/hello")
def hello():
    return {"msg": "Hello from FastAPI"}
