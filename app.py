from flask import Flask, request, jsonify, render_template
import os
from post_to_fb import post_image_to_facebook_page, post_text_to_facebook_page
from tweet import post_tweet_with_image, post_tweet
from post_to_linkedIn import post_on_linkedin
from dotenv import load_dotenv
import logging
from functools import wraps

FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
LINKEDIN_ACCESS_TOKEN = os.environ.get('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_ORG_ID = os.environ.get('LINKEDIN_ORG_ID')
X_API_KEY = os.environ.get('X_API_KEY')
PLANVESTS_FB_ACCESS_TOKEN = os.environ.get('PLANVESTS_FB_ACCESS_TOKEN')
PLANVESTS_FB_PAGE_ID = os.environ.get('PLANVESTS_FB_PAGE_ID')
PLANVESTS_TWITTER_CONSUMER_KEY = os.environ.get('PLANVESTS_TWITTER_CONSUMER_KEY')
PLANVESTS_TWITTER_CONSUMER_SECRET = os.environ.get('PLANVESTS_TWITTER_CONSUMER_SECRET')
PLANVESTS_TWITTER_ACCESS_TOKEN = os.environ.get('PLANVESTS_TWITTER_ACCESS_TOKEN')
PLANVESTS_TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('PLANVESTS_TWITTER_ACCESS_TOKEN_SECRET')
PLANVESTS_LINKEDIN_ACCESS_TOKEN = os.environ.get('PLANVESTS_LINKEDIN_ACCESS_TOKEN')
PLANVESTS_LINKEDIN_ORG_ID = os.environ.get('PLANVESTS_LINKEDIN_ORG_ID')
app = Flask(__name__)

LOG_FILE = "app.log"

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the logging level

# Create a file handler for writing logs to a file
file_handler = logging.FileHandler(LOG_FILE)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
file_handler.setFormatter(file_formatter)

# Create a console handler for printing logs to the console
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 1MB max-limit.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Authentication Middleware 
def require_app_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') != X_API_KEY:
            return jsonify({'message': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    return decorated_function

# index route 
@app.route('/')
def index():
  return render_template('form.html')

# route to post image 
@app.route('/image', methods=['POST'])
@require_app_key
def upload_file():
  # Check if the post request has the file part
  if 'file' not in request.files:
    logging.error('No file part in the request')
    return jsonify({'message': 'No file part in the request'}), 400
  file = request.files['file']

  # If the user does not select a file, the browser submits an
  # empty file without a filename.
  if file.filename == '':
    logging.error('No selected file')
    return jsonify({'message': 'No selected file'}), 400

  if file and allowed_file(file.filename):
    # Save the file with post_image.png name
    fixed_filename = 'post_image.png'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], fixed_filename)
    file.save(image_path)
    logging.info('File saved successfully')

  else:
    logging.error('Invalid file type or size')
    return jsonify({'message': 'Invalid file type or size'}), 400

  fb_text = request.form.get('fb_text', '')
  twitter_text = request.form.get('twitter_text', '')
  linkedin_text = request.form.get('linkedin_text', '')
  print(f'Received text: {fb_text}')
  print(f'Received text: {twitter_text}')
  print(f'Received text: {linkedin_text}')

  # post image to facebook page 
  post_image_to_facebook_page(PLANVESTS_FB_ACCESS_TOKEN, PLANVESTS_FB_PAGE_ID, image_path, fb_text)
  post_image_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, image_path, fb_text)
  

  # tweet on twitter
  post_tweet_with_image(PLANVESTS_TWITTER_CONSUMER_KEY, PLANVESTS_TWITTER_CONSUMER_SECRET, PLANVESTS_TWITTER_ACCESS_TOKEN, PLANVESTS_TWITTER_ACCESS_TOKEN_SECRET, image_path, twitter_text)
  post_tweet_with_image(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, image_path, twitter_text)

  # post on linkedIn
  post_on_linkedin(PLANVESTS_LINKEDIN_ACCESS_TOKEN, PLANVESTS_LINKEDIN_ORG_ID, linkedin_text, image_path)
  post_on_linkedin(LINKEDIN_ACCESS_TOKEN, LINKEDIN_ORG_ID, linkedin_text, image_path)

  return jsonify({'message': 'File successfully uploaded'}), 200


# route to post text only 
@app.route('/text', methods=['POST'])
@require_app_key
def upload_fb_text():
    fb_text = request.form.get('fb_text', '')
    twitter_text = request.form.get('twitter_text', '')
    linkedin_text = request.form.get('linkedin_text', '')
    if len(fb_text) < 3:
        logging.error('Text length less than 3')
        return jsonify({'message': 'The minimum length of the text must be 3'}), 400

    # Post text to Facebook page
    post_text_to_facebook_page(PLANVESTS_FB_ACCESS_TOKEN, PLANVESTS_FB_PAGE_ID, fb_text)
    post_text_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, fb_text)
    if len(twitter_text) < 3:
        logging.error('Text length less than 3')
        return jsonify({'message': 'The minimum length of the text must be 3'}), 400

    # Post text to twiter page
    post_tweet(PLANVESTS_TWITTER_CONSUMER_KEY, PLANVESTS_TWITTER_CONSUMER_SECRET, PLANVESTS_TWITTER_ACCESS_TOKEN, PLANVESTS_TWITTER_ACCESS_TOKEN_SECRET, twitter_text)
    post_tweet(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, twitter_text)
    
    if len(linkedin_text) < 3:
        logging.error('Text length less than 3')
        return jsonify({'message': 'The minimum length of the text must be 3'}), 400

  # post on linkedIn
    post_on_linkedin(PLANVESTS_LINKEDIN_ACCESS_TOKEN, PLANVESTS_LINKEDIN_ORG_ID, linkedin_text)
    post_on_linkedin(LINKEDIN_ACCESS_TOKEN, LINKEDIN_ORG_ID, linkedin_text)

    return jsonify({'message': 'Text uploaded successfully to all platform'}), 200

if __name__ == '__main__':
  app.run(debug=True)
