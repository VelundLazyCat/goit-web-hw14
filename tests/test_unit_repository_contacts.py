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
        self.session = MagicMock(spec=Session)
        self.user = User(user_id=1)
        self.contact = ContactSchema(
            first_name='Stepan',
            last_name='The Cat',
            email='cat_stepan@gmail.com',
            telephon_number='0999998877',
            birthday=date(200, 1, 4),
            description='This is SupaCat',
            user_id=1
        )

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(contact_field=None, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_field(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(contact_field='The Cat', user=self.user, db=self.session)
        self.assertEqual(result, contacts)
    '''
    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter_by().return_value.first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)
    '''

    async def test_create_contact(self):
        body = self.contact
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.telephon_number, body.telephon_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "contact_id"))
    '''
    async def test_remove_contact_found(self):
        contact_id = 1
        contact = Contact(contact_id=contact_id)
        self.session.query(Contact).filter_by().first.return_value = contact
        result = await delete_contact(contact_id, user=self.user, db=self.session)
        self.assertEqual(result, contact)
    
    async def test_remove_contact_not_found(self):
        self.session.query(Contact).filter().first.return_value = None
        self.session.commit.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        print(result)
        self.assertIsNone(result)'''

    async def test_update_contact_found(self):
        body = self.contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.telephon_number, body.telephon_number)
        self.assertEqual(result.birthday, body.birthday)
        # self.assertTrue(hasattr(result, "contact_id"))

    async def test_update_note_not_found(self):
        body = self.contact
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)
    '''
    async def test_birthday_list_found(self):
        contacts = [Contact(birthday=datetime.now() + timedelta(days=1)),
                    Contact(birthday=datetime.now() + timedelta(days=2)),
                    Contact(birthday=datetime.now() + timedelta(days=3)),
                    Contact(birthday=datetime.now() + timedelta(days=4)),
                    Contact(birthday=datetime.now() + timedelta(days=5)),
                    Contact(birthday=datetime.now() + timedelta(days=6)),
                    Contact(birthday=datetime.now() + timedelta(days=7)),
                    Contact(birthday=datetime.now() + timedelta(days=8)),
                    Contact(birthday=datetime.now() + timedelta(days=9)),
                    Contact(birthday=datetime.now() + timedelta(days=10)),
                    ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, contacts[0:7])
        '''


if __name__ == '__main__':
    unittest.main()
