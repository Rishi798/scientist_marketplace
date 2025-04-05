# Scientist Marketplace

## Overview
The Scientist Marketplace is a web application designed to facilitate the connection between scientists, researchers, and suppliers. It provides a platform for scientists to search for and discover research services and products based on their specific needs. The platform leverages AI-powered recommendations using the DeepSeek AI model to suggest the most relevant scientific services.

## Features
- User and Supplier Management
- AI-Powered Service Recommendations
- Service Listing and Detailed View
- Request Submission for Services
- Google Sign-In for Suppliers
- Interactive AI Chatbot for Research Assistance

## AI-Powered Recommendations
The AI chatbot in the Scientist Marketplace is powered by the **DeepSeek R1 Distill Llama 70B** model. The AI assists researchers by:
- Understanding research queries
- Providing intelligent recommendations based on available services
- Offering insights and solutions related to scientific research

## Installation
### Prerequisites
- Python 3.9+
- Flask
- PostgreSQL
- Groq API Key (for AI model integration)

### Clone the repository:
```
git clone https://github.com/yourusername/scientist_marketplace.git
cd scientist_marketplace
```

### Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### Install dependencies:
```
pip install -r requirements.txt
```

### Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_postgres_url
FLASK_APP=run.py
FLASK_ENV=development
```

### Run Database Migrations:
```
flask db upgrade
```

### Run the application:
```
flask run
```

## Usage
### Access the Platform
Visit the application at: `http://127.0.0.1:5000/`

### User Actions
- Search for services using keywords.
- Use the AI chatbot to get recommendations for research services.
- View detailed service information.
- Submit service requests to suppliers.

### Supplier Actions
- Register or log in using Google Sign-In.
- Add and manage research services.
- View and respond to user service requests.

## Database Schema
The application uses a PostgreSQL database with the following primary models:
- User
- Supplier
- Product
- Service
- Service Request
- Service Response
- ChatLog

## Testing
Use Postman to test API endpoints:
- Service Listing: `GET /services`
- AI Service Recommendation: `POST /ai_search`
- Submit a Service Request: `POST /services/<service_id>/request`

## Deployment
The application can be deployed on platforms like Heroku or AWS. Ensure to set the appropriate environment variables and configure the database.

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-branch`
5. Submit a pull request.



## Contact
For any issues or feature requests, please contact the project maintainer: rishinashikkar10@gmail.com

