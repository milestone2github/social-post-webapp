import tweepy
import logging

# function to tweet text with image 
def post_tweet_with_image(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, image_path, tweet_text) :

  # Authenticate to Twitter
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

  # Create client object from twitter API v2  
  client = tweepy.Client(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRET)

  # Create API object from twitter API v1 
  api = tweepy.API(auth)

  # function to upload media 
  def upload_image(image):
    try:
      media = api.media_upload(filename= image)
      return media
    except Exception as e:
      logging.error(f'Error occured while uploading image on twitter: {e}')
          
  # Make tweet with an image
  try:
    # Upload image
    media = upload_image(image_path)

    # Post tweet with image
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
    logging.info("Tweeted with image: %s", response.data['text'])

  except Exception as e:
    logging.error(f'An error occurred while tweeting: {e}')


# function to tweet only text 
def post_tweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, tweet_text) :
  # Create client object from twitter API v2  
  client = tweepy.Client(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRET)
  try:
    logging.info(f"Tweeting: {tweet_text}")
    response = client.create_tweet(text= tweet_text)
    logging.info(f"https://twitter.com/user/status/{response.data['id']}")
    logging.info("Tweeted text successfully.")
  except Exception as e:
    logging.error(f"An error occurred while tweeting: {e}")