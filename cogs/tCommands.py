import os 

class Command:
  def __init__(self):
    pass

  def __str__(self, verbose: bool):
    pass
    
  def execute(self, api) -> str:
    ""

##############################################################################################################
##############################################################################################################
####################################### COMMANDS #############################################################
##############################################################################################################
##############################################################################################################

class Tweet(Command):
  def __init__(self, message):
    super().__init__()
    self.message = message

  def __str__(self, verbose: bool):
    return f"Type: Tweet | Message: \"{self.message}\""
    
  def execute(self, api):
    status = api.update_status(self.message)
    return f'https://twitter.com/twitter/statuses/{status.id}'

class TweetWithImage(Command):
  def __init__(self, message, image_file, image_url):
     super().__init__()
     self.message = message
     self.image_file = image_file
     self.image_url = image_url

  def __str__(self, verbose: bool):
    im_ur = '...' if not verbose else self.image_url
    return f"Type: Tweet With Image | Message: \"{self.message}\" | Image: {im_ur}"
     
  def execute(self, api) -> str:
    media = api.media_upload(self.image_file)
    tweet = api.update_status(self.message, media_ids = [media.media_id])
    os.remove(self.image_file)
    return f'https://twitter.com/twitter/statuses/{tweet.id}'

class Reply(Command):
  def __init__(self, message, url):
    self.message = message
    self.reply_url = url

  def __str__(self, verbose: bool):
    rp_ur = '...' if not verbose else self.reply_url
    return f"Type: Reply | Message: \"{self.message}\" | Original Tweet: {rp_ur}"
    
  def execute(self, api):
    tweetid = self.reply_url[self.reply_url.find('status/') + len('status/'):]
    status = api.update_status(status=self.message, in_reply_to_tweet_id = tweetid, auto_populate_reply_metadata=True)
    return f'https://twitter.com/twitter/statuses/{status.id}'

class ReplyWithImage(Command):
  def __init__(self, message, reply_url, image_file, image_url):
    self.message = message
    self.reply_url = reply_url
    self.image_file = image_file
    self.image_url = image_url

  def __str__(self, verbose: bool):
    rp_ur = '...' if not verbose else self.reply_url
    img_ur = '...' if not verbose else self.image_url
    return f"Type: Reply With Image | Message: \"{self.message}\" | Original Tweet: {rp_ur} | Image: {img_ur}"
    
  def execute(self, api):
    tweetid = self.reply_url[self.reply_url.find('status/') + len('status/'):]
    media = api.media_upload(self.image_file)
    status = api.update_status(status=self.message, in_reply_to_tweet_id = tweetid, media_ids = [media.media_id], auto_populate_reply_metadata=True)
    os.remove(self.image_file)
    return f'https://twitter.com/twitter/statuses/{status.id}'

class QuoteRetweet(Command):
  def __init__(self, message, quote_url):
    self.message = message
    self.quote_url = quote_url

  def __str__(self, verbose: bool):
    qu_ur = '...' if not verbose else self.quote_url
    return f"Type: Quote Retweet | Message: \"{self.message}\" | Original Tweet: {qu_ur}"
    
  def execute(self, api):
    status = api.update_status(self.message, attachment_url=self.quote_url)
    return f'https://twitter.com/twitter/statuses/{status.id}'

class QuoteRetweetWithImage(Command):
  def __init__(self, message, quote_url, image_file, image_url):
    self.message = message
    self.quote_url = quote_url
    self.image_file = image_file
    self.image_url = image_url

  def __str__(self, verbose: bool):
    qu_ur = '...' if not verbose else self.quote_url
    img_ur = '...' if not verbose else self.image_url
    return f"Type: Quote Retweet With Image | Message: \"{self.message}\" | Original Tweet: {qu_ur} | Image: {img_ur}"
    
  def execute(self, api):
    media = api.media_upload(self.image_file)
    status = api.update_status(status=self.message, attachment_url=self.quote_url, media_ids = [media.media_id])
    os.remove(self.image_file)
    return f'https://twitter.com/twitter/statuses/{status.id}'