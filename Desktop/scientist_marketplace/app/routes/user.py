from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.extensions import db
from app.models import SupplierService, ServiceRequest, ServiceResponse

# Define the user blueprint
user_bp = Blueprint("user", __name__)

# User service list with search functionality
@user_bp.route('/services', methods=['GET'])
def service_list():
    query = request.args.get('q', '')

    if query:
        services = SupplierService.query.filter(
            (SupplierService.service_name.ilike(f"%{query}%")) |
            (SupplierService.service_description.ilike(f"%{query}%")) |
            (SupplierService.accreditation.ilike(f"%{query}%"))
        ).all()
    else:
        services = SupplierService.query.all()

    return render_template('user/service_list.html', services=services, query=query)

# User service details page
@user_bp.route('/services/<int:service_id>', methods=['GET'])
def service_details(service_id):
    service = SupplierService.query.get_or_404(service_id)
    return render_template('user/service_details.html', service=service)

# Submit a service request
@user_bp.route('/services/<int:service_id>/request', methods=['GET', 'POST'])
def submit_request(service_id):
    if request.method == 'POST':
        user_name = request.form['user_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        research_description = request.form['research_description']

        new_request = ServiceRequest(
            service_id=service_id,
            user_name=user_name,
            phone_number=phone_number,
            email=email,
            research_description=research_description
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Service request submitted successfully!', 'success')
        return redirect(url_for('user.my_requests'))

    service = SupplierService.query.get_or_404(service_id)
    return render_template('user/submit_request.html', service=service)

# View user service requests
@user_bp.route('/my_requests', methods=['GET'])
def my_requests():
    service_requests = ServiceRequest.query.all()
    responses = {resp.request_id: resp for resp in ServiceResponse.query.all()}
    return render_template('user/my_requests.html', service_requests=service_requests, responses=responses)
