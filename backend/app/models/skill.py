from pydantic import BaseModel


class Skill(BaseModel):
    name: str
    category: str
    level: str


class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    level: str

    class Config:
        from_attributes = True