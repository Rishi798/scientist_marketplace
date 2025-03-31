from flask import Blueprint, render_template

# Define the user blueprint
user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def user_home():
    return render_template("user/home.html")

