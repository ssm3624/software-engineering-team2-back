import requests
from fastapi import FastAPI

app = FastAPI()

# TMDb API 설정
API_KEY = "349ca079de9b470216f101783433c085"
BASE_URL = "https://api.themoviedb.org/3/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # w500은 이미지 크기를 지정

@app.get("/get-movie-poster/{tmdb_id}")
async def get_movie_poster(tmdb_id: str):
    response = requests.get(f"{BASE_URL}/{tmdb_id}", params={"api_key": API_KEY})
    data = response.json()
    poster_path = data.get('poster_path', None)
    if poster_path:
        poster_url = f"{IMAGE_BASE_URL}{poster_path}"
        return {poster_url}
    else:
        return {"error": "Poster not found"}