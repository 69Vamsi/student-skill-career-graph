
"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.errors import register_exception_handlers

# Import models so SQLAlchemy registers their tables
from app.models import student_db
from app.models import skill_db
from app.models import student_skill_db
from app.models import career_db
from app.models import career_skill_db

# Import routers
from app.routers import (
    health,
    students,
    skills,
    student_skills,
    careers,
    career_skills,
    recommendations
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Student Skill & Career Graph.",
    version="0.1.0",
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register global exception handlers
register_exception_handlers(app)


# Register API routers
app.include_router(health.router)
app.include_router(students.router)
app.include_router(skills.router)
app.include_router(student_skills.router)
app.include_router(careers.router)
app.include_router(career_skills.router)
app.include_router(recommendations.router)

