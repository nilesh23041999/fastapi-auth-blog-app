# File: main.py

from fastapi import FastAPI
from routers import auth, users, blogs
from database import engine, Base

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

