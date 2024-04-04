from flask import Flask, request, jsonify, render_template
import os
from post_to_fb import post_image_to_facebook_page, post_text_to_facebook_page
from tweet import post_tweet_with_image, post_tweet
from post_to_linkedIn import post_on_linkedin
from dotenv import load_dotenv
import logging

# SECRETS 
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
LINKEDIN_ACCESS_TOKEN = os.environ.get('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_ORG_ID = os.environ.get('LINKEDIN_ORG_ID')

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

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# index route 
@app.route('/')
def index():
  return render_template('form.html')

# route to post image 
@app.route('/image', methods=['POST'])
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

  text = request.form.get('text', '')
  print(f'Received text: {text}')

  # post image to facebook page 
  post_image_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, image_path, text)
  

  # tweet on twitter
  post_tweet_with_image(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, image_path, text)

  # post on linkedIn
  post_on_linkedin(LINKEDIN_ACCESS_TOKEN, LINKEDIN_ORG_ID, text, image_path)

  return jsonify({'message': 'File successfully uploaded'}), 200


# route to post text only 
@app.route('/text', methods=['POST'])
def upload_text():
  text = request.form.get('text', '')
  if len(text) < 3 :
    logging.error('Text length less than 3')
    return jsonify({'message': 'The minimum length of the text must be 3'})
  
  logging.info(f'Received text in text endpoint: {text}')

  # post text to facebook page
  post_text_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, text)

  # tweet on twitter
  post_tweet(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, text)

  # post on linkedIn
  post_on_linkedin(LINKEDIN_ACCESS_TOKEN, LINKEDIN_ORG_ID, text)

  return jsonify({'message': 'Text uploaded successfully'}), 200

if __name__ == '__main__':
  os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
  app.run(debug=True)
