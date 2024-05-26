'''from collections import defaultdict
from fastapi import FastAPI, HTTPException, APIRouter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from connectDB import get_supabase
from describe import get_movie_overview
from Post import get_movie_poster
import random
import time


from preprocess import get_genre
from Pre_Movie import get_movie
from Pre_UserID import get_userid

app = FastAPI()
to_router = APIRouter()
supabase = get_supabase()

TEST_USER_ID = get_userid()

def fetch_movies():
    return supabase.table("Movies_Table").select("title, movieId, genres").execute().data

def fetch_links():
    return supabase.table("Links_Table").select("movieId, imdbId, tmdbId").execute().data

def fetch_ratings():
    return supabase.table("Ratings_Table").select("movieId, rating").execute().data

def fetch_user_data():
    return supabase.table("Users_Table").select("UserId, UserTags").eq("UserId", TEST_USER_ID).execute().data

def fetch_tags(movie_id):
    return supabase.table("Tags_Table").select("tag").eq("movieId", movie_id).execute().data

@to_router.get("/get-movie-list/{genre}")
async def recommend_movies(genre: str):
    random.seed(time.time())
    try:
        # 필요한 데이터 로드
        movies_data = fetch_movies()
        links_data = fetch_links()
        ratings_data = fetch_ratings()
        user_data = fetch_user_data()

        if not movies_data or not links_data or not ratings_data:
            raise HTTPException(status_code=404, detail="Data not found")

        ratings_dict = {item['movieId']: item['rating'] for item in ratings_data}
        links_dict = {item['movieId']: {'imdbId': item['imdbId'], 'tmdbId': item['tmdbId']} for item in links_data}

        # 장르에 해당하는 영화 필터링 및 랜덤 샘플링
        filtered_movies = [movie for movie in movies_data if genre.lower() in map(str.lower, movie['genres'].split('|'))]
        if not filtered_movies:
            raise HTTPException(status_code=404, detail=f"No movies found for the genre: {genre}")

        filtered_movies = random.sample(filtered_movies, min(20, len(filtered_movies)))

        genre_movies = [
            {
                "title": movie['title'],
                "cover_url": get_movie_poster(links_dict[movie['movieId']]['tmdbId']),
                "scope": ratings_dict.get(movie['movieId'], 5)
            } for movie in filtered_movies if movie['movieId'] in links_dict
        ]

        if not user_data or not user_data[0]['UserTags']:
            possible_tags = ['Comedy', 'Romance', 'Horror', 'Action', 'Thriller', 'Drama']
            random_tags = random.sample(possible_tags, 2)
            supabase.table("Users_Table").insert({
                "UserId": TEST_USER_ID,
                "UserStack": '1',
                "UserTags": random_tags[0]
            }).execute()
            supabase.table("Users_Table").insert({
                "UserId": TEST_USER_ID,
                "UserStack": '1',
                "UserTags": random_tags[1]
            }).execute()
            user_data = fetch_user_data()

        user_tags_string = ' '.join([row['UserTags'] for row in user_data]).strip()
        if not user_tags_string:
            raise HTTPException(status_code=400, detail="User tags are empty")

        # TF-IDF 벡터화
        vectorizer = TfidfVectorizer(stop_words=None, token_pattern=r'\b\w+\b')
        user_tfidf = vectorizer.fit_transform([user_tags_string])

        recommended_movies = []
        for movie in filtered_movies:
            movie_id = movie['movieId']
            tags_data = fetch_tags(movie_id)
            if tags_data:
                movie_tags_string = ' '.join(row['tag'] for row in tags_data)
                movie_tfidf = vectorizer.transform([movie_tags_string])
                similarity_score = cosine_similarity(user_tfidf, movie_tfidf)[0][0]
                
                movie_title = movie['title']
                tmdb_id = links_dict[movie_id]['tmdbId']

                recommended_movies.append({
                    "title": movie_title,
                    "describe": get_movie_overview(tmdb_id),
                    "cover_url": get_movie_poster(tmdb_id),
                    "similarity_score": round(similarity_score, 3)
                })

        # 유사도 순으로 정렬 후 상위 10개 영화 선택
        recommended_movies.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        
        movie = recommended_movies[0]

        final_recommendations = {
            "title": movie['title'],
            "describe": movie['describe'],
            "cover_url": movie['cover_url']
        }

        return {"main": final_recommendations, "movies": genre_movies}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(to_router)'''