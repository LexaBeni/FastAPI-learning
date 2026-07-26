from dependencies.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from core.settings import settings
from core.security import hash_password
from roles import UserRole

def ensure_default_admin(db: Session):
    stmt = select(User).where(User.role == UserRole.ADMIN)
    admin = db.execute(stmt)
    admin = admin.scalar_one_or_none()
    if not admin:

        new_admin = User(
            username=settings.admin_username,
            email=settings.admin_email,
            hashed_password=hash_password(settings.admin_password),
            role=UserRole.ADMIN,
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return new_admin
    
    return admin

