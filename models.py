from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Stable') # Stable, Critical, Recovering
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    icu_admitted = db.Column(db.Boolean, default=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    performance_score = db.Column(db.Float, default=0.0) # out of 100
    active_patients = db.Column(db.Integer, default=0)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Medicine, Equipment, Bed
    quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='Available') # Available, Low Stock, Occupied

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Scheduled') # Scheduled, Completed, Cancelled
    predicted_wait_time = db.Column(db.Integer, default=0) # in minutes
