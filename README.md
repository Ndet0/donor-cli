# donor-cli
# Donor CLI — Phase 3 Project

Simple CLI to manage donors, donations and campaigns using:
- Python 3.10+
- SQLAlchemy (ORM)
- Click (CLI)
- Alembic (migrations, optional)
- Pipenv (virtual env + dependency management)

## Quick start (local dev)
```bash
# clone repo (you already did)
cd donor-cli

# create pipenv venv & install deps (if not already done)
pipenv install
pipenv shell

# create DB tables
python -m src.cli    # shows commands
python -m src.cli campaign list   # example
python -m src.cli donor add "Name" "email@example.com"
python -m src.cli campaign add --title "Food Drive" --description "End of year"
python -m src.cli donation add --amount 50 --donor-id 1 --campaign-id 1
python -m src.cli report total

#Commands

Top-level groups: donor, campaign, donation, report.

Examples:

python -m src.cli donor add (interactive prompts)

python -m src.cli donor list

python -m src.cli donor view 1

python -m src.cli campaign add

python -m src.cli donation add

python -m src.cli report by-donor


#Development notes

DB file: donor.db (SQLite) by default.

To use another database, change DATABASE_URL in src/db.py.

To manage DB schema changes use Alembic (see alembic/ notes).


#Authors

Festus Kisoi