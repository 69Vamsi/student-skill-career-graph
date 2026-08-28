from sqlalchemy import Column, Integer, String

from app.database import Base


class CareerDB(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)