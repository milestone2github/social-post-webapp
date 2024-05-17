# app/auth/__init__.py
from flask import Blueprint

# Create a Blueprint for the auth module
auth = Blueprint('auth', __name__)

from . import routes