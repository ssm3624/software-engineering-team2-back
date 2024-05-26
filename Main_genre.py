from fastapi import FastAPI, HTTPException, APIRouter

import random
import time

from RatingLinkdata import prepare_dicts
from filter_genre_movie import filter_movies_by_genre
from Movie_print import prepare_genre_movies
from UserTags_create import create_user_tags_string
from Cosine_Al_movie import recommend_movies_by_similarity
from All_load_data import load_data

app = FastAPI()
to_router = APIRouter()

TEST_USER_ID = "TestID"  # 테스트용 유저 아이디

@to_router.get("/get-movie-list/{genre}")
async def recommend_movies(genre: str):
    random.seed(time.time())
    try:
        movies_data, links_data, ratings_data, user_data = load_data()
        ratings_dict, links_dict = prepare_dicts(ratings_data, links_data)
        filtered_movies = filter_movies_by_genre(movies_data, genre)
        genre_movies = prepare_genre_movies(filtered_movies, links_dict, ratings_dict)
        user_tags_string = create_user_tags_string(user_data)
        recommended_movies = recommend_movies_by_similarity(filtered_movies, user_tags_string, links_dict)
        
        movie = recommended_movies[0]
        final_recommendations = {
            "title": movie['title'],
            "describe": movie['describe'],
            "cover_url": movie['cover_url']
        }

        return {"main": final_recommendations, "movies": genre_movies}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(to_router)
