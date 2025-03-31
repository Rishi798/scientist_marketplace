import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '629059fa5288ee02e6dc0c0cf6adcee1')  # Defaulting to your provided key
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://rishi@localhost/ecommerce')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event system to save resources
