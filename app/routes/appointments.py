from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models import Appointment, Property, Tenant, Landlord
from datetime import datetime
from fpdf import FPDF
import io

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/book/<int:pno>', methods=['POST'])
@login_required
def book_appointment(pno):
    if not isinstance(current_user, Tenant):
        flash('Access denied', 'error')
        return redirect(url_for('properties.search'))

    property_obj = Property.query.get_or_404(pno)

    # Check if appointment already exists
    existing = Appointment.query.filter_by(pno=pno, tno=current_user.tno).first()
    if existing:
        flash('You have already booked an appointment for this property', 'warning')
        return redirect(url_for('properties.search'))

    appointment = Appointment(pno=pno, tno=current_user.tno)
    appointment.astatus = 'pending'
    db.session.add(appointment)
    db.session.commit()

    landlord_name = property_obj.landlord.lname if property_obj.landlord else 'Landlord'
    landlord_contact = property_obj.landlord.contact if property_obj.landlord else 'N/A'

    flash(f'Appointment booked successfully! Request sent to {landlord_name} ({landlord_contact}).', 'success')
    return redirect(url_for('properties.search'))

@appointments_bp.route('/landlord/appointments')
@login_required
def landlord_appointments():
    if not isinstance(current_user, Landlord):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    appointments = db.session.query(Appointment, Property, Tenant)\
        .join(Property, Appointment.pno == Property.pno)\
        .join(Tenant, Appointment.tno == Tenant.tno)\
        .filter(Property.lid == current_user.lid)\
        .order_by(Appointment.adate.desc())\
        .all()

    if not appointments:
        flash('No appointment requests found for your properties yet.', 'info')

    return render_template('landlord_appointments.html', appointments=appointments)

@appointments_bp.route('/update_status/<int:ano>/<status>', methods=['GET', 'POST'])
@login_required
def update_appointment_status(ano, status):
    if not isinstance(current_user, Landlord):
        flash('Access denied', 'error')
        return redirect(url_for('appointments.landlord_appointments'))

    appointment = Appointment.query.get_or_404(ano)
    property_obj = Property.query.get(appointment.pno)

    if property_obj.lid != current_user.lid:
        flash('Access denied', 'error')
        return redirect(url_for('appointments.landlord_appointments'))

    if request.method == 'POST':
        if status == 'accepted':
            schedule_str = request.form.get('schedule')
            if schedule_str:
                try:
                    schedule = datetime.strptime(schedule_str, '%Y-%m-%dT%H:%M')
                    appointment.schedule = schedule
                except ValueError:
                    flash('Invalid schedule date/time format', 'error')
                    return redirect(url_for('appointments.landlord_appointments'))
        appointment.astatus = status
        db.session.commit()
        flash(f'Appointment {status} successfully!', 'success')
        return redirect(url_for('appointments.landlord_appointments'))

    # For GET, render a form if accepting
    if status == 'accepted':
        return render_template('accept_appointment.html', appointment=appointment, property=property_obj, tenant=Tenant.query.get(appointment.tno))
    else:
        appointment.astatus = status
        db.session.commit()
        flash(f'Appointment {status} successfully!', 'success')
        return redirect(url_for('appointments.landlord_appointments'))

@appointments_bp.route('/tenant/appointments')
@login_required
def tenant_appointments():
    if not isinstance(current_user, Tenant):
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))

    appointments = db.session.query(Appointment, Property)\
        .join(Property, Appointment.pno == Property.pno)\
        .filter(Appointment.tno == current_user.tno)\
        .all()

    return render_template('tenant_appointments.html', appointments=appointments)

# API endpoints
@appointments_bp.route('/api/appointments/book', methods=['POST'])
@login_required
def api_book_appointment():
    data = request.get_json()
    pno = data.get('pno')

    if not isinstance(current_user, Tenant):
        return jsonify({'message': 'Access denied'}), 403

    property_obj = Property.query.get_or_404(pno)

    # Check if appointment already exists
    existing = Appointment.query.filter_by(pno=pno, tno=current_user.tno).first()
    if existing:
        return jsonify({'message': 'Appointment already exists'}), 400

    appointment = Appointment(pno=pno, tno=current_user.tno)
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked successfully'}), 201

