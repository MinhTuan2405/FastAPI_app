from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
from .database import engine
from app.routers import post, user, authentication, votes

# models.Base.metadata.create_all (bind = engine)

origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get ("/")
def mess ():
    return "hello world"

app.include_router (post.router,                             tags = ["POSTS"])
app.include_router (user.router,                              tags = ["USER"])
app.include_router (authentication.router,          tags = ["Authentication"])
app.include_router (votes.router,                            tags = ["VOTES"])


# 'tag' group all the router of post or user into seperate group


