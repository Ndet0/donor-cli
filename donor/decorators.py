# donor/decorators.py
from functools import wraps
from donor.user_manager import current_user
import click

def login_required(f):
    """Decorator to enforce login for CLI commands."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            click.echo(" You must be logged in to perform this action.")
            return
        return f(*args, **kwargs, current_user=user)
    return wrapper
