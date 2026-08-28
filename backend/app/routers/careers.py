from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.career import Career, CareerResponse
from app.models.career_db import CareerDB


router = APIRouter(
    prefix="/careers",
    tags=["careers"]
)


# GET all careers
@router.get("/", response_model=List[CareerResponse])
def get_careers(
    db: Session = Depends(get_db)
):
    careers = db.query(CareerDB).all()
    return careers


# GET career by ID
@router.get("/{career_id}", response_model=CareerResponse)
def get_career(
    career_id: int,
    db: Session = Depends(get_db)
):
    career = db.query(CareerDB).filter(
        CareerDB.id == career_id
    ).first()

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    return career


# POST create a new career
@router.post("/", response_model=CareerResponse)
def create_career(
    career: Career,
    db: Session = Depends(get_db)
):
    new_career = CareerDB(
        title=career.title,
        description=career.description
    )

    db.add(new_career)
    db.commit()
    db.refresh(new_career)

    return new_career


# DELETE career
@router.delete("/{career_id}")
def delete_career(
    career_id: int,
    db: Session = Depends(get_db)
):
    career = db.query(CareerDB).filter(
        CareerDB.id == career_id
    ).first()

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    db.delete(career)
    db.commit()

    return {
        "message": "Career deleted successfully"
    }