from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from routers import oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # ensure relationship is loaded before session closes
    _ = new_post.owner
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):  
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if deleted_post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised")
    
    db.delete(deleted_post)
    db.commit()

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):  
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised")
    for key, value in post.model_dump().items():
        setattr(updated_post, key, value)
    db.commit()
    db.refresh(updated_post)
    # ensure relationship is loaded before session closes
    _ = updated_post.owner
    return updated_post

@router.get("/", response_model=list[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db),
              limit:int =10,
              skip:int=0,
              search: Optional[str]=""):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # db.query(Post, votes) returns tuples, but response_model expects objects
    return [{"Post": post, "votes": votes} for post, votes in results]

