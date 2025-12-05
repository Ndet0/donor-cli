# src/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, validates
from datetime import datetime

from .db import Base

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, unique=True)
    email = Column(String(255), unique=True, nullable=False)

    donations = relationship("Donation", back_populates="donor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Donor id={self.id} name='{self.name}'>"

    # validations 
    @validates("name")
    def _validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Donor name must not be empty")
        return value.strip()

    @validates("email")
    def _validate_email(self, key, value):
        if not value or "@" not in value:
            raise ValueError("Provide a valid email address")
        return value.strip().lower()

    # ORM helpers 
    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.name).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_attr(cls, session, **kwargs):
        return session.query(cls).filter_by(**kwargs).all()

    def delete(self, session):
        session.delete(self)
        session.commit()


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    donations = relationship("Donation", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campaign id={self.id} title='{self.title}'>"

    @validates("title")
    def _validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Campaign title must not be empty")
        return value.strip()

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.title).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_attr(cls, session, **kwargs):
        return session.query(cls).filter_by(**kwargs).all()

    def delete(self, session):
        session.delete(self)
        session.commit()


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    donor = relationship("Donor", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")

    def __repr__(self):
        return f"<Donation id={self.id} amount={self.amount}>"

    @validates("amount")
    def _validate_amount(self, key, value):
        if value is None:
            raise ValueError("Donation amount required")
        try:
            val = float(value)
        except Exception:
            raise ValueError("Amount must be numeric")
        if val <= 0:
            raise ValueError("Amount must be greater than zero")
        return val
