from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student_db import StudentDB
from app.models.student_skill_db import StudentSkillDB
from app.models.skill_db import SkillDB
from app.models.career_db import CareerDB
from app.models.career_skill_db import CareerSkillDB


router = APIRouter(
    prefix="/students",
    tags=["recommendations"]
)


@router.get("/{student_id}/career-recommendations")
def get_career_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):

    # ---------------------------------------
    # Check student exists
    # ---------------------------------------
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # ---------------------------------------
    # Get student's skills
    # ---------------------------------------
    student_skills = db.query(StudentSkillDB).filter(
        StudentSkillDB.student_id == student_id
    ).all()

    if not student_skills:
        return []

    # skill_id -> student level
    student_skill_levels = {
        item.skill_id: item.level
        for item in student_skills
    }

    # ---------------------------------------
    # Get all careers
    # ---------------------------------------
    careers = db.query(CareerDB).all()

    recommendations = []

    for career in careers:

        # Get skills required for this career
        career_skills = db.query(CareerSkillDB).filter(
            CareerSkillDB.career_id == career.id
        ).all()

        if not career_skills:
            continue

        total_importance = 0
        achieved_score = 0

        matched_skills = []

        # ---------------------------------------
        # Calculate career score
        # ---------------------------------------
        for career_skill in career_skills:

            importance = career_skill.importance

            total_importance += importance

            student_level = student_skill_levels.get(
                career_skill.skill_id,
                0
            )

            # Normalize student level to 0-1
            proficiency = min(student_level / 5, 1)

            # Weighted proficiency score
            achieved_score += proficiency * importance

            # ---------------------------------------
            # Add matched skill
            # ---------------------------------------
            if student_level > 0:

                skill = db.query(SkillDB).filter(
                    SkillDB.id == career_skill.skill_id
                ).first()

                if skill:
                    matched_skills.append({
                        "skill_id": skill.id,
                        "skill_name": skill.name,
                        "student_level": student_level,
                        "importance": importance
                    })

        # ---------------------------------------
        # Skill Coverage
        # ---------------------------------------
        matched_importance = sum(
            skill["importance"]
            for skill in matched_skills
        )

        coverage_score = (
            matched_importance / total_importance
        ) * 100 if total_importance > 0 else 0

        # ---------------------------------------
        # Skill Proficiency
        # ---------------------------------------
        proficiency_score = (
            achieved_score / total_importance
        ) * 100 if total_importance > 0 else 0

        # ---------------------------------------
        # Final Match Score
        #
        # 70% Skill Coverage
        # 30% Skill Proficiency
        # ---------------------------------------
        match_percentage = (
            coverage_score * 0.70
            + proficiency_score * 0.30
        )

        recommendations.append({
            "career_id": career.id,
            "career_title": career.title,
            "description": career.description,
            "match_percentage": round(match_percentage, 2),
            "matched_skills": matched_skills
        })

    # ---------------------------------------
    # Highest match first
    # ---------------------------------------
    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations