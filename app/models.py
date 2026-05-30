from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Tenant(db.Model, UserMixin):
    __tablename__ = 'tenant'
    tno = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(100), nullable=False)
    tpass = db.Column(db.String(255), nullable=False)
    temail = db.Column(db.String(120), unique=True, nullable=False)
    tage = db.Column(db.Integer)
    tcontact = db.Column(db.String(20))

    appointments = db.relationship('Appointment', backref='tenant', lazy=True)
    feedbacks = db.relationship('Feedback', backref='tenant', lazy=True)

    def set_password(self, password):
        self.tpass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.tpass, password)

    def get_id(self):
        return f"tenant:{self.tno}"

class Landlord(db.Model, UserMixin):
    __tablename__ = 'landlord'
    lid = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(100), nullable=False)
    lpass = db.Column(db.String(255), nullable=False)
    lemail = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20))

    properties = db.relationship('Property', backref='landlord', lazy=True)

    def set_password(self, password):
        self.lpass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.lpass, password)

    def get_id(self):
        return f"landlord:{self.lid}"

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    aid = db.Column(db.Integer, primary_key=True)
    aname = db.Column(db.String(100), nullable=False)
    aemail = db.Column(db.String(120), unique=True, nullable=False)
    apass = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.apass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.apass, password)

    def get_id(self):
        return f"admin:{self.aid}"

class Property(db.Model):
    __tablename__ = 'property'
    pno = db.Column(db.Integer, primary_key=True)
    ptype = db.Column(db.String(50), nullable=False)
    paddress = db.Column(db.Text, nullable=False)
    plocation = db.Column(db.String(100), nullable=False)
    carpet = db.Column(db.Float, nullable=False)
    img1 = db.Column(db.String(255))
    bhk = db.Column(db.Integer, nullable=False)
    no_of_tenant = db.Column(db.Integer, default=1)
    lid = db.Column(db.Integer, db.ForeignKey('landlord.lid'), nullable=False)

    appointments = db.relationship('Appointment', backref='property', lazy=True)
    feedbacks = db.relationship('Feedback', backref='property', lazy=True)
    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade='all, delete-orphan')

class Appointment(db.Model):
    __tablename__ = 'appointment'
    ano = db.Column(db.Integer, primary_key=True)
    pno = db.Column(db.Integer, db.ForeignKey('property.pno'), nullable=False)
    tno = db.Column(db.Integer, db.ForeignKey('tenant.tno'), nullable=False)
    adate = db.Column(db.DateTime, default=datetime.utcnow)
    astatus = db.Column(db.String(20), default='pending')
    schedule = db.Column(db.DateTime, nullable=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    fid = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    tno = db.Column(db.Integer, db.ForeignKey('tenant.tno'), nullable=False)
    pno = db.Column(db.Integer, db.ForeignKey('property.pno'), nullable=False)

class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.pno', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

