from connectDB import get_supabase
from fastapi import FastAPI, APIRouter

router = APIRouter()

app = FastAPI()

@router.get("/genre")
async def get_genre():
  db = get_supabase()
  response =   db.table('Movies_Table').select('genres').execute()

  genres = set()

  for data in response.data:
      genres |= set(data['genres'].split("|"))

  genres = sorted(genres)

  return { "genre": genres}