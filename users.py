from libgravatar import Gravatar
from sqlalchemy.orm import Session

from models import User
from shemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.

    :param email: Pass the email of the user to be retrieved.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: A user object if the user exists, and none if it doesn't.
    :rtype: User | None
    """
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the data to be inserted into the database.           

    :param body: Validate the data that is passed in.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The new user object.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: Get the user's id, which is used to find the user in the database
    :type user: User
    :param token: Update the refresh token in the database
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.

    :param email: Pass in the email of the user that is being confirmed
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :type email: str
    :param url: Specify the type of data that is being passed into the function
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: A user object
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_user_password(email: str, password: str, db: Session) -> User:
    """
    The update_user_password function updates a user's password in the database.
        Args:
            email (str): The email of the user to update.
            password (str): The new password for the user.

    :param email: Find the user in the database and update their password
    :type email: str
    :param password: Pass the new password to the function
    :type password: str
    :param db: The database session.
    :type db: Session
    :return: The updated user
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.password = password
    db.commit()
    return user
