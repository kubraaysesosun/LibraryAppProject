from app.models import User
from app.database.core import SessionLocal


def make_user_admin(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_admin = True
            db.commit()
            print(
                f"{email} kullanıcısı başarıyla yönetici olarak işaretlendi."
            )
        else:
            print(f"{email} kullanıcısı bulunamadı.")
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python make_user_admin.py <email>")
        sys.exit(1)
    email_address: str = sys.argv[1]
    make_user_admin(email_address)
