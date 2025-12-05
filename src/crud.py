# src/crud.py
from sqlalchemy import func
from .models import Donor, Donation, Campaign

# Note: functions expect an active SQLAlchemy session object (db),
# which your CLI creates with SessionLocal() and passes in.

# ---------- Donor ----------
def create_donor(db, name, email):
    return Donor.create(db, name=name, email=email)

def list_donors(db):
    return Donor.get_all(db)

def find_donor_by_id(db, donor_id):
    return Donor.find_by_id(db, donor_id)

def find_donor_by_name(db, name):
    return Donor.find_by_attr(db, name=name)

def find_donor_by_email(db, email):
    return Donor.find_by_attr(db, email=email.lower())

def delete_donor_by_id(db, donor_id):
    donor = Donor.find_by_id(db, donor_id)
    if not donor:
        return False
    donor.delete(db)
    return True

# ---------- Campaign ----------
def create_campaign(db, title, description=None):
    return Campaign.create(db, title=title, description=description)

def list_campaigns(db):
    return Campaign.get_all(db)

def find_campaign_by_id(db, campaign_id):
    return Campaign.find_by_id(db, campaign_id)

def find_campaign_by_title(db, title):
    return Campaign.find_by_attr(db, title=title)

def delete_campaign_by_id(db, campaign_id):
    campaign = Campaign.find_by_id(db, campaign_id)
    if not campaign:
        return False
    campaign.delete(db)
    return True

# ---------- Donation ----------
def create_donation(db, amount, donor_id, campaign_id=None):
    # Validate donor exists
    donor = Donor.find_by_id(db, donor_id)
    if not donor:
        raise ValueError(f"No donor with id={donor_id}")
    if campaign_id:
        camp = Campaign.find_by_id(db, campaign_id)
        if not camp:
            raise ValueError(f"No campaign with id={campaign_id}")
    donation = Donation(amount=amount, donor_id=donor_id, campaign_id=campaign_id)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

def list_donations(db):
    return db.query(Donation).order_by(Donation.timestamp.desc()).all()

def donations_for_donor(db, donor_id):
    return db.query(Donation).filter(Donation.donor_id == donor_id).order_by(Donation.timestamp.desc()).all()

def donations_for_campaign(db, campaign_id):
    return db.query(Donation).filter(Donation.campaign_id == campaign_id).order_by(Donation.timestamp.desc()).all()

# ---------- Reports ----------
def total_donations(db):
    total = db.query(func.coalesce(func.sum(Donation.amount), 0)).scalar()
    return float(total) if total is not None else 0.0

def donations_by_donor(db):
    rows = db.query(Donor.name, func.sum(Donation.amount).label("total")) \
             .join(Donation, Donation.donor_id == Donor.id) \
             .group_by(Donor.id).all()
    return [(name, float(total)) for name, total in rows]

def donations_by_campaign(db):
    rows = db.query(Campaign.title, func.sum(Donation.amount).label("total")) \
             .join(Donation, Donation.campaign_id == Campaign.id) \
             .group_by(Campaign.id).all()
    return [(title, float(total)) for title, total in rows]
