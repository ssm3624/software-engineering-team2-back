from connectDB import get_supabase
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

supabase = get_supabase()
app = FastAPI()

@app.post("/insert-tag/")
async def insert_tag(request: Request):
    try:
        #data = 사용자가 영화 링크 접속했을 때 title 값 
        data = await request.json()
        user_id = data.get("UserId")
        movie_genres = supabase.table("Movies Table").select("genres").eq("title", data).execute().data
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required.")

        if not movie_genres:
            raise HTTPException(status_code=400, detail="Movie genres are required.")

        for genre in movie_genres:
            # 이미 같은 사용자 ID와 영화 장르가 있는지 확인
            existing_data = supabase.table("Users Table").select("*").eq("UserId", user_id).eq("UserTags", genre).execute()

            if existing_data.data:
                # 이미 같은 사용자 ID와 영화 장르가 있으면 그 장르의 UserStack 증가
                user_stack = existing_data.data[0]["UserStack"] + 1

                # Users 테이블 업데이트
                update_response = supabase.table("Users Table").update({"UserStack": user_stack}).eq("UserId", user_id).eq("UserTags", genre).execute()

            else:
                # 같은 사용자 ID와 영화 장르가 없으면 새로운 데이터 삽입
                insert_response = supabase.table("Users Table").insert({
                    "UserId": user_id,
                    "UserTags": genre,
                    "UserStack": 1
                }).execute()

        return {"message": "Tags inserted successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))