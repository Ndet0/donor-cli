from sqlalchemy.orm import Session
from .models import Donor, Donation, Campaign


# ---------------------------------------------------------
# DONOR CRUD
# ---------------------------------------------------------

def create_donor(db: Session, name: str, email: str):
    donor = Donor(name=name, email=email)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


def get_all_donors(db: Session):
    return db.query(Donor).all()


def find_donor_by_id(db: Session, donor_id: int):
    return db.query(Donor).filter(Donor.id == donor_id).first()


def delete_donor(db: Session, donor_id: int):
    donor = find_donor_by_id(db, donor_id)
    if donor:
        db.delete(donor)
        db.commit()
        return True
    return False


# ---------------------------------------------------------
# CAMPAIGN CRUD
# ---------------------------------------------------------

def create_campaign(db: Session, title: str, description: str):
    campaign = Campaign(title=title, description=description)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def get_all_campaigns(db: Session):
    return db.query(Campaign).all()


def find_campaign_by_id(db: Session, campaign_id: int):
    return db.query(Campaign).filter(Campaign.id == campaign_id).first()


def delete_campaign(db: Session, campaign_id: int):
    campaign = find_campaign_by_id(db, campaign_id)
    if campaign:
        db.delete(campaign)
        db.commit()
        return True
    return False


# ---------------------------------------------------------
# DONATION CRUD
# ---------------------------------------------------------

def create_donation(db: Session, amount: float, donor_id: int, campaign_id: int):
    donation = Donation(amount=amount, donor_id=donor_id, campaign_id=campaign_id)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation


def get_all_donations(db: Session):
    return db.query(Donation).all()


def get_donations_by_donor(db: Session, donor_id: int):
    return db.query(Donation).filter(Donation.donor_id == donor_id).all()


def get_donations_by_campaign(db: Session, campaign_id: int):
    return db.query(Donation).filter(Donation.campaign_id == campaign_id).all()
