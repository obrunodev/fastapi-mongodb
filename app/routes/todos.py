
from app.models.todos import Todo
from app.config.database import MongoDB
from app.schema.todos import TodoOut
from bson import ObjectId
from decouple import config
from fastapi import APIRouter, HTTPException

# Instanciando o MongoDB
mongo_db = MongoDB(config("MONGODB_URI"), "fastapi_mongodb")
collection_name = mongo_db.get_collection("todos")

router = APIRouter()

def todo_serializer(todo) -> TodoOut:
    return TodoOut(id=str(todo['_id']), name=todo['name'], description=todo['description'], complete=todo['complete'])

@router.get('/', response_model=list[TodoOut])
async def get_todos():
    todos = list(collection_name.find())
    return [todo_serializer(todo) for todo in todos]

@router.post('/', response_model=TodoOut)
async def create_todo(todo: Todo):
    result = collection_name.insert_one(todo.dict())
    created_todo = collection_name.find_one({'_id': result.inserted_id})
    if created_todo is None:
        raise HTTPException(status_code=500, detail="Failed to create Todo")
    return todo_serializer(created_todo)

@router.put('/{id}', response_model=TodoOut)
async def update_todo(id: str, todo: Todo):
    result = collection_name.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': todo.model_dump()},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_serializer(result)

@router.delete('/{id}', response_model=dict)
async def delete_todo(id: str):
    result = collection_name.find_one_and_delete({'_id': ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}