from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    tasks = relationship('Tasks', back_populates='owner')


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_by = relationship('User')
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    owner = relationship('User', back_populates='tasks')
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

