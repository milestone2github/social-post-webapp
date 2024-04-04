from flask import Flask, request, jsonify, render_template
import os
from post_to_fb import post_image_to_facebook_page, post_text_to_facebook_page
from tweet import post_tweet_with_image, post_tweet
from dotenv import load_dotenv

# SECRETS 
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

app = Flask(__name__)

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
    return jsonify({'message': 'No file part in the request'}), 400
  file = request.files['file']

  # If the user does not select a file, the browser submits an
  # empty file without a filename.
  if file.filename == '':
    return jsonify({'message': 'No selected file'}), 400

  if file and allowed_file(file.filename):
    # Save the file with post_image.png name
    fixed_filename = 'post_image.png'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], fixed_filename)
    file.save(image_path)
  else:
    return jsonify({'message': 'Invalid file type or size'}), 400

  text = request.form.get('text', '')
  print(f'Received text: {text}')

  # post image to facebook page 
  post_image_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, image_path, text)
  

  # tweet on twitter
  post_tweet_with_image(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, image_path, text)

  return jsonify({'message': 'File successfully uploaded'}), 200


# route to post text only 
@app.route('/text', methods=['POST'])
def upload_text():
  text = request.form.get('text', '')
  if len(text) < 3 :
    return jsonify({'message': 'The minimum length of the text must be 3'})
  
  print(f'Received text in text endpoint: {text}')

  # post text to facebook page
  post_text_to_facebook_page(FB_ACCESS_TOKEN, FB_PAGE_ID, text)

  # tweet on twitter
  post_tweet(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, text)
  return jsonify({'message': 'Text uploaded successfully'}), 200

if __name__ == '__main__':
  os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
  app.run(debug=True)
