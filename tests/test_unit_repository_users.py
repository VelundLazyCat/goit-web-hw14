import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models import User
from shemas import UserModel
from users import (
    get_user_by_email,
    create_user,
    confirmed_email,
    update_token,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = UserModel(
            username='Andrew',
            email='andrew@google.com',
            password='qwerty1234'
        )
        self.test_email = 'test@test.com'

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.test_email, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        with patch.object(self.session, "add") as mock_add, \
                patch.object(self.session, "commit") as mock_commit, \
                patch.object(self.session, "refresh") as mock_refresh:
            user = await create_user(self.user, self.session)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.password, self.user.password)
        self.assertTrue(hasattr(user, 'user_id'))
        mock_add.assert_called_once_with(user)
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once_with(user)

    async def test_update_token(self):
        user = User()
        user.refresh_token = 'old_token'
        token = 'new_token'

        with patch.object(self.session, "commit") as mock_commit:
            await update_token(user, token, self.session)

        self.assertEqual(user.refresh_token, token)
        mock_commit.assert_called_once()

    async def test_confirmed_email(self):
        await create_user(body=self.user, db=self.session)
        await confirmed_email(email=self.user.email, db=self.session)
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result.confirmed, True)

    async def test_update_avatar(self):
        user = User(email=self.user.email)
        self.session.query().filter().first.return_value = user
        result = await update_avatar(user.email, "avatar_url", self.session)
        self.assertEqual(result.avatar, user.avatar)

    async def test_update_user_password(self):
        user = User(password=self.user.email)
        self.session.query().filter().first.return_value = user
        result = await update_avatar(user.email, "test_password", self.session)
        self.assertEqual(result.password, user.password)


if __name__ == '__main__':
    unittest.main()
