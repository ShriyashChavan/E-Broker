from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from app import db
from app.models import Property, Landlord, Tenant, Admin, PropertyImage
import os

properties_bp = Blueprint('properties', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@properties_bp.route('/')
def index():
    return render_template('index.html')

@properties_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))

    properties = Property.query.options(joinedload(Property.images)).all()
    if request.method == 'POST':
        location = request.form.get('location')
        min_rent = request.form.get('min_rent')
        max_rent = request.form.get('max_rent')
        property_type = request.form.get('property_type')
        bhk = request.form.get('bhk')

        query = Property.query.options(joinedload(Property.images))

        if location:
            query = query.filter(Property.plocation.ilike(f'%{location}%'))
        if min_rent:
            query = query.filter(Property.carpet >= float(min_rent))
        if max_rent:
            query = query.filter(Property.carpet <= float(max_rent))
        if property_type:
            query = query.filter(Property.ptype == property_type)
        if bhk:
            query = query.filter(Property.bhk == int(bhk))

        properties = query.all()

    return render_template('search.html', properties=properties)

@properties_bp.route('/landlord/dashboard')
@login_required
def landlord_dashboard():
    if not isinstance(current_user, Landlord):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    properties = Property.query.options(joinedload(Property.images)).filter_by(lid=current_user.lid).all()
    return render_template('landlord_dashboard.html', properties=properties)

@properties_bp.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    if not isinstance(current_user, Landlord):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        ptype = request.form.get('ptype')
        paddress = request.form.get('paddress')
        plocation = request.form.get('plocation')
        carpet = request.form.get('carpet')
        bhk = request.form.get('bhk')
        no_of_tenant = request.form.get('no_of_tenant')

        property_obj = Property(
            ptype=ptype,
            paddress=paddress,
            plocation=plocation,
            carpet=float(carpet),
            bhk=int(bhk),
            no_of_tenant=int(no_of_tenant),
            lid=current_user.lid
        )

        # Handle image upload
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('app', 'static', 'images'))
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        if 'img1' in request.files:
            file = request.files['img1']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                property_obj.img1 = filename

        if not property_obj.img1:
            property_obj.img1 = 'default_property.svg'

        db.session.add(property_obj)
        db.session.flush()

        if property_obj.img1 and property_obj.img1 != 'default_property.svg':
            image_url = url_for('static', filename=f'images/{property_obj.img1}')
            property_img = PropertyImage(property_id=property_obj.pno, image_url=image_url)
            db.session.add(property_img)

        db.session.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('properties.landlord_dashboard'))

    return render_template('add_property.html')

@properties_bp.route('/edit_property/<int:pno>', methods=['GET', 'POST'])
@login_required
def edit_property(pno):
    if not isinstance(current_user, Landlord):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    property_obj = Property.query.get_or_404(pno)
    if property_obj.lid != current_user.lid:
        flash('Access denied', 'error')
        return redirect(url_for('properties.landlord_dashboard'))

    if request.method == 'POST':
        property_obj.ptype = request.form.get('ptype')
        property_obj.paddress = request.form.get('paddress')
        property_obj.plocation = request.form.get('plocation')
        property_obj.carpet = float(request.form.get('carpet'))
        property_obj.bhk = int(request.form.get('bhk'))
        property_obj.no_of_tenant = int(request.form.get('no_of_tenant'))

        # Handle image upload
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('app', 'static', 'images'))
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        if 'img1' in request.files:
            file = request.files['img1']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                property_obj.img1 = filename

                PropertyImage.query.filter_by(property_id=property_obj.pno).delete()
                image_url = url_for('static', filename=f'images/{property_obj.img1}')
                property_img = PropertyImage(property_id=property_obj.pno, image_url=image_url)
                db.session.add(property_img)

        if not property_obj.img1:
            property_obj.img1 = 'default_property.svg'

        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('properties.landlord_dashboard'))

    return render_template('edit_property.html', property=property_obj)

@properties_bp.route('/delete_property/<int:pno>')
@login_required
def delete_property(pno):
    if not isinstance(current_user, Landlord):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    property_obj = Property.query.get_or_404(pno)
    if property_obj.lid != current_user.lid:
        flash('Access denied', 'error')
        return redirect(url_for('properties.landlord_dashboard'))

    db.session.delete(property_obj)
    db.session.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('properties.landlord_dashboard'))

# API endpoints
@properties_bp.route('/api/properties', methods=['GET'])
def api_get_properties():
    properties = Property.query.all()
    result = []
    for prop in properties:
        result.append({
            'pno': prop.pno,
            'ptype': prop.ptype,
            'paddress': prop.paddress,
            'plocation': prop.plocation,
            'carpet': prop.carpet,
            'img1': prop.img1,
            'bhk': prop.bhk,
            'no_of_tenant': prop.no_of_tenant,
            'landlord': prop.landlord.lname,
            'images': [img.image_url for img in prop.images]
        })
    return jsonify(result)

@properties_bp.route('/api/properties/search', methods=['POST'])
def api_search_properties():
    data = request.get_json()
    location = data.get('location')
    min_rent = data.get('min_rent')
    max_rent = data.get('max_rent')
    property_type = data.get('property_type')
    bhk = data.get('bhk')

    query = Property.query

    if location:
        query = query.filter(Property.plocation.ilike(f'%{location}%'))
    if min_rent:
        query = query.filter(Property.carpet >= float(min_rent))
    if max_rent:
        query = query.filter(Property.carpet <= float(max_rent))
    if property_type:
        query = query.filter(Property.ptype == property_type)
    if bhk:
        query = query.filter(Property.bhk == int(bhk))

    properties = query.all()
    result = []
    for prop in properties:
        result.append({
            'pno': prop.pno,
            'ptype': prop.ptype,
            'paddress': prop.paddress,
            'plocation': prop.plocation,
            'carpet': prop.carpet,
            'img1': prop.img1,
            'bhk': prop.bhk,
            'no_of_tenant': prop.no_of_tenant,
            'images': [img.image_url for img in prop.images]
        })
    return jsonify(result)