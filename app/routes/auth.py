from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
from app import db
from app.models import Tenant, Landlord, Admin
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        user = None
        if user_type == 'tenant':
            user = Tenant.query.filter_by(temail=email).first()
        elif user_type == 'landlord':
            user = Landlord.query.filter_by(lemail=email).first()
        elif user_type == 'admin':
            user = Admin.query.filter_by(aemail=email).first()

        # Fallback: try to detect the correct user type if the selection was wrong
        if not user and email and password:
            candidate = Tenant.query.filter_by(temail=email).first()
            if candidate and candidate.check_password(password):
                user = candidate
                user_type = 'tenant'
            else:
                candidate = Landlord.query.filter_by(lemail=email).first()
                if candidate and candidate.check_password(password):
                    user = candidate
                    user_type = 'landlord'
                else:
                    candidate = Admin.query.filter_by(aemail=email).first()
                    if candidate and candidate.check_password(password):
                        user = candidate
                        user_type = 'admin'

        if user and user.check_password(password):
            login_user(user)
            if user_type == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user_type == 'landlord':
                return redirect(url_for('properties.landlord_dashboard'))
            else:
                return redirect(url_for('properties.search'))

        flash('Invalid email or password', 'error')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        contact = request.form.get('contact')
        age = request.form.get('age') if user_type == 'tenant' else None

        if user_type == 'tenant':
            if Tenant.query.filter_by(temail=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('auth.register'))
            user = Tenant(tname=name, temail=email, tcontact=contact, tage=age)
        elif user_type == 'landlord':
            if Landlord.query.filter_by(lemail=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('auth.register'))
            user = Landlord(lname=name, lemail=email, contact=contact)

        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# API endpoints for mobile app
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    user = None
    if user_type == 'tenant':
        user = Tenant.query.filter_by(temail=email).first()
    elif user_type == 'landlord':
        user = Landlord.query.filter_by(lemail=email).first()
    elif user_type == 'admin':
        user = Admin.query.filter_by(aemail=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.get_id(), 'type': user_type})
        return jsonify({'access_token': access_token, 'user_type': user_type}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    user_type = data.get('user_type')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    contact = data.get('contact')
    age = data.get('age') if user_type == 'tenant' else None

    if user_type == 'tenant':
        if Tenant.query.filter_by(temail=email).first():
            return jsonify({'message': 'Email already registered'}), 400
        user = Tenant(tname=name, temail=email, tcontact=contact, tage=age)
    elif user_type == 'landlord':
        if Landlord.query.filter_by(lemail=email).first():
            return jsonify({'message': 'Email already registered'}), 400
        user = Landlord(lname=name, lemail=email, contact=contact)

    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201