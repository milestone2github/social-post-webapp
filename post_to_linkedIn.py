import logging
import requests

# LINKEDIN FUNCTIONS 
# get the url to upload image on linkedin 
def register_upload(token, organization_id):
    url = 'https://api.linkedin.com/v2/assets?action=registerUpload'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": f"urn:li:organization:{organization_id}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        return response
    except Exception as e:
        logging.error(f"Error registering upload while posting on linkedIn: {e}")

# upload the image to linkedin server 
def upload_image(access_token, upload_url, image_path):
    with open(image_path, 'rb') as image_file:
        headers = {
            'Authorization': f'Bearer {access_token}',  # Replace 'Redacted' with your actual token
            'LinkedIn-Version': '202304',
        }
        try:
            response = requests.put(upload_url, headers=headers, data=image_file)
            return response
        except Exception as e:
            logging.error(f"Error uploading image while posting on linkedIn: {e}")
            
# post the content on linkedin page 
def create_post(token, organization_id, text, image_asset=None):
    url = 'https://api.linkedin.com/v2/shares'

    headers = {
        'Authorization': f'Bearer {token}',
        'LinkedIn-Version': '202304',
        'Content-Type': 'application/json'
    }

    data = {
        "owner": f"urn:li:organization:{organization_id}",
        "text": {
            "text": text  # the title of the post
        },
        "subject": "End of the Day",
        "distribution": {
            "linkedInDistributionTarget": {}
        }
    }

    if image_asset:
        data["content"] = {
            "contentEntities": [
                {
                    "entity": image_asset
                }
            ],
            "title": "End of the Day",
            "shareMediaCategory": "IMAGE"
        }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            logging.info("Posted on LinkedIn")
        return response.json()
    except Exception as e:
        logging.error(f"Error posting on LinkedIn: {e}")

# function to post on linkedIn (it calls above functions)
def post_on_linkedin(access_token, organization_id, text, image_path = None): 
  # if got image path in args then upload image and text both 
  if image_path:
    register_upload_response = register_upload(access_token, organization_id)
    if not register_upload_response.ok:
      return
    
    register_upload_data = register_upload_response.json()
    # Extract the upload URL from the previous response
    upload_url = register_upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    upload_response = upload_image(access_token, upload_url, image_path)
    if not upload_response.ok:
      logging.error("Error uploading image while posting on linkedIn")
      return
    
    # Extract the asset ID from the register upload response
    asset = register_upload_data['value']['asset']

    post_response = create_post(access_token, organization_id, text, asset)

  # post only text 
  else:
    post_response = create_post(access_token, organization_id, text)
    