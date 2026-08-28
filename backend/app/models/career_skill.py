from pydantic import BaseModel


class CareerSkill(BaseModel):
    career_id: int
    skill_id: int
    importance: int = 1


class CareerSkillResponse(CareerSkill):
    id: int

    class Config:
        from_attributes = True