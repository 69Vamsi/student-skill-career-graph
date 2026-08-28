from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.career_skill import CareerSkill, CareerSkillResponse
from app.models.career_skill_db import CareerSkillDB
from app.models.career_db import CareerDB
from app.models.skill_db import SkillDB


router = APIRouter(
    prefix="/career-skills",
    tags=["career-skills"]
)


# GET all career-skill relationships
@router.get("/", response_model=List[CareerSkillResponse])
def get_career_skills(
    db: Session = Depends(get_db)
):
    return db.query(CareerSkillDB).all()


# POST create career-skill relationship
@router.post("/", response_model=CareerSkillResponse)
def create_career_skill(
    career_skill: CareerSkill,
    db: Session = Depends(get_db)
):

    # Check career exists
    career = db.query(CareerDB).filter(
        CareerDB.id == career_skill.career_id
    ).first()

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    # Check skill exists
    skill = db.query(SkillDB).filter(
        SkillDB.id == career_skill.skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    # Check duplicate relationship
    existing = db.query(CareerSkillDB).filter(
        CareerSkillDB.career_id == career_skill.career_id,
        CareerSkillDB.skill_id == career_skill.skill_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Career already has this skill"
        )

    # Create relationship
    new_career_skill = CareerSkillDB(
        career_id=career_skill.career_id,
        skill_id=career_skill.skill_id,
        importance=career_skill.importance
    )

    db.add(new_career_skill)
    db.commit()
    db.refresh(new_career_skill)

    return new_career_skill