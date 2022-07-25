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

##############################################################################################################
##############################################################################################################
####################################### CODE #################################################################
##############################################################################################################
##############################################################################################################
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
    
    self.safety = True
    self.print_errors = True
    self.verbose = True

  def init_tweepy(self):
    auth = tweepy.OAuthHandler(con_key, con_sec) # authenticate 
    auth.set_access_token(acc_tok, acc_sec) # grant access 
    self.api = tweepy.API(auth, wait_on_rate_limit=True) # connect to API

    try:
      self.api.verify_credentials()
      print("Authentication passed")
    except:
      print("Error during authentication")

  @commands.Cog.listener()
  async def on_ready(self):
    print("Bot started!")

  async def execute_command_(self, ctx):
    if len(self.commands) > 0: 
      command = self.commands[0]
      self.commands = self.commands[1:]
      result = command.execute(self.api)
      await ctx.send(f'```executed command -> {command.__str__(1)}```\n{result}' if self.verbose else f'{result}')
      return
      
    await ctx.send('No more commands to execute 😈')

##############################################################################################################
##############################################################################################################
####################################### TWEET COMMANDS #######################################################
##############################################################################################################
##############################################################################################################
    
  @commands.command(name='tweet')
  async def tweet(self, ctx, *args):
    content = ' '.join([word for word in args])
    self.commands.append(Tweet(content))

    if self.safety:
      await ctx.send("❤️")
    else:
      await self.execute_command_(ctx)

  @commands.command(name='reply')
  async def reply(self, ctx, url, *args):
    content = ' '.join([word for word in args])
    self.commands.append(Reply(content, url))
    
    if self.safety:
      await ctx.send("❤️")
    else:
      await self.execute_command_(ctx)

  @commands.command(name='quote')
  async def quote_retweet(self, ctx, url, *args):
    content = ' '.join([word for word in args])
    self.commands.append(QuoteRetweet(content, url))

    if self.safety:
      await ctx.send("❤️")
    else:
      await self.execute_command_(ctx)

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

        if self.safety:
          await ctx.send("❤️")
        else:
          await self.execute_command_(ctx)
    else:
        await ctx.send("Unable to retrieve image 😈")

  @commands.command(name='replyImg')
  async def reply_img(self, ctx, reply_url, img_url, *args):
    message = ' '.join([word for word in args])

    (success, file_name) = write_img(img_url)
    if success:
        self.commands.append(ReplyWithImage(message, reply_url, file_name, img_url))
      
        if self.safety:
          await ctx.send("❤️")
        else:
          await self.execute_command_(ctx)
    else:
        await ctx.send("Unable to retrieve image 😈")

  @commands.command(name='quoteImg')
  async def quote_retweet_img(self, ctx, quote_url, img_url, *args):
    message = ' '.join([word for word in args])

    (success, file_name) = write_img(img_url)
    if success:
        self.commands.append(QuoteRetweetWithImage(message, quote_url, file_name, img_url))
      
        if self.safety:
          await ctx.send("❤️")
        else:
          await self.execute_command_(ctx)
    else:
        await ctx.send("Unable to retrieve image 😈")

##############################################################################################################
##############################################################################################################
####################################### ADMIN COMMANDS #######################################################
##############################################################################################################
##############################################################################################################
      
  @commands.command(name='popC')
  @commands.has_permissions(administrator=True)
  async def pop_command(self, ctx):
    if len(self.commands) > 0:
      command = self.commands[0]
      self.commands = self.commands[1:]
      await ctx.send(f"popped command -> {command.__str__(verbose)}")
      return

    await ctx.send('No more commands to pop 😈')

  @commands.command(name='execC')
  @commands.has_permissions(administrator=True)
  async def exec_command(self, ctx):
    await self.execute_command_(ctx)

  @commands.command(name='listC')
  @commands.has_permissions(administrator=True)
  async def list_commands(self, ctx):
    if len(self.commands) > 0:
      string = ''
      for command in self.commands:
        string += command.__str__(self.verbose) + '\n'
      await ctx.send(f"```{string}```")
      return
      
    await ctx.send('No more commands to display 😈')

##############################################################################################################
##############################################################################################################
####################################### ADMIN UTILITY ########################################################
##############################################################################################################
##############################################################################################################
    
  @commands.command(name="enableErrors")
  @commands.has_permissions(administrator=True)
  async def enable_error(self, ctx):
    self.print_errors = True
    await ctx.send("Errors reports enabled")

  @commands.command(name="disableErrors")
  @commands.has_permissions(administrator=True)
  async def disable_error(self, ctx):
    self.print_errors = False
    await ctx.send("Errors reports disabled")

  @commands.command(name="enableSafety")
  @commands.has_permissions(administrator=True)
  async def enable_safety(self, ctx):
    self.safety = True
    await ctx.send("Safety Enabled")

  @commands.command(name="disableSafety")
  @commands.has_permissions(administrator=True)
  async def disable_safety(self, ctx):
    self.safety = False
    await ctx.send("Safety Disabled")
    
  @commands.command(name="enableVerbose")
  @commands.has_permissions(administrator=True)
  async def enable_verbosity(self, ctx):
    self.verbose = True
    await ctx.send("Verbose enabled")

  @commands.command(name="disableVerbose")
  @commands.has_permissions(administrator=True)
  async def disable_verbosity(self, ctx):
    self.verbose = False
    await ctx.send("Verbose disabled")

  @commands.command(name='twitterBotHelp')
  async def help(self, ctx):
    
    await ctx.send(
      """
      ```
      tweet: (Message) 
      tweetImg: (Image url, Message) 
      reply: (Tweet url, Message) 
      replyImg: (Tweet url, Image url, Message) 
      quote: (Tweet url, Message) 
      quoteImg: (Tweet url, Image url, Message)   
      ```
      """)

##############################################################################################################
##############################################################################################################
####################################### END ##################################################################
##############################################################################################################
##############################################################################################################
    
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if self.print_errors:
      await ctx.send("https://cdn.discordapp.com/attachments/612361044110868480/1000656940847878144/IMG_0945.jpg")
    
