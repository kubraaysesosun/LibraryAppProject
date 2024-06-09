import logging

from celery import shared_task
from datetime import timedelta, date

from openpyxl import Workbook
from sqlalchemy import select, func

from app.config import settings
from app.models import Borrow, User, Book
from app.database.core import SessionLocal
from app.services.email_service import email_sender, EmailSchema

logger = logging.getLogger(__name__)


@shared_task
def send_return_reminders():
    db = SessionLocal()
    try:
        today = date.today()
        q = (
            select(
                Borrow.expire_date.label("expire_date"),
                Book.name.label("book_name"),
                User.email.label("user_email"),
                User.full_name.label("user_full_name"),
            )
            .select_from(Borrow)
            .join(Book)
            .join(User)
            .filter(Borrow.is_refunded == False, Borrow.expire_date < today)
        )
        overdue_borrows = db.execute(q)

        for row in overdue_borrows:
            if not settings.DEVELOPER_MODE:
                email_schema: EmailSchema = EmailSchema(
                    receiver_email=row.user_email,
                    subject="Overdue Borrow",
                    body={
                        "user_email": row.user_email,
                        "user_full_name": row.user_full_name,
                        "book_name": row.book_name,
                        "expire_date": row.expire_date,
                    },
                    template_name="overdue_email.html",
                )
                email_sender.send_email(email_schema)
            else:
                logger.info(
                    f"{row.user_email} --- Reminder: You must return {row.book_name}!"
                )
    finally:
        db.close()


@shared_task
def generate_weekly_report():
    db = SessionLocal()
    try:
        today = date.today()
        start_of_week = today - timedelta(days=7)
        end_of_week = today

        q = (
            select(
                Book.name.label("book_name"),
                func.count(Borrow.id).label("borrow_count"),
            )
            .select_from(Borrow)
            .join(Book)
            .filter(
                Borrow.borrowed_date >= start_of_week,
                Borrow.borrowed_date < end_of_week,
            )
            .group_by(Book.name)
        )
        book_borrows_count = db.execute(q)

        wb = Workbook()
        ws = wb.active

        ws.append(["Book Name", "Borrow Count"])
        for row in list(book_borrows_count):
            ws.append([row.book_name, row.borrow_count])

        file_name = f"reports/{today.strftime('%Y-%m-%d')}_weekly_report.xlsx"
        wb.save(file_name)
    finally:
        db.close()
