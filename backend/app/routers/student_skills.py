from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student_skill import (
    StudentSkill,
    StudentSkillResponse
)
from app.models.student_skill_db import StudentSkillDB
from app.models.student_db import StudentDB
from app.models.skill_db import SkillDB


router = APIRouter(
    prefix="/student-skills",
    tags=["student-skills"]
)


@router.get("/", response_model=list[StudentSkillResponse])
def get_student_skills(
    db: Session = Depends(get_db)
):
    return db.query(StudentSkillDB).all()


@router.post("/", response_model=StudentSkillResponse)
def create_student_skill(
    student_skill: StudentSkill,
    db: Session = Depends(get_db)
):

    # Check student exists
    student = db.query(StudentDB).filter(
        StudentDB.id == student_skill.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check skill exists
    skill = db.query(SkillDB).filter(
        SkillDB.id == student_skill.skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    # Check duplicate relationship
    existing = db.query(StudentSkillDB).filter(
        StudentSkillDB.student_id == student_skill.student_id,
        StudentSkillDB.skill_id == student_skill.skill_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Student already has this skill"
        )

    new_student_skill = StudentSkillDB(
        student_id=student_skill.student_id,
        skill_id=student_skill.skill_id,
        level=student_skill.level
    )

    db.add(new_student_skill)
    db.commit()
    db.refresh(new_student_skill)

    return new_student_skill