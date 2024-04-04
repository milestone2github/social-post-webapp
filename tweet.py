import tweepy

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
      print(f"Error occured while uploading image on twitter: {e}")
          
  # Make tweet with an image
  try:
    # Upload image
    media = upload_image(image_path)

    # Post tweet with image
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
    print("Tweeted with image: {}".format(response.data['text']))
  except Exception as e:
    print(f"An error occurred while tweeting: {e}")


# function to tweet only text 
def post_tweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, tweet_text) :
  # Create client object from twitter API v2  
  client = tweepy.Client(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRET)
  try:
    print(f"Tweeting: {tweet_text}")
    response = client.create_tweet(text= tweet_text)
    print(f"https://twitter.com/user/status/{response.data['id']}")
    print("Tweeted text successfully.")
  except Exception as e:
    print(f"An error occurred while tweeting: {e}")