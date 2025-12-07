# donor_manager.py
from donor.db import SessionLocal
from donor.models import Donor, Campaign, Donation

# --------------------
# DONOR FUNCTIONS
# --------------------
def add_donor(name, email):
    db = SessionLocal()
    donor = Donor(name=name, email=email)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return {"id": donor.id, "name": donor.name, "email": donor.email}

def list_donors():
    db = SessionLocal()
    return [{"id": d.id, "name": d.name, "email": d.email} for d in db.query(Donor).all()]

def search_donor(name):
    db = SessionLocal()
    results = db.query(Donor).filter(Donor.name.ilike(f"%{name}%")).all()
    return [{"id": d.id, "name": d.name, "email": d.email} for d in results]

def update_donor(donor_id, name=None, email=None):
    db = SessionLocal()
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        return None
    if name:
        donor.name = name
    if email:
        donor.email = email
    db.commit()
    db.refresh(donor)
    return {"id": donor.id, "name": donor.name, "email": donor.email}

def delete_donor(donor_id):
    db = SessionLocal()
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        return False
    db.delete(donor)
    db.commit()
    return True

# --------------------
# CAMPAIGN FUNCTIONS
# --------------------
def add_campaign(title, description=None):
    db = SessionLocal()
    campaign = Campaign(title=title, description=description)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return {"id": campaign.id, "title": campaign.title, "description": campaign.description}

def list_campaigns():
    db = SessionLocal()
    return [{"id": c.id, "title": c.title, "description": c.description} for c in db.query(Campaign).all()]

def update_campaign(campaign_id, title=None, description=None):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return None
    if title:
        campaign.title = title
    if description:
        campaign.description = description
    db.commit()
    db.refresh(campaign)
    return {"id": campaign.id, "title": campaign.title, "description": campaign.description}

def delete_campaign(campaign_id):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return False
    db.delete(campaign)
    db.commit()
    return True

# --------------------
# DONATION FUNCTIONS
# --------------------
def add_donation(amount, donor_id, campaign_id=None):
    db = SessionLocal()
    donation = Donation(amount=amount, donor_id=donor_id, campaign_id=campaign_id)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return {"id": donation.id, "amount": donation.amount, "donor_id": donor_id, "campaign_id": campaign_id}

def list_donations():
    db = SessionLocal()
    return [
        {"id": d.id, "amount": d.amount, "donor_id": d.donor_id, "campaign_id": d.campaign_id}
        for d in db.query(Donation).all()
    ]

def update_donation(donation_id, amount=None, donor_id=None, campaign_id=None):
    db = SessionLocal()
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
    return {"id": donation.id, "amount": donation.amount, "donor_id": donation.donor_id, "campaign_id": donation.campaign_id}

def delete_donation(donation_id):
    db = SessionLocal()
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        return False
    db.delete(donation)
    db.commit()
    return True

# --------------------
# REPORTS
# --------------------
def total_donations():
    db = SessionLocal()
    return sum(d.amount for d in db.query(Donation).all())

def donations_by_donor():
    db = SessionLocal()
    result = {}
    for donor in db.query(Donor).all():
        total = sum(d.amount for d in donor.donations)
        result[donor.name] = total
    return result

def donations_by_campaign():
    db = SessionLocal()
    result = {}
    for campaign in db.query(Campaign).all():
        total = sum(d.amount for d in campaign.donations)
        result[campaign.title] = total
    return result
