import requests
from fastapi import FastAPI
from starlette.config import Config

app = FastAPI()

config = Config('.env')

# TMDb API 설정
API_KEY = config('Post_API_KEY')
BASE_URL = config('Post_BASE_URL')
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

@app.get("/get-movie-poster/{tmdb_id}")
async def get_movie_poster(tmdb_id: str):    
    response = requests.get(f"{BASE_URL}/{tmdb_id}", params={"api_key": API_KEY})   #포스터 링크 API로 request 보냄
    data = response.json()
    poster_path = data.get("backdrop_path", None)       #포스터 링크 가져오기

    if poster_path:
        poster_url = f"{IMAGE_BASE_URL}{poster_path}"   #실제 포스터 링크
        return {poster_url}
    else:
        
        return {"error": "Poster not found"}