# File: routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
from models import User
from schemas.response import UserResponse, UserResponseWithBlogs
from typing import List
from .auth import verify_token, get_current_user

router = APIRouter(prefix="/users", tags=["users"])





@router.get("/list_all_users", response_model=List[UserResponse],  dependencies=[Depends(verify_token)])
async def get_users(db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    # Check if the current user is an admin
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
    
    users = db.query(User).all()
    return users



# Update the get_user endpoint
@router.get("/list_a_user/{user_id}", response_model=UserResponseWithBlogs , dependencies=[Depends(verify_token)])
async def get_user(user_id: int, db: Session = Depends(database.get_db) , current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    print("user " ,user.username)
    print("current user " ,current_user.username)
    if user.username != current_user.username:
        raise HTTPException(status_code=404, detail="Not permitted to get other user details!!")    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Fetch latest 5 blogs for the user
    latest_blogs = []
    for blog in user.blogs[:5]:
        latest_blogs.append({"title": blog.title, "content": blog.content})

    return {"id": user.id, "username": user.username, "latest_blogs": latest_blogs}
