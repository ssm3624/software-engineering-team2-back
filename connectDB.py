from supabase import create_client, Client
from starlette.config import Config
from fastapi import APIRouter


router = APIRouter()

def get_supabase():

    config = Config('.env')

    SUPABASE_URL = config('SUPABASE_URL')  # 여기에 Supabase 프로젝트 URL 입력
    SUPABASE_KEY = config('SUPABASE_API')
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    return supabase