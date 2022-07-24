# Twitter Bot

A discord bot designed to be hosted on replit. Utilizes the tweepy api to allow users to create simple tweets for a specific account

- Commands (prefaced by !)
  -
      - tweet: (Message) 
      - tweetImg: (Image url, Message) 
      - reply: (Tweet url, Message) 
      - replyImg: (Tweet url, Image url, Message) 
      - quote: (Tweet url, Message) 
      - quoteImg: (Tweet url, Image url, Message) 
      
 #Safety
 
 The bot contains a safety system to allow a specific user validate tweets members create with the bot. This designated user (or an administrator) can    display a list of all of the pending tweets and choose which ones they wish to send out
 
 - Admin Commands
  -
      - listC: (verbose: bool = True) -> List commands. If verbose is false, url's are not printed
      - execC: (verbose: bool = True) -> Executes command at the bottom of the stack. Prints the command just executed and the tweet just created. If verbose is false, the url's contained in the command's to_string() are not printed
      - popC: (verbose: bool = True) -> Pops the command at the bottom of the stack and prints it. 



