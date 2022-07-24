import discord
from discord.ext import commands
from cogs import twitter
import os

client = commands.Bot(intents = discord.Intents.all(), command_prefix='!')

##############################################################################################################
##############################################################################################################
####################################### LOAD COGS ############################################################
##############################################################################################################
##############################################################################################################

client.add_cog(twitter.Twitter(client))
client.run(os.environ['TOKEN'])
