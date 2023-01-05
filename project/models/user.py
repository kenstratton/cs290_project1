# models > user.py


from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from project import db
from werkzeug.security import generate_password_hash, check_password_hash

# User class holds info of an actual user and relationships with multiple posts.
class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    confirmed = Column(Boolean, nullable=False, default=False) #いらない(view内のロジックで管理)
    date_added = Column(DateTime, default=datetime.utcnow() + timedelta(hours=-8))

    def __repr__(self):
        return '<Name %r>' % self.name

    @property
    def password(self):
        raise AttributeError("Password is not hashed.")

    @password.setter
    def password(self, psw):
        self.hashed_password = generate_password_hash(psw)

    def verify_password(self, psw):
        return check_password_hash(self.hashed_password, psw)