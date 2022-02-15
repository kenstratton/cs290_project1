from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import timedelta
from main import db
from werkzeug.security import generate_password_hash, check_password_hash


# User class holds info of an actual user and relationships with multiple posts.
class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow() + timedelta(hours=-8))

    def __repr__(self):
        return '<Name %r>' % self.name

    @property
    def password(self):
        raise AttributeError("Password is not hashed.")

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

def db_init():
    db.create_all()