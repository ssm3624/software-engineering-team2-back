from fastapi import FastAPI
from fastapi import APIRouter
from Main_genre import to_router
from genre import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://heung115.iptime.org:8008","*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
# async def root():
def root():
    return {"message": "Hello World"}


@app.get("/home")
def home():
    return {"message": "home"}

app.include_router(router=router)
app.include_router(router=to_router)