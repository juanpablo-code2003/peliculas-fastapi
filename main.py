import time

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse

from config.database import engine, Base
from middleware.jwt_bearer import JWTBearer
from middleware.error_handler import ErrorHandler
from routes.movies_routes import movie_router
from routes.auth_routes import auth_router

app = FastAPI()

app.title = 'Peliculas API'
app.description = 'API de peliculas'
app.version = '1.0.0'

app.add_middleware(ErrorHandler)
app.include_router(auth_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)
  

@app.get('/', tags=['Home'], dependencies=[Depends(JWTBearer())])
def home():
  return HTMLResponse(content='<h1>Bienvenido a FASTAPI movies</h1>', status_code=200)


