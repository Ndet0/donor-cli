# src/cli.py
import click
from .db import SessionLocal, Base, engine
from .models import Donor, Campaign, Donation
from .crud import (
    create_donor, list_donors, find_donor_by_id, find_donor_by_name, find_donor_by_email, delete_donor_by_id,
    create_campaign, list_campaigns, find_campaign_by_id, find_campaign_by_title, delete_campaign_by_id,
    create_donation, list_donations, donations_for_donor, donations_for_campaign,
    total_donations, donations_by_donor, donations_by_campaign
)

# Ensure tables exist (dev convenience)
Base.metadata.create_all(bind=engine)

# ---------- helpers ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def confirm_prompt(msg):
    return click.confirm(msg, default=False)

# ---------- CLI ----------
@click.group()
def cli():
    """Donor Management CLI Application"""
    pass

# ---------------- DONOR ----------------
@cli.group()
def donor():
    """Manage donors"""
    pass

@donor.command("add")
@click.option("--name", prompt=True)
@click.option("--email", prompt=True)
def donor_add(name, email):
    db = next(get_db())
    try:
        obj = create_donor(db, name=name, email=email)
        click.echo(f"✅ Donor created: {obj.id} - {obj.name} <{obj.email}>")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@donor.command("list")
def donor_list():
    db = next(get_db())
    rows = list_donors(db)
    if not rows:
        click.echo("No donors.")
        return
    click.echo("📌 Donors:")
    for d in rows:
        click.echo(f" - {d.id}: {d.name} <{d.email}>")

@donor.command("view")
@click.argument("donor_id", type=int)
def donor_view(donor_id):
    db = next(get_db())
    d = find_donor_by_id(db, donor_id)
    if not d:
        click.echo("Donor not found")
        return
    click.echo(f"ID: {d.id}\nName: {d.name}\nEmail: {d.email}\nDonations:")
    if not d.donations:
        click.echo("  None")
    else:
        for dn in d.donations:
            click.echo(f"  - {dn.id}: {dn.amount} at {dn.timestamp} (campaign={dn.campaign_id})")

@donor.command("find-by-name")
@click.argument("name")
def donor_find_by_name(name):
    db = next(get_db())
    rows = find_donor_by_name(db, name)
    if not rows:
        click.echo("No donors found with that name.")
        return
    for d in rows:
        click.echo(f"{d.id}: {d.name} <{d.email}>")

@donor.command("find-by-email")
@click.argument("email")
def donor_find_by_email(email):
    db = next(get_db())
    rows = find_donor_by_email(db, email)
    if not rows:
        click.echo("No donors found with that email.")
        return
    for d in rows:
        click.echo(f"{d.id}: {d.name} <{d.email}>")

@donor.command("delete")
@click.argument("donor_id", type=int)
def donor_delete(donor_id):
    db = next(get_db())
    d = find_donor_by_id(db, donor_id)
    if not d:
        click.echo("Donor not found.")
        return
    click.echo(f"You are about to delete donor: {d.id} - {d.name} and ALL their donations.")
    if not confirm_prompt("Are you sure?"):
        click.echo("Cancelled.")
        return
    ok = delete_donor_by_id(db, donor_id)
    click.echo("Deleted." if ok else "Delete failed.")

# ---------------- CAMPAIGN ----------------
@cli.group()
def campaign():
    """Manage campaigns"""
    pass

@campaign.command("add")
@click.option("--title", prompt=True)
@click.option("--description", prompt=False, default="")
def campaign_add(title, description):
    db = next(get_db())
    try:
        c = create_campaign(db, title=title, description=description)
        click.echo(f"✅ Campaign created: {c.id} - {c.title}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@campaign.command("list")
def campaign_list():
    db = next(get_db())
    rows = list_campaigns(db)
    if not rows:
        click.echo("No campaigns.")
        return
    click.echo("📌 Campaigns:")
    for c in rows:
        click.echo(f" - {c.id}: {c.title} — {c.description or '(no description)'}")

@campaign.command("find")
@click.argument("title")
def campaign_find(title):
    db = next(get_db())
    rows = find_campaign_by_title(db, title)
    if not rows:
        click.echo("No campaigns found.")
        return
    for c in rows:
        click.echo(f"{c.id}: {c.title} — {c.description}")

@campaign.command("delete")
@click.argument("campaign_id", type=int)
def campaign_delete(campaign_id):
    db = next(get_db())
    c = find_campaign_by_id(db, campaign_id)
    if not c:
        click.echo("Campaign not found.")
        return
    click.echo(f"You are about to delete campaign: {c.id} - {c.title} and ALL its donations.")
    if not confirm_prompt("Are you sure?"):
        click.echo("Cancelled.")
        return
    ok = delete_campaign_by_id(db, campaign_id)
    click.echo("Deleted." if ok else "Delete failed.")

# ---------------- DONATION ----------------
@cli.group()
def donation():
    """Manage donations"""
    pass

@donation.command("add")
@click.option("--amount", prompt=True, type=float)
@click.option("--donor-id", prompt=True, type=int)
@click.option("--campaign-id", default=None, type=int)
def donation_add(amount, donor_id, campaign_id):
    db = next(get_db())
    try:
        dn = create_donation(db, amount=amount, donor_id=donor_id, campaign_id=campaign_id)
        click.echo(f"✅ Donation created: {dn.id} amount={dn.amount} donor={dn.donor_id} campaign={dn.campaign_id}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@donation.command("list")
def donation_list():
    db = next(get_db())
    rows = list_donations(db)
    if not rows:
        click.echo("No donations.")
        return
    for dn in rows:
        click.echo(f"{dn.id}: {dn.amount} -> donor {dn.donor_id} campaign {dn.campaign_id} at {dn.timestamp}")

@donation.command("by-donor")
@click.argument("donor_id", type=int)
def donation_by_donor(donor_id):
    db = next(get_db())
    rows = donations_for_donor(db, donor_id)
    if not rows:
        click.echo("No donations for that donor.")
        return
    for dn in rows:
        click.echo(f"{dn.id}: {dn.amount} at {dn.timestamp} (campaign={dn.campaign_id})")

@donation.command("by-campaign")
@click.argument("campaign_id", type=int)
def donation_by_campaign(campaign_id):
    db = next(get_db())
    rows = donations_for_campaign(db, campaign_id)
    if not rows:
        click.echo("No donations for that campaign.")
        return
    for dn in rows:
        click.echo(f"{dn.id}: {dn.amount} at {dn.timestamp} (donor={dn.donor_id})")

# ---------------- REPORTS ----------------
@cli.group()
def report():
    """Reports"""
    pass

@report.command("total")
def report_total():
    db = next(get_db())
    total = total_donations(db)
    click.echo(f"Total donations: {total}")

@report.command("by-donor")
def report_by_donor():
    db = next(get_db())
    rows = donations_by_donor(db)
    if not rows:
        click.echo("No donations yet.")
        return
    click.echo("Donations by donor:")
    for name, total in rows:
        click.echo(f" - {name}: {total}")

@report.command("by-campaign")
def report_by_campaign():
    db = next(get_db())
    rows = donations_by_campaign(db)
    if not rows:
        click.echo("No donations yet.")
        return
    click.echo("Donations by campaign:")
    for title, total in rows:
        click.echo(f" - {title}: {total}")

if __name__ == "__main__":
    cli()
