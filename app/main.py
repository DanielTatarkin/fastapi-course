import os
import psycopg2

from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from dotenv import load_dotenv
from time import sleep
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .database import engine, get_db

load_dotenv("database.env")


"""Latest hhttps://youtu.be/0sOvCWFmrtA?t=21008"""

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        timeout = 2
        print("Connection to DB failed:")
        print(f"Error: {error}")
        print(f"Retrying in {timeout} seconds...")
        sleep(timeout)


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Using formatted string here would pose risk of SQL injection
    # - the following parameterized query is best practice
    # cursor.execute("""
    #                 INSERT INTO posts (title, content, published)
    #                 VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published)
    #                )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve what we created back into new_post variable

    return new_post


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    post = cursor.fetchone()

    return post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post with id: {id}",
        )

    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_q = db.query(models.Post).filter(models.Post.id == id)

    if post_q.first():
        post_q.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post with id: {id}",
        )


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_q = db.query(models.Post).filter(models.Post.id == id)
    original_post = post_q.first()

    if not original_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post with id: {id}",
        )
    post_q.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_q.first()
