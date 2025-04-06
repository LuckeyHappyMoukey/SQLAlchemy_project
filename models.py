# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.CHAR(1), db.CheckConstraint("gender IN ('M', 'F')"))
    height = db.Column(db.Integer)
    age = db.Column(db.Integer)