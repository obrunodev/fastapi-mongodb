from fastapi import FastAPI
from app.routes.todos import router as todos_routers

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Todo API!"}

app.include_router(todos_routers, prefix='/todos', tags=['Tarefas'])
