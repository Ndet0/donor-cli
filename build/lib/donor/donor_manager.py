# donor_manager.py
from donor.db import SessionLocal
from donor.models import Donor, Donation, Campaign

# --- DONOR FUNCTIONS ---

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

# --- DONATIONS FOR REPORTS ---

def get_donor_donations(donor_id):
    """Return all donations for a given donor"""
    db = SessionLocal()
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        return []
    return [{"id": dn.id, "amount": dn.amount, "campaign_id": dn.campaign_id} for dn in donor.donations]

def total_donations():
    """Return total donation amount"""
    db = SessionLocal()
    return sum(d.amount for d in db.query(Donation).all())

def donations_by_donor():
    """Return a dict {donor_name: total_amount}"""
    db = SessionLocal()
    result = {}
    for donor in db.query(Donor).all():
        total = sum(dn.amount for dn in donor.donations)
        result[donor.name] = total
    return result

def donations_by_campaign():
    """Return a dict {campaign_title: total_amount}"""
    db = SessionLocal()
    result = {}
    for campaign in db.query(Campaign).all():
        total = sum(dn.amount for dn in campaign.donations)
        result[campaign.title] = total
    return result
