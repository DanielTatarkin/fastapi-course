from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


MY_POSTS = [{"title": "Title of post 1", "content": "content of post 1", "id": 1}, {"title": "Title of post 2", "content": "content of post 2", "id": 2}]


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {
        "data": MY_POSTS
    }


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    MY_POSTS.append(post_dict)
    return {"post": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    for post in MY_POSTS:
        if post['id'] == id:
            return post
    
    return {
        "message": f"Could not find post with id: {id}"
    }