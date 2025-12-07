# donor/cli.py
import click
from functools import wraps
from donor.donor_manager import (
    add_donor, list_donors, search_donor, update_donor, delete_donor,
    add_campaign, list_campaigns, update_campaign, delete_campaign,
    add_donation, list_donations, update_donation, delete_donation,
    total_donations, donations_by_donor, donations_by_campaign
)
from donor.user_manager import register_user, authenticate_user, logout_user, current_user


# Login Decorator

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            click.echo(" You must be logged in to perform this action.")
            return
        return f(*args, **kwargs)
    return wrapper


# CLI Group

@click.group()
def cli():
    """Donor CLI - Manage donors, campaigns, donations and reports"""
    pass


# LOGIN / LOGOUT / REGISTER

@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def register(username, password):
    success, result = register_user(username, password)
    if success:
        click.echo(f"Registered user: {result.username}")
    else:
        click.echo(f" {result}")

@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def login(username, password):
    success, result = authenticate_user(username, password)
    if success:
        click.echo(f" Logged in as {result.username}")
    else:
        click.echo(f"{result}")

@click.command()
def logout():
    if logout_user():
        click.echo(" Logged out successfully")
    else:
        click.echo(" No user is currently logged in")


# DONOR COMMANDS

@click.command()
@click.option("--name", required=True)
@click.option("--email", required=True)
@login_required
def donor_add(name, email):
    donor = add_donor(name, email)
    click.echo(f"Added donor: {donor['id']}: {donor['name']} <{donor['email']}>")

@click.command(name="donor-list")
def donor_list_cmd():
    donors = list_donors()
    if not donors:
        click.echo("No donors found.")
        return
    for d in donors:
        click.echo(f"{d['id']}: {d['name']} <{d['email']}>")

@click.command()
@click.option("--name", required=True)
def donor_search(name):
    results = search_donor(name)
    if not results:
        click.echo("No matching donors found.")
        return
    for d in results:
        click.echo(f"{d['id']}: {d['name']} <{d['email']}>")

@click.command()
@click.argument("donor_id", type=int)
@click.option("--name")
@click.option("--email")
@login_required
def donor_update(donor_id, name, email):
    updated = update_donor(donor_id, name=name, email=email)
    if not updated:
        click.echo("Donor not found.")
        return
    click.echo(f"Updated donor: {updated['id']}: {updated['name']} <{updated['email']}>")

@click.command()
@click.argument("donor_id", type=int)
@login_required
def donor_delete(donor_id):
    if delete_donor(donor_id):
        click.echo(f"Deleted donor {donor_id}")
    else:
        click.echo("Donor not found.")


# CAMPAIGN COMMANDS

@click.command()
@click.option("--title", required=True)
@click.option("--description")
@login_required
def campaign_add(title, description):
    c = add_campaign(title, description)
    click.echo(f"Added campaign: {c['id']}: {c['title']}")

@click.command(name="campaign-list")
def campaign_list_cmd():
    campaigns = list_campaigns()
    for c in campaigns:
        click.echo(f"{c['id']}: {c['title']} - {c['description'] or '(no description)'}")

@click.command()
@click.argument("campaign_id", type=int)
@click.option("--title")
@click.option("--description")
@login_required
def campaign_update_cmd(campaign_id, title, description):
    c = update_campaign(campaign_id, title, description)
    if not c:
        click.echo("Campaign not found.")
        return
    click.echo(f"Updated campaign: {c['id']}: {c['title']}")

@click.command()
@click.argument("campaign_id", type=int)
@login_required
def campaign_delete_cmd(campaign_id):
    if delete_campaign(campaign_id):
        click.echo(f"Deleted campaign {campaign_id}")
    else:
        click.echo("Campaign not found.")


# DONATION COMMANDS

@click.command()
@click.option("--amount", required=True, type=float)
@click.option("--donor-id", required=True, type=int)
@click.option("--campaign-id", type=int)
@login_required
def donation_add_cmd(amount, donor_id, campaign_id):
    d = add_donation(amount, donor_id, campaign_id)
    click.echo(f"Added donation: {d['id']} amount={d['amount']} donor={d['donor_id']} campaign={d['campaign_id']}")

@click.command(name="donation-list")
def donation_list_cmd():
    donations = list_donations()
    for d in donations:
        click.echo(f"{d['id']}: {d['amount']} -> donor {d['donor_id']} campaign {d['campaign_id']}")

@click.command()
@click.argument("donation_id", type=int)
@click.option("--amount", type=float)
@click.option("--donor-id", type=int)
@click.option("--campaign-id", type=int)
@login_required
def donation_update_cmd(donation_id, amount, donor_id, campaign_id):
    d = update_donation(donation_id, amount, donor_id, campaign_id)
    if not d:
        click.echo("Donation not found.")
        return
    click.echo(f"Updated donation: {d['id']} amount={d['amount']} donor={d['donor_id']} campaign={d['campaign_id']}")

@click.command()
@click.argument("donation_id", type=int)
@login_required
def donation_delete_cmd(donation_id):
    if delete_donation(donation_id):
        click.echo(f"Deleted donation {donation_id}")
    else:
        click.echo("Donation not found.")


# REPORTS

@click.command()
def report_total():
    click.echo(f"Total donations: {total_donations()}")

@click.command()
def report_by_donor():
    data = donations_by_donor()
    for name, total in data.items():
        click.echo(f"{name}: {total}")

@click.command()
def report_by_campaign():
    data = donations_by_campaign()
    for title, total in data.items():
        click.echo(f"{title}: {total}")


# REGISTER COMMANDS
cli.add_command(register)
cli.add_command(login)
cli.add_command(logout)

cli.add_command(donor_add)
cli.add_command(donor_list_cmd)
cli.add_command(donor_search)
cli.add_command(donor_update)
cli.add_command(donor_delete)

cli.add_command(campaign_add)
cli.add_command(campaign_list_cmd)
cli.add_command(campaign_update_cmd)
cli.add_command(campaign_delete_cmd)

cli.add_command(donation_add_cmd)
cli.add_command(donation_list_cmd)
cli.add_command(donation_update_cmd)
cli.add_command(donation_delete_cmd)

cli.add_command(report_total)
cli.add_command(report_by_donor)
cli.add_command(report_by_campaign)

if __name__ == "__main__":
    cli()
