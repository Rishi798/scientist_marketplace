from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models import SupplierService, ServiceRequest, ServiceResponse
from groq import Groq
import os
from dotenv import load_dotenv

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
        # Fetch all available services from the database
        all_services = SupplierService.query.all()
        service_names = [service.service_name for service in all_services]

        # Create a prompt for the AI to choose the best matching services
        service_list_str = "\n".join(service_names)
        prompt = (
            f"You are an AI assistant specializing in recommending scientific research services. "
            f"Here is a list of available services:\n{service_list_str}\n"
            f"Based on the user's input, recommend the most relevant services from this list. "
            f"Make sure to only choose from the provided services."
        )

        # Groq API chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stream=False
        )

        # Extract the AI response
        ai_response = chat_completion.choices[0].message.content.strip()
        print(f"AI Response: {ai_response}")

        # Extract recommended services from the structured AI response
        recommended_services = []
        unmatched_services = []
        for line in ai_response.splitlines():
            # Match lines that are formatted as bullet points or numbered lists
            line = line.strip("-•1234567890. ").lower()
            matched = False
            for service_name in service_names:
                if service_name.lower() in line:
                    matching_services = [
                        service for service in all_services if service.service_name.lower() == service_name.lower()
                    ]
                    recommended_services.extend(matching_services)
                    matched = True
                    break
            if not matched:
                unmatched_services.append(line)

        # Deduplicate the list by service ID
        recommended_services = list({service.service_id: service for service in recommended_services}.values())

        # Format response for matched and unmatched services
        response_data = [
            {
                "id": service.service_id,
                "name": service.service_name,
                "description": service.service_description,
                "accreditation": service.accreditation
            }
            for service in recommended_services
        ]

        response_message = {
            "response": ai_response,
            "services": response_data
        }

        if unmatched_services:
            response_message["unmatched"] = f"Some recommended services were not found in the database: {', '.join(unmatched_services)}"

        if not response_data:
            return jsonify({"message": "No matching services found based on the AI response"}), 200

        return jsonify(response_message)

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
