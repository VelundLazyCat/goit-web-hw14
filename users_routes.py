from fastapi import APIRouter, Depends, status, UploadFile, File, BackgroundTasks, HTTPException, Request
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from my_db import get_db
from models import User
import users as repository_users
from auth import auth_service
from config import settings
from shemas import UserDb
from user_email import send_email_password


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)) -> User:
    """
    The read_users_me function is a GET endpoint that returns the current user's information.
        Args:
            current_user (User): The user whose avatar is being updated. This is passed in by the auth_service dependency,
                                 which uses JWT tokens to authenticate users and pass them into functions that require authentication. 
                                 See auth_service for more details on how this works.

    :param current_user: Pass the current user to the function.
    :type current_user: User
    :return: The current user object.
    :rtype: User
    """
    return current_user
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)) -> User:
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The image to be uploaded as an avatar.
            current_user (User): The user whose avatar is being updated.  This is passed in by the auth_service dependency, which uses JWT tokens to authenticate users and pass them into functions that require authentication.  See auth_service for more details on how this works.
            db (Session): A database session object used for querying and updating data in the database using SQLAlchemy's ORM methods.

    :param file: Upload the file to cloudinary.
    :type file: UploadFile
    :param current_user: Get the current user's email and username.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A user object
    :rtype: User
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    cloudinary.uploader.upload(
        file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}') \
        .build_url(width=250, height=250, crop='fill')
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


@router.patch('/update_password', response_model=UserDb)
async def update_password_user(password, background_tasks: BackgroundTasks, request: Request, current_user: User = Depends(auth_service.get_current_user),
                               db: Session = Depends(get_db)):
    """
    The update_password_user function updates the password of a user.
        The function takes in the new password, and returns the updated user object.

    :param password: Get the password from the request body.
    :type password: str
    :param background_tasks: Add a task to the background queue.
    :type background_tasks: BackgroundTasks
    :param request: Get the base url of the server.
    :type request: Request
    :param current_user: Get the current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The user object.
    :rtype: User
    """
    password = auth_service.get_password_hash(password)
    user = await repository_users.update_user_password(current_user.email, password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    background_tasks.add_task(
        send_email_password, user.email, user.username, request.base_url)
    return user
