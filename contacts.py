from sqlalchemy import or_, and_
from models import Contact, User
from typing import List
from sqlalchemy.orm import Session
from shemas import ContactSchema
from datetime import datetime


async def get_contacts(contact_field: str, user: User, db: Session) -> List[Contact] | Contact:
    """
    Retrieves a list of contacts for a specific user with specified search parameters.
        Args:
            contact_field (str): The parameter for search of the desired Contact.
            user (User): The User who owns the desired Contact.

    :param contact_field: contact field by which we search.
    :type contact_field: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact] | Contact
    """
    if not contact_field:
        contacts = db.query(Contact).filter(
            Contact.user_id == user.user_id).all()
        return contacts
    contact = db.query(Contact).filter(and_(Contact.user_id == user.user_id, or_(
        Contact.first_name == contact_field,
        Contact.last_name == contact_field,
        Contact.email == contact_field))).all()
    if contact:
        return contact


async def get_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified ID for a specific user.
        Args:
            contact_id (int): The id of the desired Contact.
            user (User): The User who owns the desired Contact.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.user_id == user.user_id, Contact.contact_id == contact_id)).first()
    return contact


async def create_contact(body: ContactSchema, user: User, db: Session) -> Contact:
    """
    Creates a new contact in the database for a specific user.
        Args:
            body (ContactModel): The contact to create.
            user (User): The current user, who is creating the contact.

    :param body: The data for the contact to create.
    :type body: ContactSchema
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact object.
    :rtype: Contact
    """
    contact = Contact(**body.model_dump(exclude_unset=True),
                      user_id=user.user_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.
        Args:        
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated contact information.
            user (User): The current user, used for authorization purposes.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactSchema
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.user_id == user.user_id, Contact.contact_id == contact_id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.telephon_number = body.telephon_number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
        db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging to this
            user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.user_id == user.user_id, Contact.contact_id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_birthdays(user: User, db: Session) -> List[Contact]:
    """
    The birthday_list function takes a user and database session as arguments.
    It returns a list of contacts whose birthdays are within the next 7 days.
        Args:
            user (User): The current user, used for authorization purposes.

    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts with birthdays in the next week    
    """
    contacts_list = []
    today = datetime.now().date()
    contacts_all = db.query(Contact).filter(
        Contact.user_id == user.user_id).all()
    for contact in contacts_all:
        days_ = (datetime(year=today.year,
                          month=contact.birthday.month,
                          day=contact.birthday.day).date() - today).days
        if 0 <= days_ < 7:
            contacts_list.append(contact)
    return contacts_list
