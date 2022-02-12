from sqlalchemy import Column, DateTime, func, SmallInteger, String
from sqlalchemy.orm import validates

from database import Base


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    email = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    @validates('email')
    def validate_name(self, key, email):
        if type(email) is not str:
            raise TypeError

        if len(email) > 64:
            raise ValueError

        return email
