import discord
import os
import time
import asyncio
import random

intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

HELP_COMMAND = "help"
INVOCATION_PREFIX = "!"
CHANNEL_NAME = "Random Speak "
INIT_COMMAND="init"


@client.event
async def on_ready():
  '''Called when client is ready. Prints the bot's current user.'''
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name=" use !help to see the commands!"))

@client.event
async def on_message(message):
  """Called whenever a message is sent. Handles commands.

  Parameters: a Message object"""
  if message.author == client.user:
      return

  if len(message.content) == 0:
      return

  if message.content[0] != INVOCATION_PREFIX:
      return


  command = parseCommand(message)
  call = command[0] #call is the first command i.e join, create, leave, help
  print(call)
  if call == HELP_COMMAND: #help command
        await dissapMessage(message,doHelp())
  if call == INIT_COMMAND:
    channelCategory = await doInit(message)
    await message.delete()
    await doMainLoop(message,channelCategory)
  await message.delete()

async def doInit(message):
    channelCategory = discord.utils.get(message.guild.categories,name="Dynamic Voice")
    if channelCategory == None:
        channelCategory = await message.guild.create_category(name="Dynamic Voice")
    for channel in channelCategory.voice_channels:
        await channel.delete()
    return channelCategory

async def doMainLoop(message,channelCategory):
    number=0
    while True:
        toDelete = []
        await asyncio.sleep(0.1)
        print("list" + str(channelCategory.voice_channels))
        index=0
        for channel in (channelCategory.voice_channels):
            if len(channel.members) == 0:
                print("addeddddd")
                toDelete.append(channel)
            if channel.name != (CHANNEL_NAME + str(index+1)):
                await channel.edit(name=(CHANNEL_NAME + str(index+1)))
            index +=1
        print(toDelete)
        if len(toDelete)==0:
            print("adding channel")
            number+=1
            await channelCategory.create_voice_channel(name=(CHANNEL_NAME + str(number)))

        for channel in toDelete:
            print(number)
            if channel.name != (CHANNEL_NAME + str(number)):
                await channel.delete()
                toDelete.remove(channel)
                number-=1
            else:
                print("channel maintained")





def parseCommand(message):
  """Parses the command into a list of Strings.

  Returns: A list of Strings"""
  #splits the message into a list of strings and discards the INVOCATION_PREFIX
  command = message.content[1:].split(" ")
  command[0].lower
  return command

def doHelp():
  """Constructs the help String.

  Returns: A String"""

  #constructs the string starting with a quote prifx
  outString = ">>> "
  #create command
  outString += "**" + INVOCATION_PREFIX + CREATE_COMMAND + "**" + " *[team_name]* will create a team, with name team_name, and assign the user to that team \n"
  #join command
  outString += "**" + INVOCATION_PREFIX + JOIN_COMMAND + "**" + " *[team_name]* will assign the user to the team \n"
  #leave command
  outString += "**" + INVOCATION_PREFIX + LEAVE_COMMAND + "**" + " *[team_name]* will deassign the user from the team \n"
  #del command
  outString += "**" + INVOCATION_PREFIX + DELETE_COMMAND + "**" + " *[team_name]* will **PERMANENTLY** delete the team and all channels associated. \n"
  #returns the created string
  outString += "**" + INVOCATION_PREFIX + PING_COMMAND + "**" + " can check whether the bot is active \n"

  outString += "**" + INVOCATION_PREFIX + RAND_COMMAND + "**" + " *[max_number]* will get a random number between 1 and max_number, inclusive. (default 20)\n"

  outString += "**" + INVOCATION_PREFIX + CAT_COMMAND + "**" + " 🐈 \n"
  return outString



async def dissapMessage(message,output):
  sent = await message.channel.send(output)
  await asyncio.sleep(10)
  await sent.delete()
#runs the client
client.run(os.getenv("TOKEN"))
