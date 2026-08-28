
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.models.student_db import StudentDB
from app.models.student_skill_db import StudentSkillDB
from app.models.skill_db import SkillDB


router = APIRouter(
    prefix="/students",
    tags=["students"]
)


# GET all students
@router.get("/", response_model=List[Student])
def get_students(db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()
    return students


# GET student by ID
@router.get("/{student_id}", response_model=Student)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# POST create a new student
@router.post("/", response_model=Student)
def create_student(
    student: Student,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_student = db.query(StudentDB).filter(
        StudentDB.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Student with this email already exists"
        )

    new_student = StudentDB(
        name=student.name,
        email=student.email,
        college=student.college,
        degree=student.degree,
        branch=student.branch,
        graduation_year=student.graduation_year
    )

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Student with this email already exists"
        )

    return new_student


# GET student profile with skills
@router.get("/{student_id}/profile")
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db)
):
    # Find student
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Find student's skill relationships
    student_skills = db.query(StudentSkillDB).filter(
        StudentSkillDB.student_id == student_id
    ).all()

    skills = []

    for student_skill in student_skills:

        skill = db.query(SkillDB).filter(
            SkillDB.id == student_skill.skill_id
        ).first()

        if skill:
            skills.append({
                "id": skill.id,
                "name": skill.name,
                "category": skill.category,
                "level": student_skill.level
            })

    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "college": student.college,
            "degree": student.degree,
            "branch": student.branch,
            "graduation_year": student.graduation_year
        },
        "skills": skills
    }

