from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, case
from app import db
from app.models import Tenant, Landlord, Admin, Property, Appointment, Feedback

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    stats = {
        'tenants': Tenant.query.count(),
        'landlords': Landlord.query.count(),
        'properties': Property.query.count(),
        'appointments': Appointment.query.count(),
        'feedbacks': Feedback.query.count()
    }

    return render_template('admin_dashboard.html', stats=stats)

@admin_bp.route('/tenants')
@login_required
def manage_tenants():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    tenants = Tenant.query.all()
    return render_template('manage_tenants.html', tenants=tenants)

@admin_bp.route('/landlords')
@login_required
def manage_landlords():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    landlords = Landlord.query.all()
    return render_template('manage_landlords.html', landlords=landlords)

@admin_bp.route('/database')
@login_required
def view_database():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    # Get all data from database
    tenants = Tenant.query.all()
    landlords = Landlord.query.all()
    admins = Admin.query.all()
    properties = Property.query.all()
    appointments = db.session.query(Appointment, Property, Tenant, Landlord)\
        .join(Property, Appointment.pno == Property.pno)\
        .join(Tenant, Appointment.tno == Tenant.tno)\
        .join(Landlord, Property.lid == Landlord.lid)\
        .all()
    feedbacks = db.session.query(Feedback, Property, Tenant)\
        .join(Property, Feedback.pno == Property.pno)\
        .join(Tenant, Feedback.tno == Tenant.tno)\
        .all()

    stats = {
        'tenants': len(tenants),
        'landlords': len(landlords),
        'admins': len(admins),
        'properties': len(properties),
        'appointments': len(appointments),
        'feedbacks': len(feedbacks)
    }

    return render_template('database_view.html',
                         tenants=tenants,
                         landlords=landlords,
                         admins=admins,
                         properties=properties,
                         appointments=appointments,
                         feedbacks=feedbacks,
                         stats=stats)

@admin_bp.route('/reports')
@login_required
def reports():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    daily_data = db.session.query(
        func.date(Appointment.adate).label('date'),
        func.count(Appointment.ano).label('total'),
        func.sum(case((Appointment.astatus == 'accepted', 1), else_=0)).label('accepted'),
        func.sum(case((Appointment.astatus == 'rejected', 1), else_=0)).label('rejected'),
        func.sum(case((Appointment.astatus == 'pending', 1), else_=0)).label('pending')
    ).group_by(func.date(Appointment.adate)).order_by(func.date(Appointment.adate).desc()).all()

    daily_reports = [
        {
            'date': row.date,
            'total': row.total,
            'accepted': row.accepted,
            'rejected': row.rejected,
            'pending': row.pending
        }
        for row in daily_data
    ]

    overall = {
        'tenants': Tenant.query.count(),
        'landlords': Landlord.query.count(),
        'properties': Property.query.count(),
        'appointments': Appointment.query.count(),
        'accepted': Appointment.query.filter_by(astatus='accepted').count(),
        'rejected': Appointment.query.filter_by(astatus='rejected').count(),
        'pending': Appointment.query.filter_by(astatus='pending').count(),
        'feedbacks': Feedback.query.count()
    }

    return render_template('admin_reports.html', daily_reports=daily_reports, overall=overall)

@admin_bp.route('/properties')
@login_required
def manage_properties():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    properties = Property.query.all()
    return render_template('manage_properties.html', properties=properties)

@admin_bp.route('/appointments')
@login_required
def manage_appointments():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    appointments = db.session.query(Appointment, Property, Tenant, Landlord)\
        .join(Property, Appointment.pno == Property.pno)\
        .join(Tenant, Appointment.tno == Tenant.tno)\
        .join(Landlord, Property.lid == Landlord.lid)\
        .all()

    return render_template('manage_appointments.html', appointments=appointments)

@admin_bp.route('/feedbacks')
@login_required
def manage_feedbacks():
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    feedbacks = db.session.query(Feedback, Property, Tenant)\
        .join(Property, Feedback.pno == Property.pno)\
        .join(Tenant, Feedback.tno == Tenant.tno)\
        .all()

    return render_template('manage_feedbacks.html', feedbacks=feedbacks)

@admin_bp.route('/delete_tenant/<int:tno>')
@login_required
def delete_tenant(tno):
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('admin.manage_tenants'))

    tenant = Tenant.query.get_or_404(tno)
    db.session.delete(tenant)
    db.session.commit()
    flash('Tenant deleted successfully!', 'success')
    return redirect(url_for('admin.manage_tenants'))

@admin_bp.route('/delete_landlord/<int:lid>')
@login_required
def delete_landlord(lid):
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('admin.manage_landlords'))

    landlord = Landlord.query.get_or_404(lid)
    db.session.delete(landlord)
    db.session.commit()
    flash('Landlord deleted successfully!', 'success')
    return redirect(url_for('admin.manage_landlords'))

@admin_bp.route('/delete_property/<int:pno>')
@login_required
def delete_property(pno):
    if not isinstance(current_user, Admin):
        flash('Access denied', 'error')
        return redirect(url_for('admin.manage_properties'))

    property_obj = Property.query.get_or_404(pno)
    db.session.delete(property_obj)
    db.session.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('admin.manage_properties'))

# API endpoints
@admin_bp.route('/api/stats', methods=['GET'])
@login_required
def api_stats():
    if not isinstance(current_user, Admin):
        return jsonify({'message': 'Access denied'}), 403

    stats = {
        'tenants': Tenant.query.count(),
        'landlords': Landlord.query.count(),
        'properties': Property.query.count(),
        'appointments': Appointment.query.count(),
        'feedbacks': Feedback.query.count()
    }
    return jsonify(stats)

@admin_bp.route('/api/tenants', methods=['GET'])
@login_required
def api_tenants():
    if not isinstance(current_user, Admin):
        return jsonify({'message': 'Access denied'}), 403

    tenants = Tenant.query.all()
    result = []
    for tenant in tenants:
        result.append({
            'tno': tenant.tno,
            'tname': tenant.tname,
            'temail': tenant.temail,
            'tage': tenant.tage,
            'tcontact': tenant.tcontact
        })
    return jsonify(result)

@admin_bp.route('/api/landlords', methods=['GET'])
@login_required
def api_landlords():
    if not isinstance(current_user, Admin):
        return jsonify({'message': 'Access denied'}), 403

    landlords = Landlord.query.all()
    result = []
    for landlord in landlords:
        result.append({
            'lid': landlord.lid,
            'lname': landlord.lname,
            'lemail': landlord.lemail,
            'contact': landlord.contact
        })
    return jsonify(result)