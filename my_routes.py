
from fastapi import APIRouter, HTTPException, Depends, status, Query
from my_db import get_db
from shemas import ContactSchema, ContactResponse
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
import contacts
from contacts import User
from auth import auth_service


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(contact_field: str = Query(None), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.
    May search_field function searches for a contacts in the database.
    It takes a string as an argument and returns all contacts that contain this string in any of their fields.
    If no such contacts are found, it raises an HTTPException with status code 404.
        Args:
            contact_field (str): The parameter for search of the desired Contact.            
            db (Session): A database session object used for querying and updating data in the database using SQLAlchemy's ORM methods.
            current_user (User): The User who owns the desired Contact.

    :param contact_field: The parameter for search of the desired Contact.
    :type contact_field: str
    :param db: The database session.
    :type db: Session
    :param current_user: Get the current user from the auth_service.
    :type current_user: User
    :return: A list of contacts
    :rtype: List[Contact]
    """
    contacts_ = await contacts.get_contacts(contact_field, current_user, db)
    if contacts_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACTS NOT FOUND')
    return contacts_


@router.get('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a single contact with the specified ID for a specific user.
        Args:
            contact_id (int): The id of the desired Contact.
            db (Session): A database session object used for querying and updating data in the database using SQLAlchemy's ORM methods.
            current_user (User): The User who owns the desired Contact.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve the contact for.
    :type current_user: User    
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = await contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACT NOT FOUND')
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactSchema, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new contact in the database for a specific user.
        Args:
            body (ContactModel): The contact to create.
            db (Session): A database session object used for querying and updating data in the database using SQLAlchemy's ORM methods.
            current_user (User): The current user, who is creating the contact.

    :param body: The data for the contact to create.
    :type body: ContactSchema
    :param db: The database session.
    :type db: Session
    :param current_user: The user to create the contact for.
    :type current_user: User    
    :return: The contact object.
    :rtype: Contact
    """
    contact = await contacts.create_contact(body, current_user, db)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactSchema, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            body (ContactSchema): object containing the new values for the contact.
            contact_id (int): An integer representing the id of an existing contact to be updated.
            db (Session): A database session object used for querying and updating data in the database using SQLAlchemy's ORM methods.
            current_user (User): The current user, who is creating the contact.


    :param body: Get the contact data from the request body.
    :type body : ContactSchema
    :param contact_id: Specify the id of the contact to update.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: Get the current user.
    :type current_user: User
    :return: The updated contact
    :rtype: Contact
    """
    contact = await contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACT NOT FOUND')
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse,
               description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Removes a single contact with the specified ID for a specific user.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging to this
            user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to remove the contact for.
    :type current_user: User
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = await contacts.delete_contact(contact_id, current_user, db)
    return contact


@router.get('/7', response_model=list[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_birthdays(db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    """
    The birthday_list function takes a user and database session as arguments.
    It returns a list of contacts whose birthdays are within the next 7 days.
        Args:
            user (User): The current user, used for authorization purposes.

    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts with birthdays in the next week    
    """
    contacts_ = await contacts.get_contacts_birthdays(current_user, db)
    if contacts_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACTS NOT FOUND')
    return contacts_
