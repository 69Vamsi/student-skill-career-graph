
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.skill import Skill, SkillResponse
from app.models.skill_db import SkillDB


router = APIRouter(
    prefix="/skills",
    tags=["skills"]
)


# GET all skills
@router.get("/", response_model=List[SkillResponse])
def get_skills(
    db: Session = Depends(get_db)
):
    skills = db.query(SkillDB).all()
    return skills


# POST create a new skill
@router.post("/", response_model=SkillResponse)
def create_skill(
    skill: Skill,
    db: Session = Depends(get_db)
):
    # Check if skill already exists
    existing_skill = db.query(SkillDB).filter(
        SkillDB.name == skill.name,
        SkillDB.category == skill.category
    ).first()

    if existing_skill:
        raise HTTPException(
            status_code=409,
            detail="Skill already exists"
        )

    new_skill = SkillDB(
        name=skill.name,
        category=skill.category,
        level=skill.level
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


# DELETE skill
@router.delete("/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    skill = db.query(SkillDB).filter(
        SkillDB.id == skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    db.delete(skill)
    db.commit()

    return {
        "message": "Skill deleted successfully"
    }

