from fastapi import FastAPI, APIRouter
from preprocess import get_genre


router = APIRouter()

app = FastAPI()

@router.get("/genre")
async def get_Allgenre():
  response = get_genre()

  return { "genre": response}