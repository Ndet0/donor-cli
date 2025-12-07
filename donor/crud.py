from .db import SessionLocal
from .models import Donor, Campaign, Donation
from sqlalchemy import or_


# DONOR CRUD


def create_donor(name, email):
    db = SessionLocal()
    donor = Donor(name=name, email=email)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


def list_donors():
    db = SessionLocal()
    return db.query(Donor).all()


def update_donor(db, donor_id, name=None, email=None):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        return None

    if name:
        donor.name = name
    if email:
        donor.email = email

    db.commit()
    db.refresh(donor)
    return donor


def delete_donor(donor_id):
    db = SessionLocal()
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if donor:
        db.delete(donor)
        db.commit()
        return True
    return False



# DONOR SEARCH


def search_donors(name=None, email=None):
    db = SessionLocal()
    query = db.query(Donor)

    if name:
        query = query.filter(Donor.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Donor.email.ilike(f"%{email}%"))

    return query.all()



# CAMPAIGN CRUD


def create_campaign(title, description=None):
    db = SessionLocal()
    campaign = Campaign(title=title, description=description)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def list_campaigns():
    db = SessionLocal()
    return db.query(Campaign).all()


def update_campaign(db, campaign_id, title=None, description=None):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return None

    if title:
        campaign.title = title
    if description:
        campaign.description = description

    db.commit()
    db.refresh(campaign)
    return campaign


def delete_campaign(campaign_id):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign:
        db.delete(campaign)
        db.commit()
        return True
    return False



# CAMPAIGN SEARCH


def search_campaigns(title=None, description=None):
    db = SessionLocal()
    query = db.query(Campaign)

    if title:
        query = query.filter(Campaign.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(Campaign.description.ilike(f"%{description}%"))

    return query.all()



# DONATION CRUD


def create_donation(amount, donor_id, campaign_id):
    db = SessionLocal()
    donation = Donation(amount=amount, donor_id=donor_id, campaign_id=campaign_id)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation


def list_donations():
    db = SessionLocal()
    return db.query(Donation).all()


def update_donation(db, donation_id, amount=None, donor_id=None, campaign_id=None):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        return None

    if amount:
        donation.amount = amount
    if donor_id:
        donation.donor_id = donor_id
    if campaign_id:
        donation.campaign_id = campaign_id

    db.commit()
    db.refresh(donation)
    return donation


def delete_donation(donation_id):
    db = SessionLocal()
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if donation:
        db.delete(donation)
        db.commit()
        return True
    return False
