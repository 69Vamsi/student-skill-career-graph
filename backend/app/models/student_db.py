
from sqlalchemy import Column, Integer, String

from app.database import Base


class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    college = Column(String(200), nullable=False)
    degree = Column(String(100), nullable=False)
    branch = Column(String(100), nullable=False)
    graduation_year = Column(Integer, nullable=False)

