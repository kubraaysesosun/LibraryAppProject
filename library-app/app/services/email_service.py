from typing import Optional

from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config import settings


class EmailSchema(BaseModel):
    receiver_email: EmailStr
    subject: str
    body: dict
    template_name: Optional[str] = None


class EmailSender:
    def __init__(self):
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=True,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER=settings.TEMPLATE_FOLDER,
        )
        self.fm = FastMail(conf)

    async def send_email(self, email_schema: EmailSchema):
        message = MessageSchema(
            subject=email_schema.subject,
            recipients=[email_schema.receiver_email],
            template_body=email_schema.body,
            subtype="html",
        )

        await self.fm.send_message(message, email_schema.template_name)


email_sender = EmailSender()
