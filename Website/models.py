from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class QueueEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    notified = db.Column(db.Boolean, default=False)  # New field to track notification status


class User(db.Model, UserMixin):  # Inherit from UserMixin
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.id