@appointments_bp.route('/api/appointments/landlord', methods=['GET'])
@login_required
def api_landlord_appointments():
    if not isinstance(current_user, Landlord):
        return jsonify({'message': 'Access denied'}), 403

    appointments = db.session.query(Appointment, Property, Tenant)\
        .join(Property, Appointment.pno == Property.pno)\
        .join(Tenant, Appointment.tno == Tenant.tno)\
        .filter(Property.lid == current_user.lid)\
        .all()

    result = []
    for appointment, property_obj, tenant in appointments:
        result.append({
            'ano': appointment.ano,
            'property': {
                'pno': property_obj.pno,
                'address': property_obj.paddress,
                'location': property_obj.plocation
            },
            'tenant': {
                'tno': tenant.tno,
                'name': tenant.tname,
                'email': tenant.temail
            },
            'date': appointment.adate.isoformat(),
            'status': appointment.astatus
        })
    return jsonify(result)

@appointments_bp.route('/api/appointments/update_status', methods=['POST'])
@login_required
def api_update_status():
    data = request.get_json()
    ano = data.get('ano')
    status = data.get('status')

    if not isinstance(current_user, Landlord):
        return jsonify({'message': 'Access denied'}), 403

    appointment = Appointment.query.get_or_404(ano)
    property_obj = Property.query.get(appointment.pno)

    if property_obj.lid != current_user.lid:
        return jsonify({'message': 'Access denied'}), 403

    if status in ['accepted', 'rejected']:
        appointment.astatus = status
        db.session.commit()
        return jsonify({'message': f'Appointment {status}'}), 200

    return jsonify({'message': 'Invalid status'}), 400

@appointments_bp.route('/download_receipt/<int:ano>')
@login_required
def download_receipt(ano):
    appointment = Appointment.query.get_or_404(ano)
    if not isinstance(current_user, Tenant) or appointment.tno != current_user.tno:
        flash('Access denied', 'error')
        return redirect(url_for('appointments.tenant_appointments'))

    if appointment.astatus != 'accepted':
        flash('Receipt not available for this appointment', 'error')
        return redirect(url_for('appointments.tenant_appointments'))

    property_obj = Property.query.get(appointment.pno)
    landlord = property_obj.landlord
    tenant = current_user

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Appointment Receipt", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Landlord Name: {landlord.lname}", ln=True)
    pdf.cell(200, 10, txt=f"Tenant Name: {tenant.tname}", ln=True)
    pdf.cell(200, 10, txt=f"Contact Number: {landlord.contact}", ln=True)
    pdf.cell(200, 10, txt=f"Property Location: {property_obj.plocation}", ln=True)
    pdf.cell(200, 10, txt=f"Appointment Date & Time: {appointment.adate.strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Scheduled Time: {appointment.schedule.strftime('%Y-%m-%d %H:%M') if appointment.schedule else 'N/A'}", ln=True)

    # Save to buffer
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_bytes)

    from flask import send_file
    return send_file(buffer, as_attachment=True, download_name=f'receipt_{ano}.pdf', mimetype='application/pdf')

@appointments_bp.route('/download_receipt_landlord/<int:ano>')
@login_required
def download_receipt_landlord(ano):
    appointment = Appointment.query.get_or_404(ano)
    property_obj = Property.query.get(appointment.pno)
    if not isinstance(current_user, Landlord) or property_obj.lid != current_user.lid:
        flash('Access denied', 'error')
        return redirect(url_for('appointments.landlord_appointments'))

    if appointment.astatus != 'accepted':
        flash('Receipt not available for this appointment', 'error')
        return redirect(url_for('appointments.landlord_appointments'))

    landlord = current_user
    tenant = Tenant.query.get(appointment.tno)

    # Generate PDF (same as above)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Appointment Receipt", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Landlord Name: {landlord.lname}", ln=True)
    pdf.cell(200, 10, txt=f"Tenant Name: {tenant.tname}", ln=True)
    pdf.cell(200, 10, txt=f"Contact Number: {landlord.contact}", ln=True)
    pdf.cell(200, 10, txt=f"Property Location: {property_obj.plocation}", ln=True)
    pdf.cell(200, 10, txt=f"Appointment Date & Time: {appointment.adate.strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Scheduled Time: {appointment.schedule.strftime('%Y-%m-%d %H:%M') if appointment.schedule else 'N/A'}", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_bytes)

    return send_file(buffer, as_attachment=True, download_name=f'receipt_{ano}.pdf', mimetype='application/pdf')