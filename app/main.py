from fastapi import FastAPI, Path, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Database connection
try:
    conn = psycopg2.connect(
        host="****",
        database="***",
        user="****",
        password="****",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")

# Get all posts
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# Get a single post by ID
@app.get("/posts/{id}")
def get_post(id: int = Path(..., description="The ID of the post to retrieve")):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"post_detail": post}

# Delete a post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_route(id: int = Path(..., description="The ID of the post to delete")):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"message": f"Post with id {id} deleted successfully"}

# Update a post by ID
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": updated_post}
