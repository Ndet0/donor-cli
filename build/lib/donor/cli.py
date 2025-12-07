import click
from donor.donor_manager import (
    add_donor, list_donors, search_donor, update_donor, delete_donor,
    add_campaign, list_campaigns, update_campaign, delete_campaign,
    add_donation, list_donations, update_donation, delete_donation
)

@click.group()
def cli():
    """Donor CLI - Manage donors, campaigns, and donations easily."""
    pass

# ========================
# DONOR COMMANDS
# ========================

@click.command()
@click.option("--name", required=True, help="Donor's name")
@click.option("--email", required=True, help="Donor's email")
def add_d(name, email):
    """Add a new donor"""
    donor = add_donor(name, email)
    click.echo(f"[✔] Added donor: {donor['id']}: {donor['name']} <{donor['email']}>")

@click.command(name="list-donors")
def list_donors_cmd():
    """List all donors"""
    donors = list_donors()
    if not donors:
        click.echo("[i] No donors found.")
        return
    click.echo(f"[i] Total donors: {len(donors)}")
    click.echo("-" * 40)
    for d in donors:
        click.echo(f"{d['id']}: {d['name']} <{d['email']}>")
    click.echo("-" * 40)

@click.command()
@click.option("--name", required=True, help="Name to search for")
def search_d(name):
    """Search donors by name"""
    results = search_donor(name)
    if not results:
        click.echo(f"[i] No donors matching '{name}' found.")
        return
    click.echo(f"[i] Found {len(results)} donor(s):")
    for d in results:
        click.echo(f"{d['id']}: {d['name']} <{d['email']}>")

@click.command()
@click.argument("donor_id", type=int)
@click.option("--name", help="New name")
@click.option("--email", help="New email")
def update_d(donor_id, name, email):
    """Update donor details"""
    updated = update_donor(donor_id, name=name, email=email)
    if not updated:
        click.echo(f"[!] Donor with ID {donor_id} not found.")
        return
    click.echo(f"[✔] Updated donor: {updated['id']}: {updated['name']} <{updated['email']}>")

@click.command()
@click.argument("donor_id", type=int)
def delete_d(donor_id):
    """Delete a donor"""
    confirm = click.confirm(f"Are you sure you want to delete donor ID {donor_id}?", default=False)
    if not confirm:
        click.echo("[i] Delete cancelled.")
        return
    if delete_donor(donor_id):
        click.echo(f"[✔] Deleted donor {donor_id}")
    else:
        click.echo(f"[!] Donor with ID {donor_id} not found.")

# ========================
# CAMPAIGN COMMANDS
# ========================

@click.command()
@click.option("--title", required=True, help="Campaign title")
@click.option("--description", help="Campaign description")
def add_c(title, description):
    """Add a new campaign"""
    campaign = add_campaign(title, description)
    click.echo(f"[✔] Added campaign: {campaign['id']}: {campaign['title']}")

@click.command(name="list-campaigns")
def list_campaigns_cmd():
    """List all campaigns"""
    campaigns = list_campaigns()
    if not campaigns:
        click.echo("[i] No campaigns found.")
        return
    click.echo(f"[i] Total campaigns: {len(campaigns)}")
    click.echo("-" * 40)
    for c in campaigns:
        click.echo(f"{c['id']}: {c['title']} — {c.get('description','(no description)')}")
    click.echo("-" * 40)

@click.command()
@click.argument("campaign_id", type=int)
@click.option("--title", help="New title")
@click.option("--description", help="New description")
def update_c(campaign_id, title, description):
    """Update a campaign"""
    updated = update_campaign(campaign_id, title=title, description=description)
    if not updated:
        click.echo(f"[!] Campaign with ID {campaign_id} not found.")
        return
    click.echo(f"[✔] Updated campaign: {updated['id']}: {updated['title']} — {updated.get('description','(no description)')}")

@click.command()
@click.argument("campaign_id", type=int)
def delete_c(campaign_id):
    """Delete a campaign"""
    confirm = click.confirm(f"Are you sure you want to delete campaign ID {campaign_id}?", default=False)
    if not confirm:
        click.echo("[i] Delete cancelled.")
        return
    if delete_campaign(campaign_id):
        click.echo(f"[✔] Deleted campaign {campaign_id}")
    else:
        click.echo(f"[!] Campaign with ID {campaign_id} not found.")

# ========================
# DONATION COMMANDS
# ========================

