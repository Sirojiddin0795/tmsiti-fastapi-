from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, user, news, regulations, institute, activity, contact, admin
from app.middlewares.language import LanguageMiddleware
from app.db.database import engine, Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TMSITI API",
    description="Technical Standardization and Research Institute API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Language middleware
app.add_middleware(LanguageMiddleware)

# Static files
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/default", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(news.router, prefix="/api/v1/news", tags=["News"])
app.include_router(regulations.router, prefix="/api/v1/regulations", tags=["Regulations"])
app.include_router(institute.router, prefix="/api/v1/institute", tags=["Institute"])
app.include_router(activity.router, prefix="/api/v1/activity", tags=["Activity"])
app.include_router(contact.router, prefix="/api/v1/contact", tags=["Contact"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "TMSITI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
