from pydantic import BaseModel


class Career(BaseModel):
    title: str
    description: str | None = None


class CareerResponse(Career):
    id: int

    class Config:
        from_attributes = True