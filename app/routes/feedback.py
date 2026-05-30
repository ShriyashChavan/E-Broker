from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Feedback, Property, Tenant, Landlord, Admin

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/add/<int:pno>', methods=['GET', 'POST'])
@login_required
def add_feedback(pno):
    if not isinstance(current_user, Tenant):
        flash('Access denied', 'error')
        return redirect(url_for('properties.search'))

    property_obj = Property.query.get_or_404(pno)

    # Check if feedback already exists
    existing = Feedback.query.filter_by(pno=pno, tno=current_user.tno).first()
    if existing:
        flash('You have already submitted feedback for this property', 'warning')
        return redirect(url_for('properties.search'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        feedback = Feedback(
            rating=int(rating),
            comment=comment,
            tno=current_user.tno,
            pno=pno
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('properties.search'))

    return render_template('add_feedback.html', property=property_obj)

@feedback_bp.route('/property/<int:pno>')
@login_required
def view_property_feedback(pno):
    property_obj = Property.query.get_or_404(pno)

    # Only landlord of the property or admin can view feedback
    if isinstance(current_user, Landlord) and property_obj.lid != current_user.lid:
        flash('Access denied', 'error')
        return redirect(url_for('properties.landlord_dashboard'))
    elif isinstance(current_user, Tenant):
        flash('Access denied', 'error')
        return redirect(url_for('properties.search'))

    feedbacks = db.session.query(Feedback, Tenant)\
        .join(Tenant, Feedback.tno == Tenant.tno)\
        .filter(Feedback.pno == pno)\
        .all()

    return render_template('property_feedback.html', property=property_obj, feedbacks=feedbacks)

# API endpoints
@feedback_bp.route('/api/feedback/add', methods=['POST'])
@login_required
def api_add_feedback():
    data = request.get_json()
    pno = data.get('pno')
    rating = data.get('rating')
    comment = data.get('comment')

    if not isinstance(current_user, Tenant):
        return jsonify({'message': 'Access denied'}), 403

    property_obj = Property.query.get_or_404(pno)

    # Check if feedback already exists
    existing = Feedback.query.filter_by(pno=pno, tno=current_user.tno).first()
    if existing:
        return jsonify({'message': 'Feedback already exists'}), 400

    feedback = Feedback(
        rating=int(rating),
        comment=comment,
        tno=current_user.tno,
        pno=pno
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted successfully'}), 201

@feedback_bp.route('/api/feedback/property/<int:pno>', methods=['GET'])
@login_required
def api_property_feedback(pno):
    property_obj = Property.query.get_or_404(pno)

    # Only landlord of the property or admin can view feedback
    if isinstance(current_user, Landlord) and property_obj.lid != current_user.lid:
        return jsonify({'message': 'Access denied'}), 403
    elif isinstance(current_user, Tenant):
        return jsonify({'message': 'Access denied'}), 403

    feedbacks = db.session.query(Feedback, Tenant)\
        .join(Tenant, Feedback.tno == Tenant.tno)\
        .filter(Feedback.pno == pno)\
        .all()

    result = []
    for feedback, tenant in feedbacks:
        result.append({
            'fid': feedback.fid,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'tenant': {
                'tno': tenant.tno,
                'name': tenant.tname,
                'email': tenant.temail
            }
        })
    return jsonify(result)