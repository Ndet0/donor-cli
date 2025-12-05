from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


# ---------------------------------------------------------
# Donor Model
# Each donor can have MANY donations
# ---------------------------------------------------------
class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Relationship: donor -> donations
    donations = relationship("Donation", back_populates="donor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Donor id={self.id} name='{self.name}'>"


# ---------------------------------------------------------
# Campaign Model
# Each campaign can have MANY donations
# ---------------------------------------------------------
class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    # Relationship: campaign -> donations
    donations = relationship("Donation", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campaign id={self.id} title='{self.title}'>"


# ---------------------------------------------------------
# Donation Model
# Links donor -> campaign
# ---------------------------------------------------------
class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Foreign keys
    donor_id = Column(Integer, ForeignKey("donors.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))

    # Relationships
    donor = relationship("Donor", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")

    def __repr__(self):
        return f"<Donation id={self.id} amount={self.amount}>"
