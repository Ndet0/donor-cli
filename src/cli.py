import click
from .db import SessionLocal, Base, engine
from .crud import (
    create_donor, get_all_donors, find_donor_by_id, delete_donor,
    create_campaign, get_all_campaigns, find_campaign_by_id, delete_campaign,
    create_donation, get_donations_by_donor, get_donations_by_campaign
)


# ---------------------------------------------------------
# Initialize database tables
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# Helper: get a database session
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# CLI Application Root
# ---------------------------------------------------------
@click.group()
def cli():
    """Donor Management CLI Application"""
    pass


# ---------------------------------------------------------
# DONOR COMMANDS
# ---------------------------------------------------------
@cli.group()
def donor():
    """Manage donors"""
    pass


@donor.command()
@click.argument("name")
@click.argument("email")
def add(name, email):
    """Add a new donor"""
    db = next(get_db())
    donor = create_donor(db, name, email)
    click.echo(f"Donor created: {donor}")


@donor.command()
def list():
    """List all donors"""
    db = next(get_db())
    donors = get_all_donors(db)
    if not donors:
        click.echo("No donors found.")
        return
    for d in donors:
        click.echo(f"{d.id}: {d.name} ({d.email})")


@donor.command()
@click.argument("donor_id", type=int)
def view(donor_id):
    """View a donor and their donations"""
    db = next(get_db())
    donor = find_donor_by_id(db, donor_id)
    if not donor:
        click.echo("Donor not found!")
        return

    click.echo(f"ID: {donor.id}")
    click.echo(f"Name: {donor.name}")
    click.echo(f"Email: {donor.email}")
    click.echo("Donations:")

    if not donor.donations:
        click.echo("  No donations yet.")
    else:
        for donation in donor.donations:
            click.echo(f"  - {donation.amount} on {donation.timestamp}")


@donor.command()
@click.argument("donor_id", type=int)
def delete(donor_id):
    """Delete a donor"""
    db = next(get_db())
    if delete_donor(db, donor_id):
        click.echo("Donor deleted successfully.")
    else:
        click.echo("Donor not found.")


# ---------------------------------------------------------
# CAMPAIGN COMMANDS
# ---------------------------------------------------------
@cli.group()
def campaign():
    """Manage campaigns"""
    pass


@campaign.command()
@click.argument("title")
@click.argument("description")
def add(title, description):
    """Add a new campaign"""
    db = next(get_db())
    camp = create_campaign(db, title, description)
    click.echo(f"Campaign created: {camp}")


@campaign.command()
def list():
    """List all campaigns"""
    db = next(get_db())
    campaigns = get_all_campaigns(db)
    if not campaigns:
        click.echo("No campaigns found.")
        return
    for c in campaigns:
        click.echo(f"{c.id}: {c.title} - {c.description}")


@campaign.command()
@click.argument("campaign_id", type=int)
def delete(campaign_id):
    """Delete a campaign"""
    db = next(get_db())
    if delete_campaign(db, campaign_id):
        click.echo("Campaign deleted successfully.")
    else:
        click.echo("Campaign not found.")


# ---------------------------------------------------------
# DONATION COMMANDS
# ---------------------------------------------------------
@cli.group()
def donation():
    """Manage donations"""
    pass


@donation.command()
@click.argument("amount", type=float)
@click.argument("donor_id", type=int)
@click.argument("campaign_id", type=int)
def add(amount, donor_id, campaign_id):
    """Add a donation"""
    db = next(get_db())
    donation = create_donation(db, amount, donor_id, campaign_id)
    click.echo(f"Donation created: {donation}")


@donation.command()
@click.argument("donor_id", type=int)
def by_donor(donor_id):
    """List donations for a donor"""
    db = next(get_db())
    donations = get_donations_by_donor(db, donor_id)
    if not donations:
        click.echo("No donations found.")
        return
    for d in donations:
        click.echo(f"{d.amount} -> Campaign {d.campaign_id}")


@donation.command()
@click.argument("campaign_id", type=int)
def by_campaign(campaign_id):
    """List donations for a campaign"""
    db = next(get_db())
    donations = get_donations_by_campaign(db, campaign_id)
    if not donations:
        click.echo("No donations found.")
        return
    for d in donations:
        click.echo(f"{d.amount} -> Donor {d.donor_id}")


if __name__ == "__main__":
    cli()
