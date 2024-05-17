from flask import Blueprint, session, request, redirect, url_for
import requests
import os
import time

auth = Blueprint('auth', __name__)

# Login route
@auth.route('/zoho')
def login_with_zoho():
    print(f'in login with zoho route')
    return redirect(f'https://accounts.zoho.com/oauth/v2/auth?scope=Aaaserver.profile.Read&client_id={os.environ.get('ZOHO_CLIENT_ID')}&response_type=code&access_type=offline&redirect_uri={os.environ.get('ZOHO_REDIRECT_URI')}')

# Callback route
@auth.route('/zoho/callback')
def zoho_callback():
    code = request.args.get('code')
    data = {
        'code': code,
        'redirect_uri': os.environ.get('ZOHO_REDIRECT_URI'),
        'client_id': os.environ.get('ZOHO_CLIENT_ID'),
        'client_secret': os.environ.get('ZOHO_CLIENT_SECRET'),
        'grant_type': 'authorization_code'
    }
    r = requests.post('https://accounts.zoho.com/oauth/v2/token', data=data)
    json_data = r.json()
    session['access_token'] = json_data.get('access_token')
    return redirect(url_for('index'))