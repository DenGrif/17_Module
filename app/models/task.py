from sqlalchemy import Integer
from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.models import *

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    priority = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='tasks')
