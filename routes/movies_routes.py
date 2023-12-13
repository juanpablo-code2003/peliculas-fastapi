import time

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from middleware.jwt_bearer import JWTBearer
from models.movie_model import Movie as MovieModel
from config.database import SessionDB
from schemas.movie_schema import MovieSchema

movie_router = APIRouter()

@movie_router.get('/movies', tags=['Movies'], response_model=List[MovieSchema], status_code=200)#, dependencies=[Depends(JWTBearer())])
def get_all_movies() -> List[MovieSchema]:
  db = SessionDB()
  movies = db.query(MovieModel).all()
  return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=MovieSchema, status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(ge=1, le=2000)):
  db = SessionDB()
  movie = db.query(MovieModel).filter(MovieModel.id == id).first()
  response = JSONResponse(content=jsonable_encoder(movie), status_code=200)
  if not movie:
    response = JSONResponse(content={'message': 'Movie not found'}, status_code=404)
    
  return response

# Query parameters
@movie_router.get('/movies/', tags=['Movies'], response_model=List[MovieSchema], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str = Query(min_length=5, max_length=12)):
  db = SessionDB()
  movies = db.query(MovieModel).filter(MovieModel.category == category).all()
  response = JSONResponse(content=movies, status_code=200)
  if not movies:
    response = JSONResponse(content={'message': 'Category not found'}, status_code=404)
    
  return response

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def add_movie(movie: MovieSchema):
  db = SessionDB()
  new_movie = MovieModel(**movie.model_dump())
  db.add(new_movie)
  db.commit()
  return JSONResponse(content={'message': 'Movie added successfully'}, status_code=201)

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_movie(id: int, movie: MovieSchema):
  db = SessionDB()
  movie_query = db.query(MovieModel).filter(MovieModel.id == id).first()
  
  if not movie:
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)
  
  movie_query.title = movie.title
  movie_query.overview = movie.overview
  movie_query.year = movie.year
  movie_query.rating = movie.rating
  movie_query.category = movie.category
  db.commit()
    
  return JSONResponse(content={'message': 'Movie updated successfully'}, status_code=200)

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int = Path(ge=1, le=2000)):
  db = SessionDB()
  movie = db.query(MovieModel).filter(MovieModel.id == id).first()
  if not movie:
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)
  
  db.delete(movie)
  db.commit()
    
  return JSONResponse(content={'message': 'Movie deleted successfully'}, status_code=200)