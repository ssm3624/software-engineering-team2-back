from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from connectDB import get_supabase
from fastapi import RedirectResponse
import random
import time

app = FastAPI()
# Supabase 설정
supabase = get_supabase()

@app.get("/No_Login_movies/")
async def random_genre_movies():
    random.seed(time.time())
    
    try:
        # 모든 영화와 링크 정보를 한 번에 로드
        movies_data = supabase.table("movies").select("title, movieId, genres").execute().data
        if not movies_data:
            raise HTTPException(status_code=404, detail="No movies data found")

        links_data = supabase.table("links").select("movieId, imdbId, tmdbId").execute().data
        if not links_data:
            raise HTTPException(status_code=404, detail="No links data found")

        # movieId를 키로 하여 imdbId와 tmdbId를 빠르게 찾을 수 있는 사전 생성
        links_dict = {item['movieId']: {'imdbId': item['imdbId'], 'tmdbId': item['tmdbId']}
                      for item in links_data if 'imdbId' in item and 'tmdbId' in item}

        # 장르 리스트 생성
        genres_list = set()
        for movie in movies_data:
            if movie['genres']:
                genres_list.update(movie['genres'].split('|'))
        if not genres_list:
            raise HTTPException(status_code=404, detail="No genres found")

        # 무작위 장르 선택
        random_genres = random.sample(list(genres_list), k=min(10, len(genres_list)))

        # 선택된 장르에 해당하는 영화 타이틀과 imdbId 및 tmdbId 검색
        movies = {}
        for genre in random_genres:
            # 장르에 해당하는 모든 영화 리스트
            filtered_movies = [movie for movie in movies_data if genre in movie.get('genres', '') and movie['movieId'] in links_dict]
            if not filtered_movies:
                continue  # 해당 장르의 영화가 없는 경우 스킵

            # 랜덤으로 영화 선택
            selected_movies = random.sample(filtered_movies, min(len(filtered_movies), 10))

            # 선택된 영화 정보 구성
            genre_movies = [{"title": movie['title'], "imdbId": links_dict[movie['movieId']]['imdbId'],
                             "tmdbId": links_dict[movie['movieId']]['tmdbId'],
                             "imdbLink": f"https://www.imdb.com/title/tt0{links_dict[movie['movieId']]['imdbId']}",
                             "PosterLink": f"http://127.0.0.1:8000/get-movie-poster/{links_dict[movie['movieId']]['tmdbId']}"} 
                            for movie in selected_movies]
            movies[genre] = {"genre": genre, "movies": genre_movies}

        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))