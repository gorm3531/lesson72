from fastapi import FastAPI, status, Body, HTTPException, Path
import uvicorn
from typing import List, Annotated
from pydantic import BaseModel

app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_get() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def get_put(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                  username: Annotated[
            str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                  age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]):
    try:
        for edit_user in users:
            if edit_user.id == user_id:
                edit_user.username = username
                edit_user.age = age
            return edit_user
    except:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def get_del(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]):
    try:
        user = next(user for user in users if users.id == user_id)
        users.pop(user)
        return user
    except:
        raise HTTPException(status_code=404, detail="User was not found")


@app.get('/')
async def messages() -> dict:
    return {"message": "Главная страница"}

