# src/cli.py
import click
from .db import SessionLocal, Base, engine
from .models import Donor, Campaign, Donation
from .crud import (
    create_donor, list_donors, update_donor, delete_donor,
    create_campaign, list_campaigns, update_campaign, delete_campaign,
    create_donation, list_donations, update_donation, delete_donation
)

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Helpers

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def confirm_prompt(msg):
    return click.confirm(msg, default=False)


# Main CLI Group

@click.group()
def cli():
    """Donor Management CLI Application"""
    pass

# DONOR COMMANDS

@cli.group()
def donor():
    """Manage donors"""
    pass

@donor.command("add")
@click.option("--name", prompt=True)
@click.option("--email", prompt=True)
def donor_add(name, email):
    donor = create_donor(name, email)
    click.echo(f" Donor created: {donor.id} - {donor.name} <{donor.email}>")

@donor.command("list")
def donor_list():
    donors = list_donors()
    if not donors:
        click.echo("No donors.")
        return
    click.echo("Donors:")
    for d in donors:
        click.echo(f" - {d.id}: {d.name} <{d.email}>")

@donor.command("update")
@click.argument("donor_id", type=int)
@click.option("--name")
@click.option("--email")
def donor_update(donor_id, name, email):
    db = next(get_db())
    d = update_donor(db, donor_id, name=name, email=email)
    if not d:
        click.echo("Donor not found.")
    else:
        click.echo(f"Updated donor: {d.id} - {d.name} <{d.email}>")

@donor.command("delete")
@click.argument("donor_id", type=int)
def donor_delete(donor_id):
    db = next(get_db())
    d = db.query(Donor).filter(Donor.id == donor_id).first()
    if not d:
        click.echo("Donor not found.")
        return
    click.echo(f"You are about to delete donor: {d.id} - {d.name}")
    if not confirm_prompt("Are you sure?"):
        click.echo("Cancelled.")
        return
    ok = delete_donor(donor_id)
    click.echo("Deleted." if ok else "Delete failed.")


# CAMPAIGN COMMANDS
@cli.group()
def campaign():
    """Manage campaigns"""
    pass

@campaign.command("add")
@click.option("--title", prompt=True)
@click.option("--description", prompt=False, default="")
def campaign_add(title, description):
    c = create_campaign(title, description)
    click.echo(f" Campaign created: {c.id} - {c.title}")

@campaign.command("list")
def campaign_list():
    campaigns = list_campaigns()
    if not campaigns:
        click.echo("No campaigns.")
        return
    click.echo("Campaigns:")
    for c in campaigns:
        click.echo(f" - {c.id}: {c.title} — {c.description or '(no description)'}")

@campaign.command("update")
@click.argument("campaign_id", type=int)
@click.option("--title")
@click.option("--description")
def campaign_update(campaign_id, title, description):
    db = next(get_db())
    c = update_campaign(db, campaign_id, title=title, description=description)
    if not c:
        click.echo("Campaign not found.")
    else:
        click.echo(f"Updated campaign: {c.id} - {c.title} — {c.description or '(no description)'}")

@campaign.command("delete")
@click.argument("campaign_id", type=int)
def campaign_delete(campaign_id):
    db = next(get_db())
    c = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not c:
        click.echo("Campaign not found.")
        return
    click.echo(f"You are about to delete campaign: {c.id} - {c.title}")
    if not confirm_prompt("Are you sure?"):
        click.echo("Cancelled.")
        return
    ok = delete_campaign(campaign_id)
    click.echo("Deleted." if ok else "Delete failed.")


# DONATION COMMANDS
@cli.group()
def donation():
    """Manage donations"""
    pass

@donation.command("add")
@click.option("--amount", prompt=True, type=float)
@click.option("--donor-id", prompt=True, type=int)
@click.option("--campaign-id", default=None, type=int)
def donation_add(amount, donor_id, campaign_id):
    dn = create_donation(amount, donor_id, campaign_id)
    click.echo(f"Donation created: {dn.id} amount={dn.amount} donor={dn.donor_id} campaign={dn.campaign_id}")

@donation.command("list")
def donation_list():
    donations = list_donations()
    if not donations:
        click.echo("No donations.")
        return
    for dn in donations:
        click.echo(f"{dn.id}: {dn.amount} -> donor {dn.donor_id} campaign {dn.campaign_id} at {dn.timestamp}")

@donation.command("update")
@click.argument("donation_id", type=int)
@click.option("--amount", type=float)
@click.option("--donor-id", type=int)
@click.option("--campaign-id", type=int)
def donation_update(donation_id, amount, donor_id, campaign_id):
    db = next(get_db())
    dn = update_donation(db, donation_id, amount=amount, donor_id=donor_id, campaign_id=campaign_id)
    if not dn:
        click.echo("Donation not found.")
    else:
        click.echo(f"Updated donation: {dn.id}: {dn.amount} -> donor {dn.donor_id} campaign {dn.campaign_id}")

@donation.command("delete")
@click.argument("donation_id", type=int)
def donation_delete(donation_id):
    db = next(get_db())
    dn = db.query(Donation).filter(Donation.id == donation_id).first()
    if not dn:
        click.echo("Donation not found.")
        return
    click.echo(f"You are about to delete donation: {dn.id}")
    if not confirm_prompt("Are you sure?"):
        click.echo("Cancelled.")
        return
    ok = delete_donation(donation_id)
    click.echo("Deleted." if ok else "Delete failed.")


# REPORTS
@cli.group()
def report():
    """Reports"""
    pass

@report.command("total")
def report_total():
    db = next(get_db())
    total = sum(d.amount for d in db.query(Donation).all())
    click.echo(f"Total donations: {total}")

@report.command("by-donor")
def report_by_donor():
    db = next(get_db())
    donors = db.query(Donor).all()
    click.echo("Donations by donor:")
    for d in donors:
        total = sum(dn.amount for dn in d.donations)
        click.echo(f" - {d.name}: {total}")

@report.command("by-campaign")
def report_by_campaign():
    db = next(get_db())
    campaigns = db.query(Campaign).all()
    click.echo("Donations by campaign:")
    for c in campaigns:
        total = sum(dn.amount for dn in c.donations)
        click.echo(f" - {c.title}: {total}")

# -----------------------
# MAIN
# -----------------------
if __name__ == "__main__":
    cli()
