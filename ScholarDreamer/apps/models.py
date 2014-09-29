"""
models.py

"""

from apps import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    user_student_num = db.Column(db.long, primary_key=True)
    user_prev1_grade = db.Column(db.Float)
    user_prev2_grade = db.Column(db.Float)
    user_all_grade = db.Column(db.Float)
    user_grade_condition = db.Column(db.Text)
    user_area_state = db.Column(db.String(255))
    user_area_city = db.Column(db.String(255))


class Scholarship(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    prev1_grade = db.Column(db.Float)
    prev2_grade = db.Column(db.Float)
    all_grade = db.Column(db.Float)
    grade_conditions = db.Column(db.Text)
    area_state = db.Column(db.String(255))
    area_city = db.Column(db.String(255))
    income = db.Column(db.Text)
    region = db.Column(db.Text)
    notes = db.Column(db.Text)
    recruitment_time = db.Column(db.Text)
    etc = db.Column(db.Text)
    contents = db.Column(db.Text)
    homepage = db.Column(db.String(255))

