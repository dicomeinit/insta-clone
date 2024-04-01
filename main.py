from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment, like
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)
app.include_router(like.router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
def root():
    return "Hello World!"


origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')

