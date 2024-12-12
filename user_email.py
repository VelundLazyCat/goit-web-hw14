from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from auth import auth_service
from config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        The function takes in three parameters:
            -email (EmailStr): the user's email address.
            -username (str): the username of the user who is registering for an account.  This will be used in a greeting message within the body of the email sent to them.
            -host (str): this is where we are hosting our application (i.e., localhost).  This will be used as part of a URL that users can click on within their emails.

    :param email: Validate the email address.
    :type email: EmailStr
    :param username: Get the username of the user.
    :type username: str
    :param host: Send the host to the email template.
    :type host: str
    :return: A coroutine object, which is an awaitable. 
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username,
                           "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)


async def send_email_password(email: EmailStr, username: str, host: str):
    """
    The send_email_password function sends an email to the user with a link to reset their password.
        Args:
            email (str): The user's email address.
            username (str): The user's username.
            host (str): The host of the website, used for generating links in emails.

    :param email: Specify the email address of the recipient.
    :type email: EmailStr
    :param username: Pass the username to the template.
    :type username: str
    :param host: Create the link to the reset password page.
    :type host: str
    :return: A coroutine object.    
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Your information was updated",
            recipients=[email],
            template_body={"host": host, "username": username,
                           "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_password_template.html")
    except ConnectionErrors as err:
        print(err)
