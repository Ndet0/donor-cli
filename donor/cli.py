import argparse
from donor.donor_manager import DonorManager
from donor.user_manager import admin_login

parser = argparse.ArgumentParser("donor")
sub = parser.add_subparsers(dest="command")

login_cmd = sub.add_parser("login")
login_cmd.add_argument("--email", required=True)
login_cmd.add_argument("--password", required=True)

sub.add_parser("list")

add_cmd = sub.add_parser("add")
add_cmd.add_argument("--name", required=True)
add_cmd.add_argument("--amount", type=int, required=True)

args = parser.parse_args()

if args.command == "login":
    admin_login(args.email, args.password)

elif args.command == "list":
    DonorManager().list_donations()

elif args.command == "add":
    DonorManager().add_donation(args.name, args.amount)
