from http.client import HTTPException
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI
from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID('1b5a830c-9812-4272-a67c-6b2376e40140'),
        first_name='Douglas',
        last_name='Fresh',
        gender=Gender.male,
        roles=[Role.student]
    ),
    User(
        id=UUID('0e960aba-3bf2-4339-8ebb-d522eba85c00'),
        first_name='Deidre',
        last_name='Teach',
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get('/api/v1/users')
async def fetch_users():
    return db


@app.post('/api/v1/users')
async def register_users(user: User):
    db.append(user)
    return {'id': user.id}


@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f'user with id: {user_id} does not exist'
    )


@app.put('/ap/v1/users/{user_id}')
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f'user with id: {user_id} does not exist'
    )
