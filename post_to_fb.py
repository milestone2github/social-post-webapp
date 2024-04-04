import requests
import logging

def post_image_to_facebook_page(access_token, page_id, image_path, message):
  """
  Post an image to a Facebook page.

  :param access_token: Page Access Token
  :param page_id: Facebook Page ID
  :param image_path: Path to the image file
  :param message: Message to post along with the image
  """
  graph_api_url = f'https://graph.facebook.com/v18.0/{page_id}/photos'
  payload = {
    'message': message,
    'access_token': access_token
  }
  files = {
    'source': open(image_path, 'rb')
  }

  try:
    response = requests.post(graph_api_url, data=payload, files=files)
    if response.ok:
      print('Post on facebook successfully')
      return response.json()
    json_res = response.json()
    logging.error('Unable to post on facebook: ', json_res['error']['message'])
    return
  except Exception as e:
    logging.error(f"Error in posting to facebook: {e}")

def post_text_to_facebook_page(access_token, page_id, message):
  """
  Post text to a Facebook page.

  :param access_token: Page Access Token
  :param page_id: Facebook Page ID
  :param message: Message to post
  """
  graph_api_url = f'https://graph.facebook.com/v18.0/{page_id}/feed'
  payload = {
    'message': message,
    'access_token': access_token
  }

  try:
    response = requests.post(graph_api_url, data=payload)
    if response.ok:
      print('Post text on facebook successfully')
      return response.json()
    json_res = response.json()
    logging.error('Unable to post on facebook: ', json_res['error']['message'])
    return
  except Exception as e:
    logging.error(f"Error in posting to facebook: {e}")
