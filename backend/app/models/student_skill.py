from pydantic import BaseModel


class StudentSkill(BaseModel):
    student_id: int
    skill_id: int
    level: int = 1


class StudentSkillResponse(BaseModel):
    id: int
    student_id: int
    skill_id: int
    level: int

    class Config:
        from_attributes = True