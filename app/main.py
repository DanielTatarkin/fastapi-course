from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from dotenv import load_dotenv

import os
from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv('database.env')

app = FastAPI()

"""Latest https://youtu.be/0sOvCWFmrtA?t=16279"""


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        timeout = 2
        print("Connection to DB failed:")
        print(f"Error: {error}")
        print(f"Retrying in {timeout} seconds...")
        sleep(timeout)


MY_POSTS = [{"title": "Title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "Title of post 2", "content": "content of post 2", "id": 2}]


def find_post(id):
    for post in MY_POSTS:
        if post['id'] == id:
            return post


def modify_post(id, updated_post):
    for i, post in enumerate(MY_POSTS):
        if post['id'] == id:
            MY_POSTS[i] = updated_post
            MY_POSTS[i]['id'] = id
            print(MY_POSTS)


def find_index_post(id):
    for i, post in enumerate(MY_POSTS):
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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {
        "data": posts
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Using formatted string here would pose risk of SQL injection
    # - the following parameterized query is best practice
    cursor.execute("""
                    INSERT INTO posts (title, content, published)
                    VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published)
                   )
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    post = cursor.fetchone()

    return {"post_detail": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post with id: {id}")

    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post with id: {id}")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post with id: {id}")
    return {"post_detail": updated_post}
