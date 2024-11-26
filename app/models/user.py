from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models import *

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    tasks = relationship("Task", back_populates="user")

from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))

