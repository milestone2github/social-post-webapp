from functools import wraps
from flask import jsonify, request, session, redirect, url_for
import os
import requests

X_API_KEY = os.environ.get('X_API_KEY')

def verify_zoho_access_token(access_token):
    url = 'https://accounts.zoho.com/oauth/user/info'
    headers = {
        'Authorization': f'Zoho-oauthtoken {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200


# Authentication Middleware 
def require_app_key(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if request.headers.get('x-api-key') != X_API_KEY:
      return jsonify({'message': 'Unauthorized'}), 403
    return f(*args, **kwargs)
  return decorated_function

def require_zoho_login(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    access_token = session.get('access_token')
    if not access_token:
      return jsonify({'message': 'Unauthorized'}), 403
    elif access_token and not verify_zoho_access_token(access_token):
      session.pop('access_token')
      return jsonify({'message': 'Unauthorized'}), 403
    return f(*args, **kwargs)
  return decorated_function

def require_login(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    print(f'in require_login')
    access_token = session.get('access_token')
    if not access_token:
      return redirect(url_for('login'))
    elif access_token and not verify_zoho_access_token(access_token):
      session.pop('access_token')
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated_function