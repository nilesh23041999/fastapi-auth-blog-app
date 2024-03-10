from pydantic import BaseModel
from typing import Optional
from typing import List, Dict


class UserResponseWithBlogs(BaseModel):
    id: int
    username: str
    latest_blogs: List[Dict[str, str]]



class UserResponse(BaseModel):
    id: int
    username: str
    


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author_info: UserResponse
    
        
    

class SingleBlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author_username: str
    
    
