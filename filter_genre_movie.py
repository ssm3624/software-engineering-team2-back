from fastapi import HTTPException

import random
import time

def filter_movies_by_genre(movies_data, genre):
    filtered_movies = [movie for movie in movies_data if genre.lower() in [g.lower() for g in movie['genres']]]
    if not filtered_movies:
        raise HTTPException(status_code=404, detail=f"No movies found for the genre: {genre}")
    
    return random.sample(filtered_movies, min(20, len(filtered_movies)))