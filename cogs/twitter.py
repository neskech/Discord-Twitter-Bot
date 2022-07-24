import discord
from discord.ext import commands
import tweepy
import requests
from .tCommands import Tweet, TweetWithImage, Reply, ReplyWithImage, QuoteRetweet, QuoteRetweetWithImage
import os

con_key = "" 
con_sec = ""
acc_tok = ""
acc_sec = ""
bearer = ""

##############################################################################################################
##############################################################################################################
####################################### CODE #################################################################
##############################################################################################################
##############################################################################################################
def validate_user(ctx):
    return ctx.message.author.id == 559440854578626565 

def write_img(url):
    idx = url.find('attachments/')
    length = len('attachments/')

    u = url[ idx + length: url.find( '/',  idx + length, len(url) ) ] 
    filename = f'./img/{u}.jpg' #unique image name 
    request = requests.get(url, stream=True) #request the url
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    else:
        return (False, filename)
    return (True, filename)
      
class Twitter(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.init_tweepy()
    self.commands = []

  def init_tweepy(self):
    auth = tweepy.OAuthHandler(con_key, con_sec) # authenticate 
    auth.set_access_token(acc_tok, acc_sec) # grant access 
    self.api = tweepy.API(auth, wait_on_rate_limit=True) # connect to API
    #self.api = tweepy.Client(
    #  bearer_token=bearer, 
    #  consumer_key=con_key, 
    #  consumer_secret=con_sec, 
    #  access_token=acc_tok, 
    #  access_token_secret=acc_sec, 
    #  wait_on_rate_limit = True
    #)

    try:
      self.api.verify_credentials()
      print("Authentication passed")
    except:
      print("Error during authentication")

  @commands.Cog.listener()
  async def on_ready(self):
    print("Bot started!")
    
  @commands.command(name='tweet')
  async def tweet(self, ctx, *args):
    content = ' '.join([word for word in args])
    self.commands.append(Tweet(content))
    await ctx.send("❤️")

  @commands.command(name='reply')
  async def reply(self, ctx, url, *args):
    content = ' '.join([word for word in args])
    self.commands.append(Reply(content, url))
    await ctx.send("❤️")

  @commands.command(name='quote')
  async def quote_retweet(self, ctx, url, *args):
    content = ' '.join([word for word in args])
    self.commands.append(QuoteRetweet(content, url))
    await ctx.send("❤️")

  @commands.command(name='friend')
  async def friend(self, ctx, *args):
    user = ' '.join([word for word in args])
    self.api.create_friendship(user)
    await ctx.send(f"Friendship Time! {user.url}")

  @commands.command(name='tweetImg')
  async def tweet_img(self, ctx, img_url, *args):
    message = ' '.join([word for word in args])

    (success, file_name) = write_img(img_url)
    if success:
        self.commands.append(TweetWithImage(message, file_name, img_url))
        await ctx.send("❤️")
    else:
        await ctx.send("Unable to retrieve image 😈")

  @commands.command(name='replyImg')
  async def reply_img(self, ctx, reply_url, img_url, *args):
    message = ' '.join([word for word in args])

    (success, file_name) = write_img(img_url)
    if success:
        self.commands.append(ReplyWithImage(message, reply_url, file_name, img_url))
        await ctx.send("❤️")
    else:
        await ctx.send("Unable to retrieve image 😈")

  @commands.command(name='quoteImg')
  async def quote_retweet_img(self, ctx, quote_url, img_url, *args):
    message = ' '.join([word for word in args])

    (success, file_name) = write_img(img_url)
    if success:
        self.commands.append(QuoteRetweetWithImage(message, quote_url, file_name, img_url))
        await ctx.send("❤️")
    else:
        await ctx.send("Unable to retrieve image 😈")

  @commands.command(name='popC')
  @commands.check(validate_user)
  async def pop_command(self, ctx, verbose: bool = True):
    if len(self.commands) > 0:
      command = self.commands[0]
      self.commands = self.commands[1:]
      await ctx.send(f"popped command -> {command.__str__(verbose)}")
      return

    await ctx.send('No more commands to pop 😈')

  @commands.command(name='execC')
  @commands.check(validate_user)
  async def exec_command(self, ctx, verbose: bool = True):
    if len(self.commands) > 0:
      command = self.commands[0]
      self.commands = self.commands[1:]
      result = command.execute(self.api)
      string = f'```executed command -> {command.__str__(1)}```\n{result}' if verbose else f'{result}'
      await ctx.send(string)
      return

    await ctx.send('No more commands to execute 😈')

  @commands.command(name='listC')
  @commands.check(validate_user)
  async def list_commands(self, ctx, verbose: bool = True):
    if len(self.commands) > 0:
      string = ''
      for command in self.commands:
        string += command.__str__(verbose) + '\n'
      await ctx.send(f"```{string}```")
      
    await ctx.send('No more commands to display 😈')

  @commands.command(name='Meth')
  @commands.check(validate_user)
  async def help(self, ctx):
    
    await ctx.send(
      """
      ```
      tweet: (Message) 😉
      tweetImg: (Image url, Message) 😋
      reply: (Tweet url, Message) 👅
      replyImg: (Tweet url, Image url, Message) 🍆
      quote: (Tweet url, Message) 💦
      quoteImg: (Tweet url, Image url, Message) 👍  
      ```
      """)
    
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    await ctx.send("https://cdn.discordapp.com/attachments/612361044110868480/1000656940847878144/IMG_0945.jpg")
    
