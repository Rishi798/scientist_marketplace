from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.extensions import db
from app.models import SupplierService, ServiceRequest, ServiceResponse

# Define the supplier blueprint
supplier_bp = Blueprint("supplier", __name__)

# Supplier dashboard to view all services
@supplier_bp.route('/dashboard')
def dashboard():
    services = SupplierService.query.all()
    return render_template('supplier/dashboard.html', services=services)

# Add a new service
@supplier_bp.route('/add', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        service_name = request.form['service_name']
        service_description = request.form.get('service_description', '')
        accreditation = request.form.get('accreditation', '')

        # Placeholder for logged-in supplier
        supplier_id = 1  

        new_service = SupplierService(
            service_name=service_name, 
            service_description=service_description, 
            accreditation=accreditation, 
            supplier_id=supplier_id
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/add_service.html')

# View and update service details
@supplier_bp.route('/service/<int:service_id>', methods=['GET', 'POST'])
def service_details(service_id):
    service = SupplierService.query.get_or_404(service_id)

    if request.method == 'POST':
        service.service_name = request.form['service_name']
        service.service_description = request.form.get('service_description', '')
        service.accreditation = request.form.get('accreditation', '')
        db.session.commit()
        flash('Service details updated successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/service_details.html', service=service)

# Edit an existing service
@supplier_bp.route('/edit/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    service = SupplierService.query.get_or_404(service_id)

    if request.method == 'POST':
        service.service_name = request.form['service_name']
        service.service_description = request.form.get('service_description', '')
        service.accreditation = request.form.get('accreditation', '')
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/edit_service.html', service=service)

# Delete a service along with related requests and responses
@supplier_bp.route('/delete/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    service = SupplierService.query.get_or_404(service_id)

    associated_requests = ServiceRequest.query.filter_by(service_id=service_id).all()

    for req in associated_requests:
        associated_responses = ServiceResponse.query.filter_by(request_id=req.request_id).all()
        for resp in associated_responses:
            db.session.delete(resp)
        db.session.delete(req)

    db.session.delete(service)
    db.session.commit()
    flash('Service and related requests/responses deleted successfully!', 'success')
    return redirect(url_for('supplier.dashboard'))

# View service requests for a specific service
@supplier_bp.route('/service_requests/<int:service_id>')
def view_requests(service_id):
    requests = ServiceRequest.query.filter_by(service_id=service_id).all()
    return render_template('supplier/view_requests.html', requests=requests, service_id=service_id)

# Respond to a service request with an option to reject
@supplier_bp.route('/respond/<int:request_id>', methods=['GET', 'POST'])
def respond_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)

    if request.method == 'POST':
        if 'reject' in request.form:
            new_response = ServiceResponse(
                request_id=request_id,
                supplier_id=1,  
                response_details="Rejected",
                price=None
            )
            db.session.add(new_response)
            db.session.commit()
            flash('Request rejected successfully!', 'warning')
            return redirect(url_for('supplier.dashboard'))

        response_details = request.form['response_details']
        price = float(request.form.get('price', 0))

        new_response = ServiceResponse(
            request_id=request_id,
            supplier_id=1,  
            response_details=response_details,
            price=price
        )
        db.session.add(new_response)
        db.session.commit()
        flash('Response sent successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/respond_request.html', request=service_request)
