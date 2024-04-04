import requests

# Example usage
ZOHO_REFRESH_TOKEN = '1000.cfcf7c16f88e59fbe2b28c88d1911677.bc7e13d00dab098b3591d6280378151d'
ZOHO_CLIENT_ID = '1000.Q7WP7HFCH3UYVB5U2ABQZS15464WBQ'
ZOHO_CLIENT_SECRET = '2cc94720d110d45956760dbe5d297858469b2ba8a4'

ZOHO_ACCESS_TOKEN = '1000.695fd60d9682e7a78a6d963027624353.a318af0f6e7e2f01644dd5736581feb3'

def get_access_token(refresh_token, client_id, client_secret):
    try:
        TOKEN_ENDPOINT = "https://accounts.zoho.com/oauth/v2/token"
        payload = {
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
        }
        response = requests.post(TOKEN_ENDPOINT, data=payload)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return access_token
        else:
            # Optionally, log the error or handle it according to your application's requirements
            response.raise_for_status()  # This will raise an HTTPError if the request returned an error code
    except requests.exceptions.RequestException as e:
        # Handle different exceptions, e.g., connection errors, timeout, etc.
        # Optionally, send an email with the error details or log the error
        print(f"Failed to refresh access token: {e}")
        # send_summary_email(e)  # Make sure this function is defined to handle sending emails
        return None

access_token = get_access_token(ZOHO_REFRESH_TOKEN, ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET)
if access_token:
    print("Access Token:", access_token)
else:
    print("Failed to obtain access token.")
