from sqlalchemy import select
from models.user import User
from core.exception import UserAlreadyExists, InvalidCredentials


class UserSerise():
    def __init__(self, db):
        self.db = db
    
    def get_user_by_username(self, user_name):
        stmt = select(User).where(User.username == user_name)
        result = self.db.execute(stmt)
        outcome = result.scalar_one_or_none()
        return outcome

    def get_user_by_email(self, email):
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        outcome = result.scalar_one_or_none()

        return outcome
    
    def get_user_by_id(self, id):
        stmt = select(User).where(User.id == id)
        result = self.db.execute(stmt)
        outcome = result.scalar_one_or_none()
        
        return outcome
    
    def register_user(self, user):
        from core.security import hash_password

        if self.get_user_by_email(user.email):
            raise UserAlreadyExists(user.email)
        if self.get_user_by_username(user.username):
            raise UserAlreadyExists(user.username)
        
        password = hash_password(user.password)

        db_user = User(
            username= user.username,
            email= user.email,
            hashed_password= password
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def log_in_user(self, login):
        from core.security import verify_password

        user = self.get_user_by_username(login.username)

        if user is None:
            raise InvalidCredentials()

        if verify_password(login.password, user.hashed_password) is False:
            raise InvalidCredentials()
        
        return user
        

    

    

        