@click.command()
@click.option("--donor-id", required=True, type=int, help="Donor ID")
@click.option("--campaign-id", type=int, help="Campaign ID (optional)")
@click.option("--amount", required=True, type=float, help="Donation amount")
def add_dn(donor_id, campaign_id, amount):
    """Add a new donation"""
    donation = add_donation(donor_id, campaign_id, amount)
    click.echo(f"[✔] Added donation: {donation['id']} amount={donation['amount']} donor={donation['donor_id']} campaign={donation.get('campaign_id')}")

@click.command(name="list-donations")
def list_donations_cmd():
    """List all donations"""
    donations = list_donations()
    if not donations:
        click.echo("[i] No donations found.")
        return
    click.echo(f"[i] Total donations: {len(donations)}")
    click.echo("-" * 40)
    for d in donations:
        click.echo(f"{d['id']}: {d['amount']} -> donor {d['donor_id']} campaign {d.get('campaign_id')}")
    click.echo("-" * 40)

@click.command()
@click.argument("donation_id", type=int)
@click.option("--amount", type=float, help="New amount")
@click.option("--donor-id", type=int, help="New donor ID")
@click.option("--campaign-id", type=int, help="New campaign ID")
def update_dn(donation_id, amount, donor_id, campaign_id):
    """Update a donation"""
    updated = update_donation(donation_id, amount=amount, donor_id=donor_id, campaign_id=campaign_id)
    if not updated:
        click.echo(f"[!] Donation with ID {donation_id} not found.")
        return
    click.echo(f"[✔] Updated donation: {updated['id']} amount={updated['amount']} donor={updated['donor_id']} campaign={updated.get('campaign_id')}")

@click.command()
@click.argument("donation_id", type=int)
def delete_dn(donation_id):
    """Delete a donation"""
    confirm = click.confirm(f"Are you sure you want to delete donation ID {donation_id}?", default=False)
    if not confirm:
        click.echo("[i] Delete cancelled.")
        return
    if delete_donation(donation_id):
        click.echo(f"[✔] Deleted donation {donation_id}")
    else:
        click.echo(f"[!] Donation with ID {donation_id} not found.")


# ========================
# REPORT COMMANDS
# ========================

@click.group()
def report():
    """Reports on donations"""
    pass

@click.command(name="total")
def report_total():
    """Show total donations"""
    donations = list_donations()
    total = sum(d['amount'] for d in donations)
    click.echo(f"[i] Total donations: {total}")

@click.command(name="by-donor")
def report_by_donor():
    """Show donations grouped by donor"""
    donors = list_donors()
    if not donors:
        click.echo("[i] No donors found.")
        return
    click.echo("[i] Donations by donor:")
    for d in donors:
        donations = [dn for dn in list_donations() if dn['donor_id'] == d['id']]
        total = sum(dn['amount'] for dn in donations)
        click.echo(f" - {d['name']}: {total}")

@click.command(name="by-campaign")
def report_by_campaign():
    """Show donations grouped by campaign"""
    campaigns = list_campaigns()
    if not campaigns:
        click.echo("[i] No campaigns found.")
        return
    click.echo("[i] Donations by campaign:")
    for c in campaigns:
        donations = [dn for dn in list_donations() if dn.get('campaign_id') == c['id']]
        total = sum(dn['amount'] for dn in donations)
        click.echo(f" - {c['title']}: {total}")



# ========================
# REGISTER COMMANDS
# ========================

# Donor
cli.add_command(add_d, name="donor-add")
cli.add_command(list_donors_cmd, name="donor-list")
cli.add_command(search_d, name="donor-search")
cli.add_command(update_d, name="donor-update")
cli.add_command(delete_d, name="donor-delete")

# Campaign
cli.add_command(add_c, name="campaign-add")
cli.add_command(list_campaigns_cmd, name="campaign-list")
cli.add_command(update_c, name="campaign-update")
cli.add_command(delete_c, name="campaign-delete")

# Donation
cli.add_command(add_dn, name="donation-add")
cli.add_command(list_donations_cmd, name="donation-list")
cli.add_command(update_dn, name="donation-update")
cli.add_command(delete_dn, name="donation-delete")


# Register report commands
report.add_command(report_total)
report.add_command(report_by_donor)
report.add_command(report_by_campaign)

# Add report group to main CLI
cli.add_command(report)
     

if __name__ == "__main__":
    cli()
