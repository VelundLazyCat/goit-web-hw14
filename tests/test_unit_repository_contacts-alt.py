import unittest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models import Contact, User
from datetime import date, datetime, timedelta
from shemas import ContactSchema, ContactResponse, UserModel, UserResponse
from contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    get_contacts_birthdays,
)


class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(user_id=1, username='Peter',
                         email='pete@mail.py', password='12345678')

    async def test_get_contacts(self):
        contacts = [Contact(contact_id=1, first_name='Ole', last_name='Tole',
                            telephon_number='380991112233', birthday='13.12.2001', user_id=1),
                    Contact(contact_id=2, first_name='Ale', last_name='Pole',
                            telephon_number='380991112255', birthday='15.12.2001', user_id=1),
                    Contact(contact_id=3, first_name='Ele', last_name='Kole',
                            telephon_number='380991112244', birthday='29.12.2001', user_id=1)]
        mocked_contacts = MagicMock()

        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(contact_field=None, user=self.user, db=self.session)
        self.assertEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
