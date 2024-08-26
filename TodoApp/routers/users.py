from email.policy import default
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from TodoApp.models import Todos, Users
from TodoApp.database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = "/user",
    tags = ["user"],
)
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class Phone_number(BaseModel):
    password: str
    new_phone_number: str = Field(min_length=8)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()
@router.put("/change_phone_number2",status_code=status.HTTP_201_CREATED)
async def change_phone_number(user:user_dependency, db:db_dependency,new_phone_number:str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Auth failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = new_phone_number
    db.add(user_model)
    db.commit()
@router.put("/change_phone_number",status_code=status.HTTP_201_CREATED)
async def change_phone_number(user:user_dependency, db:db_dependency,user_verification:Phone_number):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Auth failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
    user_model.phone_number = user_verification.new_phone_number
    db.add(user_model)
    db.commit()



@router.put("/password",status_code=status.HTTP_201_CREATED)
async def change_password(user:user_dependency,db:db_dependency,user_verification:UserVerification): #we are especting a body
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Auth failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect password')
    user_model.hashed_password = bcrypt_context.encrypt(user_verification.new_password)
    db.add(user_model)
    db.commit()