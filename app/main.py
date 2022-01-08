from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

"""Latest https://youtu.be/0sOvCWFmrtA?t=7288"""


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


MY_POSTS = [{"title": "Title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "Title of post 2", "content": "content of post 2", "id": 2}]


def find_post(id):
    for post in MY_POSTS:
        if post['id'] == id:
            return post

def modify_post(id, updated_post):
    for i,post in enumerate(MY_POSTS):
        if post['id'] == id:
            MY_POSTS[i] = updated_post
            MY_POSTS[i]['id'] = id
            print(MY_POSTS)


def find_index_post(id):
    for i,post in enumerate(MY_POSTS):
        if post['id'] == id:
            return i
    return None


def remove_post(id):
    for i, post in enumerate(MY_POSTS):
        if post['id'] == id:
            MY_POSTS.pop(i)
            return True
    return False


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {
        "data": MY_POSTS
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    MY_POSTS.append(post_dict)
    return {"post": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post with id: {id}")


@app.get("/posts/latest")
def get_latest_post():
    post = MY_POSTS[-1]
    return {
        "data": post
    }


@app.delete("/posts/{id}")
def delete_post(id: int):
    if remove_post(id):
        Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post with id: {id}")


@app.put("/posts/{id}" )
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post with id: {id}")

    post_dict = post.dict()
    post_dict['id'] = id
    MY_POSTS[index] = post_dict
    return {"data": post_dict}
