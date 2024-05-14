from collections import defaultdict
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from connectDB import get_supabase
import random
import time


app = FastAPI()
supabase = get_supabase()


TEST_USER_ID = None  #테스트용 유저 아이디

@app.get("/recommend-movies/")
def recommend_movies():
        #-----------------------------무작위 장르의 영화들 나열-------------------------------
        random.seed(time.time())
    
        try:
            # 모든 영화와 링크 정보를 한 번에 로드
            movies_data = supabase.table("Movies Table").select("title, movieId, genres").execute().data
            if not movies_data:
                raise HTTPException(status_code=404, detail="No movies data found")

            links_data = supabase.table("Links Table").select("movieId, imdbId, tmdbId").execute().data
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
                genre_movies = [{"title": movie['title'],
                                "imdbLink": f"https://www.imdb.com/title/tt0{links_dict[movie['movieId']]['imdbId']}",
                                "PosterLink": f"http://127.0.0.1:8000/get-movie-poster/{links_dict[movie['movieId']]['tmdbId']}"} 
                                for movie in selected_movies]
                movies[genre] = {"genre": genre, "movies": genre_movies}


            if TEST_USER_ID is None:
                return movies

            #-----------------------------태그를 이용한 영화 추천-------------------------------

            # 유저의 태그들을 가져옴
            user_data = supabase.table("Users Table").select("UserId, UserTags").eq("UserId", TEST_USER_ID).execute()
            
            # 유저 태그 데이터가 없거나 태그가 비어 있는 경우
            if not user_data.data or not user_data.data[0]['UserTags']:
                # 랜덤 태그 선택
                possible_tags = ['Comedy', 'Romance', 'Horror', 'Action', 'Thriller', 'Drama']
                random_tags = random.sample(possible_tags, 2)  # 랜덤으로 2개 태그 추출

                # Users 테이블에 태그 정보 삽입
                update_response = supabase.table("Users Table").insert({
                    "UserId" : TEST_USER_ID,
                    "UserStack": '1',
                    "UserTags": random_tags[0]
                }).execute()

                update_response = supabase.table("Users Table").insert({
                    "UserId" : TEST_USER_ID,
                    "UserStack": '1',
                    "UserTags": random_tags[1]
                }).execute()

                # 업데이트된 데이터 다시 가져오기
                user_data = supabase.table("Users Table").select("UserId, UserTags").eq("UserId", TEST_USER_ID).execute()

            #가져온 태그들을 한줄로 저장
            user_tags_agg = defaultdict(str)
            for row in user_data.data:
                user_tags_agg[row['UserId']] += row.get('UserTags', []) + ' '

            if TEST_USER_ID not in user_tags_agg:
                raise HTTPException(status_code=404, detail="User tags for the given ID are empty")
            

            user_tags_string = ' '.join(user_tags_agg.values()).strip()
            if not user_tags_string:
                raise HTTPException(status_code=400, detail="User tags contain only invalid characters or are empty")


            # 문자들 벡터화
            vectorizer = TfidfVectorizer(stop_words=None, token_pattern=r'\b\w+\b')
            user_tfidf = vectorizer.fit_transform([user_tags_string])
            
            recommended_movies = []
            
            # 코사인 유사도 계산할 무작위 영화 id 100개 선정 (1~500 movieId)
            movie_ids = random.sample(range(1, 501), 100)
            
            movie_R = {}
            #무작위 영화100개의 Tag들을 가져옴.
            for movie1 in movie_ids:
                tags_data = supabase.table("Tags Table").select("tag").eq("movieId", movie1).execute()
                if tags_data.data:
                    movie_tags_string = ' '.join(row['tag'] for row in tags_data.data)
                    movie_tfidf = vectorizer.transform([movie_tags_string])
                    #벡터화 시킨 유저태그와 영화 태그를 코사인 유사도 계산
                    similarity_score = cosine_similarity(user_tfidf, movie_tfidf)[0][0]

                    #간단히 정리하자면 유저의 태그가 영화 태그에서 몇번 언급되어있나를 계산. (태그가 많을수록 유리함.)

                    #유사도 0인 관련 없는 영화들 제외
                    if (similarity_score != 0 ):
                        movies_data = supabase.table("Movies Table").select("title").eq("movieId", movie1).execute()
                        if not movies_data:
                            raise HTTPException(status_code=404, detail="No movies data found")

                        links_data = supabase.table("Links Table").select("imdbId, tmdbId").eq("movieId", movie1).execute()
                        if not links_data:
                            raise HTTPException(status_code=404, detail="No links data found")
                        
                        movie_title = movies_data.data[0]['title'] if movies_data.data else "Title Not Found"
                        imdb_id = links_data.data[0]['imdbId'] if links_data.data else "IMDb Not Found"
                        tmdb_id = links_data.data[0]['tmdbId'] if links_data.data else "TMDb Not Found"

                        recommended_movies.append({
                            "title": movie_title,
                            "imdbLink": f"https://www.imdb.com/title/tt0{imdb_id}",
                            "PosterLink":  f"http://127.0.0.1:8000/get-movie-poster/{tmdb_id}",

                            "similarity_score": round(similarity_score, 3)
                            

                            #,"user_tags": user_tags_string, # 테스트용 태그 출력
                            #"movie_tags": movie_tags_string 
                            #,"movie_id" : movie

                        })

            # 계산한 유사도 크기순 정렬
            recommended_movies.sort(key=lambda x: x['similarity_score'], reverse=True)

            top_10_recommended = recommended_movies[:10]  # 상위 10개 항목 추출

            return {"recommended_movies": top_10_recommended
                    ,"genre_movies": movies}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))