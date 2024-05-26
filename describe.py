'''import requests
from fastapi import FastAPI
from starlette.config import Config

app = FastAPI()

config = Config('.env')

# TMDb API 설정
API_KEY = config('Post_API_KEY')
BASE_URL = config('Post_BASE_URL')

def get_movie_overview(tmdb_id: str):    
    response = requests.get(f"{BASE_URL}/{tmdb_id}", params={"api_key": API_KEY}) 
    data = response.json()
    overview_path = data.get("overview", None)       

    if overview_path:
        return overview_path
    else:
        
        return {"error": "Poster not found"}'''