# Twitter Bot

A discord bot designed to be hosted on replit. Utilizes the tweepy api to allow users to create simple tweets for a specific account

*Note, this project uses V 1.1 of the twitter api via tweepy. In order to use this, you'll need to apply for 'elevated' access on twitter's developer portal. V 1.1 is required to tweet images, which is why I'm using it* 

- Commands (prefaced by !)
  -
      - tweet: (Message) 
      - tweetImg: (Image url, Message) 
      - reply: (Tweet url, Message) 
      - replyImg: (Tweet url, Image url, Message) 
      - quote: (Tweet url, Message) 
      - quoteImg: (Tweet url, Image url, Message) 
      
 # Safety
 
 This bot contains a safety system which allows admins to validate tweets before they're sent out. The bot keeps a queue of all the proccessed commands from which admins can pick and choose to send out
 
- Admin Commands
  -
      - listC:  List commands in the queue
      - execC: Executes command at the start of the queue. Prints the created tweet 
      - popC:  Pops the command at the start of the queue

 # Utility

- Admin Utility Commands
  -
      - enableSafety: Enables the safety system (on by default)
      - disableSafety: Disables the safety system. Tweets are immediately sent out after a user requests one
      - enableVerbose: Enables verbosity. When verbose is true, commands to_strings() will print url's (on by default)
      - disableVerbose: Disables verbosity
      - enableErrors: Enables error info printing when an error occurs (on by default)
      - disableErrors: Disables error printing
      - twitterBotHelp: (can be used by anyone). Prints tweet command information

# Errors

 -Upon receiving an error, a high quality image of Saul Goodman from Breaking Bad™ will be printed
 
 ![](./img/Saul.jpg)
 
 *Some things to note: Making duplicate tweets will result in errors*
