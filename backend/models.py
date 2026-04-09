from backend.extensions import db
from datetime import datetime, date


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    
    # Relationship
    student_profile = db.relationship('Student', backref='user', uselist=False)
    company_profile = db.relationship('Company', backref='user', uselist=False)

class Student(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    resume_path = db.Column(db.String(200), nullable=False)

    # Relationship
    applications = db.relationship('Application', backref='student', lazy=True)

class Company(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    hr_contact = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'

    # Relationship
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)

class PlacementDrive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligible_branch = db.Column(db.String(200), nullable=False)
    eligible_cgpa = db.Column(db.Float, nullable=False)
    eligible_year = db.Column(db.Integer, nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'closed', 'rejected'
    created_date = db.Column(db.Date, default=date.today)

    # Relationship
    applications = db.relationship('Application', backref='drive', cascade='all, delete-orphan', lazy=True)

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id', ondelete='CASCADE'), nullable=False)
    applied_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default='applied')  # 'applied', 'selected', 'rejected'
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # for unique application per student per drive
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_student_drive'),)
    
    