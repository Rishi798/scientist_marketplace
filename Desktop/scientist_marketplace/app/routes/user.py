from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models import SupplierService, ServiceRequest, ServiceResponse
from groq import Groq
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")
client = Groq(api_key=api_key)

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

# AI-powered service recommendation using Groq API
@user_bp.route('/ai_search', methods=['POST'])
def ai_search():
    user_input = request.json.get('query')
    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Groq API chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that recommends research services based on user input. "
                               "Your responses should be relevant to scientific services available in the database."
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stream=False
        )

        # Extract the AI response
        ai_response = chat_completion.choices[0].message.content.strip()

        # Log the AI response
        print(f"AI Response: {ai_response}")

        # Extract potential keywords from AI response
        keywords = re.findall(r'\b\w+\b', ai_response)
        keywords = [kw.lower() for kw in keywords if len(kw) > 2]

        # Query the database using extracted keywords
        query = db.session.query(SupplierService)
        for keyword in keywords:
            query = query.filter(
                (SupplierService.service_name.ilike(f"%{keyword}%")) |
                (SupplierService.service_description.ilike(f"%{keyword}%"))
            )
        services = query.all()

        # Format response
        response_data = {
            "ai_response": ai_response,
            "services": [
                {
                    "id": service.service_id,
                    "name": service.service_name,
                    "description": service.service_description,
                    "accreditation": service.accreditation
                }
                for service in services
            ]
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
