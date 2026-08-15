import os
import argparse
import getpass

from pwdlib import PasswordHash

import app.user_store as user_store
from app.routers.user import UserInDB as User

password_hash = PasswordHash.recommended()

def handle_list_users(args):
    user_list = user_store.get_users()
    for user in user_list:
        print(f"User: {user.username}")

def handle_add_user(args):
    username = args.name
    password_1 = getpass.getpass("Enter password: ")
    password_2 = getpass.getpass("Confirm password: ")
    password = password_1 if password_1 == password_2 else None
    if not password:
        print("Passwords do not match. Exiting.")
        return
    user = User(username=username, hashed_password=password_hash.hash(password))
    print(f"Adding user: {username}")
    user_store.add_user(user)
    print(f"User {username} added")

def handle_delete_user(args):
    username = args.name
    user_store.remove_user(username)
    print(f"User {username} removed")

def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-p", "--path", help="Path to the user store")

    parser = argparse.ArgumentParser(description="User Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List Users Command
    parser_list = subparsers.add_parser(
        "list-users",
        parents=[parent_parser],
        help="List all users"
    )
    parser_list.set_defaults(func=handle_list_users)

    # Add User Command
    parser_add = subparsers.add_parser(
        "add-user",
        parents=[parent_parser],
        help="Add a new user"
    )
    parser_add.add_argument(
        "-n", "--name",
        required=True,
        help="Username of the new user"
    )
    parser_add.set_defaults(func=handle_add_user)

    # Remove User Command
    parser_del = subparsers.add_parser(
        "delete-user",
        parents=[parent_parser],
        help="Delete an existing user"
    )
    parser_del.add_argument(
        "-n", "--name",
        required=True,
        help="Username of the user to delete"
    )
    parser_del.set_defaults(func=handle_delete_user)

    args = parser.parse_args()
    if args.path:
        print(f"Using user store at: {args.path}")
        os.environ["COPY_PDF_USER_STORE"] = args.path
    args.func(args)

if __name__ == "__main__":
    main()