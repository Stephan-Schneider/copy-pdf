import shelve
import os
from app.routers.user import UserInDB
import logging

logger = logging.getLogger(__name__)

def _get_db_path():
    path = os.getenv('COPY_PDF_USER_STORE', 'users')
    logger.debug(f"Using user store path: {path}")
    return path

def add_user(user: UserInDB):
    """
    Adds a new user to the persistent storage.

    This function checks if the user's username already exists in the persistent
    storage. If it exists, an exception is raised. Otherwise, the user is stored
    in a shelve-based database. It ensures that the user list is maintained
    persistently.

    According to the Python documentation, shelve is not thread-safe. However, concurrent write access
    will never happen in this application as users can't be added via the web interface.

    :param user: The user to be added to the database.
    :type user: UserInDB
    :raises ValueError: If a user with the same username already exists.
    """
    if user.username in [u.username for u in get_users()]:
        raise ValueError("User already exists")

    logger.info(f"Adding user: {user.username}")
    with shelve.open(_get_db_path(), 'c', writeback=True) as db:
        if "users" not in db:
            db["users"] = []
        db["users"].append(user)

def remove_user(username: str):
    """
    Removes a user with the specified username from the database.

    This function opens a shelve database named 'users' and removes any user
    whose username matches the given parameter. If the 'users' list does not
    exist in the database, it does nothing.

    :param username: The username of the user to be removed.
    :type username: str
    :return: None
    """
    with shelve.open(_get_db_path(), 'c', writeback=True) as db:
        if "users" in db:
            db["users"] = [user for user in db["users"] if user.username != username]

def get_users() -> list[UserInDB]:
    with shelve.open(_get_db_path(), 'c') as db:
        try:
            return db["users"]
        except KeyError:
            logger.warning("No users found in database.")
            return []

def get_user(username: str) -> UserInDB | None:
    with shelve.open(_get_db_path(), 'c') as db:
        try:
            return next(user for user in db["users"] if user.username == username)
        except StopIteration:
            return None