# File: routers/blogs.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database  
from models import Blog, User
from schemas.blogs import BlogCreate
from schemas.response import BlogResponse, UserResponse, SingleBlogResponse
from .auth import verify_token, oauth2_scheme, get_current_user
from typing import List
from settings import SECRET_KEY, ALGORITHM
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import database
from jose import jwt, JWTError


router = APIRouter(prefix="/blogs", tags=["blogs"])


# Function to get current user from JWT token
    
    
        

@router.post("/create_blog", response_model=BlogResponse, dependencies=[Depends(verify_token)])
async def create_blog(blog: BlogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    db_blog = Blog(title=blog.title, content=blog.content, user_id=current_user.id)  # Use current user's ID
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)  # Refresh the database object to get the user associated with the blog
    # Fetch the author details from the current user
    author_details = UserResponse(id=current_user.id, username=current_user.username)
    return BlogResponse(id=db_blog.id, title=db_blog.title, content=db_blog.content, author_info=author_details)



# Update the get_blogs endpoint to use the new response model
@router.get("/list_all_blogs", tags=["blogs"], dependencies=[Depends(verify_token)])
async def get_blogs(db: Session = Depends(database.get_db) , current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
    blogs = db.query(Blog).all()
    # Construct a list of BlogListResponse objects for each, blog
    blogs_response = []
    for blog in blogs:
        author_username = blog.owner.username  # Fetch the author's username from the associated User object
        blogs_response.append(SingleBlogResponse(id=blog.id, title=blog.title, content=blog.content, author_username=author_username))
    return blogs_response


@router.get("list_a_blog/{blog_id}", response_model=SingleBlogResponse, tags=["blogs"], dependencies=[Depends(verify_token)] )
async def get_blog(blog_id: int, db: Session = Depends(database.get_db) , current_user: User = Depends(get_current_user)):
    
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    author_info = blog.owner.username
    if author_info != current_user.username:
        raise HTTPException(status_code=403, detail="Cant access a blog that you havent written!!")    
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    author_info = blog.owner.username
    return SingleBlogResponse(id = blog.id, title = blog.title, content = blog.content, author_username = author_info)

