# donor-cli
**Donor CLI — Phase 3 Project**

A simple CLI tool to manage donors, donations, campaigns, and reports using:

- Python 3.10+
- SQLAlchemy (ORM)
- Click (CLI)
- Alembic (migrations, optional)
- Pipenv (virtual environment + dependency management)

---

## Quick Start (Local Development)

```bash
# Clone the repository (if not already done)
cd donor-cli

# Install dependencies and activate pipenv virtual environment
pipenv install
pipenv shell

# Initialize database tables
python -m donor.cli   # Shows available commands


#User Authentication

 Sensitive commands (add, update, delete) require a logged-in user.

 # Register a new user
python -m donor.cli register --username admin --password secret123

# Log in as a user
python -m donor.cli login --username admin --password secret123

# Log out
python -m donor.cli logout


#Donor commands 

# Add a new donor (requires login)
python -m donor.cli donor-add --name "John Doe" --email "john@example.com"

# List all donors (no login required)
python -m donor.cli donor-list

# Search donors by name (no login required)
python -m donor.cli donor-search --name "John"

# Update a donor (requires login)
python -m donor.cli donor-update 1 --name "John Smith" --email "johnsmith@example.com"

# Delete a donor (requires login)
python -m donor.cli donor-delete 1


#campaign commands 

# Add a new campaign (requires login)
python -m donor.cli campaign-add --title "Food Drive" --description "End of year donations"

# List all campaigns (no login required)
python -m donor.cli campaign-list

# Update a campaign (requires login)
python -m donor.cli campaign-update 1 --title "Holiday Food Drive"

# Delete a campaign (requires login)
python -m donor.cli campaign-delete 1


#Donation commands 

# Add a donation (requires login)
python -m donor.cli donation-add --amount 50 --donor-id 1 --campaign-id 1

# List all donations (no login required)
python -m donor.cli donation-list

# Update a donation (requires login)
python -m donor.cli donation-update 1 --amount 75 --donor-id 1 --campaign-id 1

# Delete a donation (requires login)
python -m donor.cli donation-delete 1


#Reports

# Total donations
python -m donor.cli report-total

# Donations by donor
python -m donor.cli report-by-donor

# Donations by campaign
python -m donor.cli report-by-campaign


Development Notes

Default database: donor.db (SQLite)

To change the database, update DATABASE_URL in donor/db.py

Use Alembic for schema migrations (see alembic/ folder)

Only authenticated users can perform add, update, and delete actions.

#Authors

Festus Kisoi