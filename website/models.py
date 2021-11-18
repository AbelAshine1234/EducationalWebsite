from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name= db.Column(db.String(200))
    if type == "student":
        type = db.Column(db.String(20),default="student")
    elif type == "instructor":
        type = db.Column(db.String(20),default="instructor")
    elif type=="administrator":
        type = db.Column(db.String(20),default="administrator")

    else:
        type = db.Column(db.String(20),default="unknown")
    questions_asked = db.relationship(
        'Question',
        foreign_keys="Question.asked_by_id",
        backref='asker', 
        lazy=True
        ) 
    answer_requested  = db.relationship(
        'Question',
        foreign_keys="Question.asked_to_id ",
        backref='instructor', 
        lazy=True
        ) 

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    chapter = db.Column(db.String(20))
    section = db.Column(db.String(20))
    subject = db.Column(db.String(50))
    content = db.Column(db.Text)
    teacher = db.Column(db.String(34))
     
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    question = db.Column(db.Text)
    answer =  db.Column(db.Text)
    asked_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    asked_to_id =  db.Column(db.Integer,db.ForeignKey('user.id'))

class Course(db.Model):
     id = db.Column(db.Integer, primary_key=True)  
     coursename = db.Column(db.String(20))

    
     



    
   
