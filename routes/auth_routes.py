from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from utils.jwt_manager import create_token
from schemas.user_schema import UserSchema

auth_router = APIRouter()

@auth_router.post('/login', tags=['auth'], response_model=dict, status_code=200)
def login(user: UserSchema = Body()):
  if user.email == 'admin@mail.com' and user.password == '12345678':
    token = create_token(data=user.model_dump())
    response = JSONResponse(content={'message': 'Login success', 'token': token}, status_code=200)
  else:
    response = JSONResponse(content={'message': 'Login failed'}, status_code=401)
    
  return response