import unittest

from app.routers.user import UserInDB
import app.user_store as user_store
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class TestUserStore(unittest.TestCase):

    def setUp(self):
        hashed_password_1 = password_hash.hash("geheim")
        hashed_password_2 = password_hash.hash("other_password")

        user = UserInDB(
            username="testuser",
            password="geheim",
            hashed_password=hashed_password_1
        )

        user_2 = UserInDB(
            username="other_user",
            password="other_password",
            hashed_password=hashed_password_2
        )

        user_store.add_user(user)
        user_store.add_user(user_2)

    def tearDown(self):
        user_store.remove_user("testuser")
        user_store.remove_user("other_user")

    def test_user_store(self):
        user_list = user_store.get_users()
        self.assertGreaterEqual(len(user_list), 1)
        self.assertEqual(user_list[0].username, "testuser")
        self.assertEqual(user_list[0].password, "geheim")

    def test_get_user(self):
        user: UserInDB | None = user_store.get_user("testuser")
        self.assertIsNotNone(user)
        self.assertIsInstance(user, UserInDB)
        self.assertEqual("testuser", user.username)

    def test_no_duplicate_users(self):
        with self.assertRaises(ValueError):
            user_store.add_user(UserInDB(
                username="testuser",
                password="geheim",
                hashed_password="hashed_password"
            ))

    def test_get_nonexistent_user(self):
        user: UserInDB | None = user_store.get_user("nonexistent_user")
        self.assertIsNone(user)

    def test_remove_user(self):
        user_store.remove_user("testuser")
        user: UserInDB | None = user_store.get_user("testuser")
        self.assertIsNone(user)