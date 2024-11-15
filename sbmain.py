from datetime import datetime, timedelta 
import discord
from discord.ext import commands
import json
import asyncio 
from bs4 import BeautifulSoup
import os
from pathlib import Path
import requests
import pyfiglet
import urllib.parse
from urllib.parse import quote
import aiohttp
from ping3 import ping
import GPUtil
import psutil
import random
import string
import re
import httpx
import qrcode
import io
import platform
import subprocess
import platform
from colorama import init, Fore, Style
from googletrans import Translator, LANGUAGES
init()

def cls():
    """clears terminal"""
    if os.name == 'nt':  # Windows terminal clear
        os.system('cls')
    else:  # Linux/macos terminal clear
        os.system('clear')
cls()

translator = Translator()


folder_sb = os.path.dirname(os.path.realpath(__file__)) # checks for config.json within the file path if it is missing creates then reads from the file
json_file = os.path.join(folder_sb, 'config.json')
if os.path.exists(json_file):

    with open(json_file, 'r') as file:
        sb = json.load(file)
else:
    sb = {}

async def tokenchecker(token):
    """checks if discord token is valid"""
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
        "User-Agent": "DiscordBot (https://discord.com, v1)"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return True  
        else:
            return False  

async def GetToken(sb, json_file):
    """Prompts the user for their discord token"""
    TOKEN = sb.get("TOKEN", "").strip()

    while not TOKEN or not await tokenchecker(TOKEN):
        TOKEN = input("Enter a valid Discord token >.< ").strip()
        if await tokenchecker(TOKEN):
            sb["TOKEN"] = TOKEN
            with open(json_file, "w") as file:
                json.dump(sb, file, indent=4)
            printwordwithgradient("Token accepted and saved to config.json")
        else:
            printwordwithgradient("Invalid token, please enter a valid token to continue: ")

    return TOKEN

TOKEN = asyncio.run(GetToken(sb, json_file))

if "LOGGING" not in sb or not isinstance(sb["LOGGING"], bool):
    LOGGING = input("Do you want to enable logging? (true/false) ").strip().lower()  

    # Validate input
    if LOGGING == "true":
        sb["LOGGING"] = True
    elif LOGGING == "false":
        sb["LOGGING"] = False
    else:
        print("Invalid input. Defaulting to logging disabled.")
        sb["LOGGING"] = False


    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)

LOGGING = sb.get("LOGGING", False)  

PREFIX = sb.get("PREFIX", "").strip() # checks for PREFIX within config.json if there is no PREFIX prompts the user to enter it then writes to the file
if not PREFIX:
    PREFIX = input("Enter what you want the prefix to be set as ")
    sb["PREFIX"] = PREFIX


    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)

WEATHERKEY = sb.get("WEATHERKEY", "").strip() # checks for WEATHERKEY within config.json if there is no WEATHERKEY sets a preset api key until replaced with your own
if not WEATHERKEY:
    WEATHERKEY = ("6eda74c50a8a47ba6d896888dae26c13")
    sb["WEATHERKEY"] = WEATHERKEY
    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)  

cls()  

prefix = PREFIX

bot = commands.Bot(command_prefix=prefix, self_bot=True,) # sets the bot variable and sets the prefix for the bot

bot.remove_command("help")

@bot.command()
async def webhookpurge(ctx): 
    """Deletes all existing webhooks in the channel."""
    channel = ctx.channel  

    if channel is not None:
        try:
            existing_webhooks = await channel.webhooks()  # Retrieve all webhooks
            for webhook in existing_webhooks:
                try:
                    await webhook.delete()  # Delete each webhook
                    print(f"Deleted webhook: {webhook.name}")  # Log deletion
                except discord.Forbidden:
                    print(f"Cannot delete webhook: Insufficient permissions.")
                except discord.HTTPException as e:
                    print(f"Error deleting webhook: {e}")

        except discord.HTTPException as e:
            print(f"Failed to retrieve webhooks: {e}")


@bot.command()
async def spam(ctx, Number=None, *, message): # sends a message the amount of times specified
  """spams a string the amount of times specified"""
  await ctx.message.delete()
  count = 0
  while count < int(Number):
      await ctx.send("{}".format(message))
      count = count + 1
      
@bot.command()
async def meow(ctx): # sends an ascii image of a cat
    await ctx.message.delete()
    await ctx.send('''**```
       ,
       \\`-._           __
        \\\\  `-..____,.'  `.
         :`.         /    \\`.
         :  )       :      : \\
          ;'        '   ;  |  :
          )..      .. .:.`.;  :
         /::...  .:::...   ` ;
         ; _ '    __        /:\\
         `:o>   /\\o_>      ;:. `.
        `-`.__ ;   __..--- /:.   \\
        === \\_/   ;=====_.':.     ;
         ,/'`--'...`--....        ;
              ;                    ;
            .'                      ;
          .'                        ;
        .'     ..     ,      .       ;
       :       ::..  /      ;::.     |
      /      `.;::.  |       ;:..    ;
     :         |:.   :       ;:.    ;
     :         ::     ;:..   |.    ;
      :       :;      :::....|     |
      /\\     ,/ \\      ;:::::;     ;
    .:. \\:..|    :     ; '.--|     ;
   ::.  :''  `-.,,;     ;'   ;     ;
.-'. _.'\\      / `;      \\,__:      \\
`---'    `----'   ;      /    \\,.,,,/
                   `----`              meow
```**''')

@bot.command()
async def deletechannels(ctx): # deletes all channels in the guild the message was sent requires admin (needs exceptions adding)
    """deletes all channels"""
    await ctx.message.delete()
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
    return

@bot.command()
async def help(ctx): # a guide to commands the bot has
    await ctx.message.delete()
    direction = await ctx.send("commands sent to terminal")
    printwithgradient('''```
- lawcan selfbot -

meow - sends an ASCII art of a cat
iplookup [ip address] - looks up an IP address
spam - [amount] [message] sends a message as many times as you choose (input how many times, then the message)
ban [user] [reason] - bans a user with an optional reason
kick [user] - kicks a user from the server
unban [user] - unbans a user
purge [amount] - deletes a specified number of messages
search [query] - searches Google for a query (currently outdated)
deletechannels - deletes all channels in the server
createchannels - creates a specified number of text channels with a given name
massban - bans all members in the server with a reason
webhookmessage [message] - sends a message via webhook with a specified username
webhookspam [amount] [message] - spams a message a specified number of times using webhooks
nuke - deletes all channels, creates new channels, deletes all roles, creates new roles, and bans all members
spamroles - creates a specified number of roles with a given name
ascii - generates ASCII art for a given message
lastraid - fetches the most recent raid completion for a given Destiny username
nuke2 - deletes all channels, creates new channels, deletes all roles, creates new roles, and bans all members (alternate version with different behavior)
getpfp [user] - retrieves the profile picture of a specified user or the command author if no user is specified
pc info - displays the pc components of the computer hosting the selfbot
ipping [ipaddress] - pings an ip address 
math [equation] - uses eval to complete math equations for you
weather [city name] - gets the weather of a given city name
time - sends the current time formatted as Y-%m-%d %H:%M:%S
generatenitro - sends a random nitro.gift link
dictionary [word] - looks up a word in the dictionary
activity [activity name] - sets your discord activity
editconfig [json file] [key] [value] - edits the config file
translate [language] [text] - translates text using google translate
cat - sends a cat image
dog - sends a dog image
usersearch [username] - searches a user and prints sites found with said user
massdm [message] - sends a message to all users in the server
massping [message] - pings all users in the server with an optional message
catfact - sends a random cat fact
crypto [coin] - gets the price of a specified cryptocurrency
uwuify [text] - uwuifies text
```''')
    await asyncio.sleep(5)
    await direction.delete()

@bot.command()
async def iplookup(ctx, TARGET_IP=None): # looks up an ip address using the ip-api api
    """looks up an ip address"""
    await ctx.message.delete()
    if TARGET_IP:
        try:
            RESPONSE = requests.get('http://ip-api.com/json/{}'.format(TARGET_IP))
            CONTENT = json.loads(RESPONSE.text)

            if str(CONTENT['status']) == 'success':
                await ctx.message.delete()
                one = TARGET_IP
                two = CONTENT['isp']
                three = CONTENT['city']
                four = CONTENT['regionName']
                five = CONTENT['lat']
                six = CONTENT['lon']

                await ctx.send('''```py
IP: {} 
ISP: {}
City: {}
Region: {}
Coordinates: {} LON, {} LAT
```'''.format(one, two, three, four, five, six))
            else:
                if str(CONTENT['message']) == 'invalid query':
                  await ctx.message.delete()
                  await ctx.send('``INVALID IP``')
        except:
            await ctx.send('`An error has occurred.`')
        return

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None): # bans the user pinged with no reason
    """bans a user"""
    await member.ban(reason=reason)
    await ctx.message.delete()
    return

@bot.command()
async def kick(ctx, member: discord.Member): # kicks a member
    """kicks a user"""
    await member.kick()
    await ctx.message.delete()
    return

@bot.command()
async def unban(ctx, member: discord.Member,): # unbans a member
    """unbans a user"""
    await member.unban()
    await ctx.message.delete()
    return

@bot.command()
async def purge(ctx, amount:int=None): #deletes all messages in a server from the user
    """deletes the amount of messages specified"""
    await ctx.message.delete()
    try:
        if amount is None:
            await ctx.send("Invalid amount")
        else:
            deleted = await ctx.channel.purge(limit=amount, before=ctx.message, check=message.author == bot.user) 
            await asyncio.sleep(3)
            await asd.delete()
    except:
        try:
            await asyncio.sleep(1)
            c = 0
            async for message in ctx.message.channel.history(limit=amount):
                if message.author == bot.user:
                    c += 1
                    await message.delete()
                else:
                    pass
            asd = await ctx.send('Deleted {} message(s)'.format((c)))
            await asyncio.sleep(3)
            await asd.delete()
        except Exception as e:
            await ctx.send(f"Error: {e}")
        return

@bot.command()
async def createchannels(ctx, number: int, channel_name): # creates the amount of channels specified with the name given 
    """creates the amount of channels specified with the name specified"""
    await ctx.message.delete()
    guild = ctx.guild
    channel_amount = 0
    while channel_amount < number:
       await guild.create_text_channel(channel_name)
       channel_amount +=1
    
@bot.command()
async def massban(ctx,  reason): # bans all users in a discord after checking if the command was used in a server and if the user has permissions
    """bans all users in a guild"""
    await ctx.message.delete()
    guild= ctx.guild
    if guild is None:
        
        return
    
    if not ctx.author.guild_permissions.ban_members:
        
        return
    
    for member in guild.members:
        if member != bot.user:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden:
                print("no workie need perms")
            except discord.HTTPException:
                print("also no workie")

@bot.command()
async def webhookmessage(ctx, message, user_name: str): # creates a webhook then sends a message using it
    """sends a message using a webhook"""
    await ctx.message.delete()
    channel = ctx.channel
    if channel is not None:
        await webhookpurge(ctx)
        webhook = await channel.create_webhook(name="LAWCAN")
        await webhook.send(message, username=user_name)
    else:
        pass

@bot.command()
async def webhookspam(ctx, amount: int, message: str): # uses webhooks to spam messages while avoiding ratelimits through rotating between them 
    """uses webhooks to spam a message avoiding rate limits"""
    await ctx.message.delete()
    channel = ctx.channel
    counter = 0
    webhooks = []
    webhook_limit = 15  

    if channel is not None:
        await webhookpurge(ctx)
        for i in range(webhook_limit):
            webhook = await channel.create_webhook(name=f"webspam-{i + 1}")
            webhooks.append(webhook)
        
        try:
            while counter < amount:

                for webhook in webhooks:
                    if counter >= amount:
                        break  

                    try:
                        await webhook.send(message, username="Lawcan")
                        counter += 1
                        
                        await asyncio.sleep(1)  
                    except discord.HTTPException as e:
                        if e.status == 429:  
                            
                            new_webhook = await channel.create_webhook(name=f"webspam-{len(webhooks) + 1}")
                            webhooks.append(new_webhook)
                        else:
                            raise 

        except discord.Forbidden:
            await ctx.send("need admin")
        except discord.HTTPException as e:
            await ctx.send(f"An HTTP error occurred: {e}")
# needs work

@bot.command()
async def spamroles(ctx, number: int, role_name: str): # creates the amount of roles specified with the rolename specified
    """creates an amount of roles specified"""
    await ctx.message.delete()
    role_amount = 0
    while role_amount < number:
        try:
            await ctx.guild.create_role(name=role_name)
            role_amount += 1
        except discord.Forbidden:
            await ctx.send("Cannot create role. Missing permission.")
            break
        except discord.HTTPException as e:
            await ctx.send(f"http error {e}")
            break

async def deleteroles(ctx): # loops through every role in a server and deletes them all other than the default @everyone role
    """deletes all roles"""
    await ctx.message.delete()
    roles = ctx.guild.roles
    roles_to_delete = [role for role in roles if role.name != "@everyone" and role != ctx.guild.me.top_role]
    for role in roles_to_delete:
        try:
            await role.delete()
        except discord.Forbidden:
            await ctx.send("Cannot delete roles. Missing permies")
            return
        except discord.HTTPException as e:
            await ctx.send(f"HTTP error occurred while deleting role {role.name}: {e}")
            return

@bot.command()
async def search(ctx, *, query: str): # uses bs4 html parsing to find the first 6 webpages that show up in results from google for your given search query
    """searches for the first six search results using google"""
    await ctx.message.delete()
    search_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    
    search_results = []
    for g in soup.find_all('div', class_='tF2Cxc', limit=6):  
        title = g.find('h3').text
        link = g.find('a')['href']
        search_results.append(f"[{title}]({link})")

    if search_results:
        await ctx.send("\n".join(search_results))
    else:
        await ctx.send("No results found.")

@bot.command()
async def ascii(ctx, *, message): # uses pyfiglets library to change your letters into ascii and uses markdowns to ensure the messages indent properly
    """converts text to ascii"""
    await ctx.message.delete()
    ascii_art = pyfiglet.figlet_format(message)
    await ctx.send(f"```{ascii_art}```")

API_KEY = 'ec05741ca2d94292b8aef3537e6421fc'#replace with your own api key if you want >.<
BASE_URL = 'https://www.bungie.net/Platform/Destiny2/'

headers = {
    'X-API-Key': API_KEY
}

raid_name_map = {
    2693136600: 'Leviathan',
    3089205900: 'Eater_of_Worlds',
    119944200: 'Spire_of_Stars',
    548750096: 'Scourge_of_the_Past',
    3333172150: 'Crown_of_Sorrow',
    2122313384: 'Last_Wish',
    1042180643: 'Garden_of_Salvation',
    910380154: 'Deep_Stone_Crypt',
    3881495763: 'Vault_of_Glass',
    1441982566: 'Vow_of_the_Disciple',
    1374392663: 'Kings_Fall',
    2381413764: 'Root_of_Nightmares',
    2192826039: 'Salvation\'s Edge'
}
# bungie api docs are impossible to read even more impossible to document afterwards but searches for the username in the bungie.net api for the membership type and id then gets the most recent raid for each character then checks which is the most recent
def get_membership_id_and_type(username):
    """searches a bungie username for the type and id"""
    
    encoded_username = urllib.parse.quote(username)
    search_endpoint = f'{BASE_URL}SearchDestinyPlayer/-1/{encoded_username}/'
    
    try:
        response = requests.get(search_endpoint, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return None, None, f"Error fetching membership details: {str(e)}"
    
    data = response.json()
    if 'Response' in data and data['Response']:
        membership_type = data['Response'][0]['membershipType']
        membership_id = data['Response'][0]['membershipId']
        return membership_id, membership_type, None
    else:
        return None, None, "Username not found or invalid."

def get_most_recent_raid(membership_id, membership_type): # checks the last raid completion for each character then returns the most recent raid
    """gets the last completed raid for an account"""
    characters_endpoint = f'{BASE_URL}{membership_type}/Profile/{membership_id}/?components=200'
    try:
        response = requests.get(characters_endpoint, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching character data: {str(e)}"

    characters_data = response.json()
    character_ids = characters_data['Response']['characters']['data'].keys()

    most_recent_raid = None
    most_recent_raid_index = None

    for character_id in character_ids:
        activities_endpoint = f'{BASE_URL}{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/Activities/'
        params = {
            'mode': '4',
            'count': '1',
            'page': '0'
        }

        try:
            response = requests.get(activities_endpoint, headers=headers, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Error fetching activities data for character {character_id}: {str(e)}"

        data = response.json()
        activities = data['Response']['activities']
        if activities:
            last_raid = activities[0]
            raid_time = datetime.fromisoformat(last_raid['period'].replace('Z', '+00:00'))
            duration_seconds = last_raid['values']['activityDurationSeconds']['basic']['value']
            duration = timedelta(seconds=duration_seconds)
            raid_index = activities.index(last_raid) + 1  

            if most_recent_raid is None or raid_time > most_recent_raid['time']:
                most_recent_raid = {
                    'time': raid_time,
                    'raid': last_raid,
                    'duration': duration
                }
                most_recent_raid_index = raid_index

    if most_recent_raid:
        raid_reference_id = most_recent_raid['raid']['activityDetails']['referenceId']
        raid_name = raid_name_map.get(raid_reference_id, "Unknown Raid")
        duration = most_recent_raid['duration']

        return (
            f"Most recent raid completion:\n"
            f"Raid Name: {raid_name}\n"
            f"Completion Time: {most_recent_raid['time']}\n"
            f"Duration: {str(duration)}\n"
            f"Raid Index: {most_recent_raid_index}"
        )
    else:
        return "No raid completions found for any character."

@bot.command()
async def lastraid(ctx, username: str = None): # sends the most recent raid from a given user
    await ctx.message.delete()
    """sends the last raid completed by a user"""
    if username is None:
        username = "bring hotswapping back :)#5380"  
    membership_id, membership_type, error = get_membership_id_and_type(username)
    if error:
        await ctx.send(error)
        return

    await ctx.message.delete()
    raid_info = get_most_recent_raid(membership_id, membership_type)
    await ctx.send(f"lawcan\n{raid_info}\n{username}")

@bot.command()
async def nuke2(ctx): # nukes a server in a very rudimentary way which likely will result in ratelimits and makes bans very easy
    """nukes discord server without the use of webhoooks"""
    await ctx.message.delete()
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You don't have perms silly :3.")
        return

    await deletechannels(ctx)
    await massban(ctx, reason="Lawcan")
    await createchannels(ctx, number=50, channel_name="lawcan")
    await deleteroles(ctx)
    await spamroles(ctx, number=250, role_name="lawcan")

@bot.command()
async def getpfp(ctx, member: discord.User = None):
    """gets the avatar of a member"""
    if member is None:
        member = ctx.author
    pfp = member.avatar.url
    await ctx.send(f"{pfp}")

async def DeleteChannels(ctx):
    """deletes every channel"""
    for channel in ctx.guild.channels:
        if channel.name.lower() == "lawcan":  
            continue  # skips channels named lawcan

        try:
            await channel.delete()
        except discord.Forbidden:
            printwordwithgradient(f"Cannot delete channel: {channel.name}. lf perms.")
        except discord.HTTPException as e:
            printwordwithgradient(f"Failed to delete channel: {channel.name} due to an HTTP error >.<. {e}")

async def MaxOutChannels(ctx, number=50, channel_name="lawcan"): 
    """
    maxes out channels
    """
    channel_amount = 0
    while channel_amount < number:
        try:
            await ctx.guild.create_text_channel(channel_name)
            channel_amount += 1
        except discord.Forbidden:
            printwordwithgradient("lf perms")
            break
        except discord.HTTPException as e:
            printwordwithgradient(f"Failed to create channel due to an HTTP error >.<. error is {e}")
            break

async def MassBan(ctx, reason="lawcan"): 
    """bans all users"""
    for member in ctx.guild.members:
        if member != ctx.bot.user:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden:
                print(f"Failed to ban {member}. lf perms.")
            except discord.HTTPException as e:
                print(f"Failed to ban {member} due to an HTTP error. {e}")

async def DeleteRoles(ctx, webhook): # deletes all roles
    """
    deletes all roles
    """
    roles = ctx.guild.roles
    roles_to_delete = [role for role in roles if role.name != ["@everyone", "lawcan"] and role != ctx.guild.me.top_role]
    for role in roles_to_delete:
        try:
            await role.delete()
        except discord.Forbidden:
            printwordwithgradient("lf perms")
            return
        except discord.HTTPException as e:
            printwordwithgradient(f"HTTP error occurred while deleting role {role.name}: {e}")
            return

async def SpamRole(ctx, channel: discord.TextChannel, number: int = 250, role_name: str = "lawcan"):
    """
    Creates the max amount of roles
    """
    # Create a webhook in the specified channel
    try:
        webhook = await channel.create_webhook(name="spam_roles")
    except discord.Forbidden:
        printwordwithgradient("needs perms")
        return
    except discord.HTTPException as e:
        printwordwithgradient(f"HTTP error occurred while creating webhook: {e}")
        return

    role_amount = 0
    while role_amount < number:
        try:
            # Create a role in the guild
            await ctx.guild.create_role(name=role_name)
            role_amount += 1

        except discord.Forbidden:
            printwordwithgradient("Lack of permissions to create roles.")
            break
        except discord.HTTPException as e:
            printwordwithgradient(f"HTTP error occurred while creating role: {e}")
            break
        except Exception as e:
            printwordwithgradient(f"An unexpected error occurred: {e}")
            break

@bot.command()
async def nuke(ctx): # gathers all nuke commands and processes them at once
    """nukes discord server"""    
    await ctx.message.delete()
    printwordwithgradient(f"nuking: {ctx.guild}")
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You don't have perms silly :3.")
        return
    await webhookpurge(ctx)

    tasks = [
        asyncio.create_task(MassBan(ctx, reason="lawcan")),
        asyncio.create_task(DeleteChannels(ctx)),
        asyncio.create_task(MaxOutChannels(ctx,)),
        asyncio.create_task(SpamRole(ctx,)),
        asyncio.create_task(DeleteRoles(ctx,))
    ]
    await asyncio.gather(*tasks)

async def getarea(city_name: str): # uses openweathermap to get the latitude/longitude of an area based on the cities name
    """gets the lat/lon of an area based on the city name"""
    city_name_encoded = quote(city_name)
    cityurl = f"https://api.openweathermap.org/data/2.5/weather?q={city_name_encoded}&appid={WEATHERKEY}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(cityurl) as response:
                if response.status == 404:
                    raise ValueError(f"City '{city_name}' not found.")
                response.raise_for_status()
                areadata = await response.json()
        
        if "coord" in areadata:
            latitude = areadata['coord']['lat']
            longitude = areadata['coord']['lon']
            return latitude, longitude
        else:
            return None, None
    except aiohttp.ClientError as e:
        raise ValueError(f"An error occurred while fetching coordinates: {str(e)}")

@bot.command()
async def weather(ctx, city_name: str): # gets the weather of an area based on city name using openweathermap api
    """gets the weather of a location"""
    await ctx.message.delete()
    try:
        latitude, longitude = await getarea(city_name)
        if latitude is None or longitude is None:
            await ctx.send("There are no cities found with this name")
            return
        
        weatherurl = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHERKEY}&units=metric"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(weatherurl) as response:
                response.raise_for_status()
                weatherdata = await response.json()
        
        city = weatherdata.get('name')
        temperature = weatherdata['main'].get('temp')
        description = weatherdata['weather'][0].get('description')
        
        if city and temperature is not None and description:
            weatherinfo = (f"**Weather in {city}:**\n"
                f"Temperature: {temperature}°C\n"
                f"Condition: {description.capitalize()}")
        else:
            weatherinfo = "Could not find weather information"
    
    except ValueError as e:
        weatherinfo = str(e)
    except aiohttp.ClientError as e:
        weatherinfo = f"An error occurred while fetching weather data: {str(e)}"
    
    await ctx.send(weatherinfo)
    
@bot.command()
async def math(ctx, numbers: str): # calculates mathmatical equations using the eval function 
    """uses eval to complete math queries for you"""
    await ctx.message.delete()
    numbers = numbers.replace('x', '*').replace('÷', '/')
    try:
        result = eval(numbers)
        await ctx.send(f"{numbers} = {result}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
@bot.command()
async def ipping(ctx, ip: str): # pings an ip and send the response name
    """pings an ip address"""
    await ctx.message.delete()
    try:
        response_time = ping(ip)
        if response_time is None:
            await ctx.send("Response timed out.")
        else:
            await ctx.send(f"Ping: replied in{response_time:.2f} seconds.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
@bot.command()
async def editconfig(ctx, json_file, key, value): # writes values to the json file incase you wish to change token or weathermap api key without opening the file
    """finds and changes configs"""
    await ctx.message.delete()
    try:
        with open(json_file, "r") as file:
            sb = json.load(file)
    except FileNotFoundError:
        sb = {}
    sb[key] = value.strip()
    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)

def get_linux_distro():
    """
    Retrieves the Linux distribution name from /etc/os-release
    """
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("PRETTY_NAME="):
                return line.split("=")[1].strip().replace('"', '')
    except FileNotFoundError:
        return "Unknown Linux Distro"

def get_pc_parts():
    """
    Returns each PC component information, works on both Linux and Windows.
    """
    # Declare variables
    cpuname = ""
    gpuname = ""
    raminfo = ""
    diskinfo = ""
    
    # Check platform
    ostype = platform.system().lower()

    # Get CPU name
    if ostype == "windows":
        import wmi
        computer = wmi.WMI()
        for cpu in computer.Win32_Processor(): 
            cpuname = f"**CPU**: {cpu.Name}\n"
    else:
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpuname = f"**CPU**: {line.split(':')[1].strip()}\n"
                        break
        except FileNotFoundError:
            cpuname = "**CPU**: Could not determine CPU name\n"

    # Get GPU name
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            gpuname += f"**GPU**: {gpu.name}\n"
    else:
        try:
            # nvidia on linux makes me sad
            result = subprocess.run(['lspci'], stdout=subprocess.PIPE)
            gpu_info = result.stdout.decode()
            gpu_lines = [line for line in gpu_info.splitlines() if 'VGA' in line or '3D controller' in line]
            if gpu_lines:
                gpuname = "**GPU**: " + ", ".join([line.split(":")[-1].strip() for line in gpu_lines]) + "\n"
            else:
                gpuname = "**GPU**: No dedicated GPU found\n"
        except Exception:
            gpuname = "**GPU**: Could not determine GPU info\n"

    # Get RAM info
    if ostype == "windows":
        for ram in computer.Win32_PhysicalMemory():
            raminfo += f"**RAM**: {ram.Manufacturer} {int(ram.Capacity) / (1024 ** 3):.2f} GB\n"
    else:
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        raminfo = f"**RAM**: Total {total_ram_gb:.2f} GB\n"

    # Get Disk info
    if ostype == "windows":
        for disk in computer.Win32_DiskDrive():
            diskinfo += f"**Disk Drive**: {disk.Model} ({int(disk.Size) / (1024 ** 3):.2f} GB)\n"
    else:
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,SIZE,MODEL'], stdout=subprocess.PIPE)
            disk_lines = result.stdout.decode().splitlines()[1:]  # Skip the header
            diskinfo = "**Disk Drives**:\n"
            for line in disk_lines:
                if not line.strip().startswith("├") and not line.strip().startswith("└"):
                    diskinfo += f"- {line.strip()}\n"
        except Exception:
            diskinfo = "**Disk Drive**: Could not retrieve disk info\n"

    # Get total amount of RAM
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    
    # Get OS name
    osname = f"**Operating System**: {ostype.capitalize()}"

    if ostype == "linux":
        distro = get_linux_distro()
        osname = f"**Operating System**: Linux ({distro})"
    else:
        osname = f"**Operating System**: {ostype.capitalize()}"

    # list of parts
    pcparts = (
        f"{cpuname}"
        f"{gpuname}"
        f"{raminfo}"
        f"**Total RAM**: {total_ram:.2f} GB\n"
        f"{diskinfo}"
        f"{osname}"
    )
    
    return pcparts

@bot.command()
async def pcinfo(ctx):
    """sends a message containing each pc component"""
    await ctx.message.delete()
    parts = get_pc_parts()
    await ctx.send(f"{parts}")
    
@bot.command()
async def generatenitro(ctx):
    """sends a formatted random nitro.gift link with the possibility to send nitro"""
    await ctx.message.delete() #unlikely to ever work just wanted to add cos cool feature very very useless
    nitrocode = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(f"discord.gift/{nitrocode}")

@bot.command()
async def time(ctx):
    """sends the current time in a message""" # gets the current time using date time
    await ctx.message.delete()
    time = datetime.now()
    formattedtime = time.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"the time is: {formattedtime}")

async def word(dictionaryword):
    """gets the definitions of a word from dictionary api"""
    dictionaryurl = f"https://api.dictionaryapi.dev/api/v2/entries/en/{dictionaryword}" # sets url for the dictionary api
    
    async with aiohttp.ClientSession() as session:
        async with session.get(dictionaryurl) as response:
            data = await response.json()
            return data # returns the information from the api

@bot.command()
async def dictionary(ctx, dictionaryword):
    """looks up a word in the dictionary api"""
    await ctx.message.delete()
    
    try:
        data = await word(dictionaryword)
        if isinstance(data, list) and "word" in data[0]:
            word_info = data[0]
            meanings = word_info.get('meanings', [])
            definitions_list = []
            
            for meaning in meanings:
                definitions = meaning.get('definitions', [])
                for definition in definitions:
                    definitions_list.append(definition['definition'])
                    if len(definitions_list) == 3:  
                        break
                if len(definitions_list) == 3:
                    break

            if definitions_list:
                definitions_text = "\n".join([f"{i+1}. {definition}" for i, definition in enumerate(definitions_list)])
                await ctx.send(f"**{word_info['word']}**:\n{definitions_text}")
            else:
                await ctx.send(f"No definitions found for {dictionaryword}.")
        else:
            await ctx.send(f"Word not found: {dictionaryword}.")
    except Exception as e:
        await ctx.send(f"An oopsie happened: {str(e)}")

coderegex = re.compile(r"(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
ready = False 

@bot.event
async def on_message(ctx):
    """checks messages for nitro gift links"""
    global ready
    if not ready:
        ready = True
    
    if bot.user.mention in ctx.content:
        if ctx.guild == None:
            printwordwithgradient(f"({bot.user}) mentioned by: ({ctx.author}) | message: {ctx.content} | in: Direct messages")
        else:
            printwordwithgradient(f"({bot.user}) mentioned by: ({ctx.author}) | message: {ctx.content} | in: {ctx.guild}")

    # checks messages for discord gift links
    if coderegex.search(ctx.content):
        code = coderegex.search(ctx.content).group(2)
        asyncio.create_task(redeemgiftcode(ctx.channel.id, code))    
    await bot.process_commands(ctx)  # idk what this does but it fixes all my problems so its here now ig

async def redeemgiftcode(channel_id, code): # redeems the code
    """redeems a gift code"""
    async with httpx.AsyncClient() as client:
        try:
            result = await client.post(
                f'https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem',
                json={'channel_id': str(channel_id)},
                headers={'authorization': TOKEN, 'user-agent': 'Mozilla/5.0'}
            )

            
            if result.status_code == 200:
                print('\033[32m' + 'Successfully redeemed gift code!' + '\033[0m')  # success message in pretty green
            else:
                print('\033[31m' + json.dumps(result.json(), indent=4) + '\033[0m')  # evil error message in red to show its evil
        except Exception as e:
            print('\033[31m' + f'An error occurred: {str(e)}' + '\033[0m')  # same thing as the other one in red

@bot.command()
async def activity(ctx,new_status: str):
    await ctx.message.delete()
    status = discord.Status.do_not_disturb
    await bot.change_presence(status=status, activity=discord.Game(name=new_status))
    
@bot.command()
async def qrcodegen(ctx, link):
    """generates a qrcode based on a given link"""
    await ctx.message.delete()
    qr = qrcode.QRCode(
        version=2,  
        error_correction=qrcode.constants.ERROR_CORRECT_L,  
        box_size=30,  
        border=5,  
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    #saves the image in a buffer
    with io.BytesIO() as buf:
        img.save(buf, format='PNG')
        buf.seek(0)  
        await ctx.send(file=discord.File(buf, filename='qrcode.png'))

catart = r'''
       ,
       \`-._           __
        \\  `-..____,.'  `.
         :`.         /    \` .
         :  )       :      : \
          ;'        '   ;  |  :
          )..      .. .:.`.;  :
         /::...  .:::...   ` ;
         ; _ '    __        /: \
         `:o>   /\o_>      ;:. `.
        `-`.__ ;   __..--- /:.   \
        === \_/   ;=====_.':.     ;
         ,/'`--'...`--....        ;
              ;                    ;
            .'                      ;
          .'                        ;
        .'     ..     ,      .       ;
       :       ::..  /      ;::.     |
      /      `.;::.  |       ;:..    ;
     :         |:.   :       ;:.    ;
     :         ::     ;:..   |.    ;
      :       :;      :::....|     |
      /\     ,/ \      ;:::::;     ;
    .:. \:..|    :     ; '.--|     ;
   ::.  :''  `-.,,;     ;'   ;     ;
.-'. _.'\      / `;      \\,__:      \
`---'    `----'   ;      /    \\,.,,,/
                   `----`              
██       ██████  ██████   ██████  █████  ███    ██     ███████ ███████ ██      ███████ ██████   ██████  ████████ 
██      ██    ██ ██   ██ ██      ██   ██ ████   ██     ██      ██      ██      ██      ██   ██ ██    ██    ██    
██      ██    ██ ██████  ██      ███████ ██ ██  ██     ███████ █████   ██      █████   ██████  ██    ██    ██    
██      ██    ██ ██   ██ ██      ██   ██ ██  ██ ██          ██ ██      ██      ██      ██   ██ ██    ██    ██    
███████  ██████  ██   ██  ██████ ██   ██ ██   ████     ███████ ███████ ███████ ██      ██████   ██████     ██    
                                                                                                                 
'''
def printwithgradient(text):
    """prints art with a gradient"""
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)
    print(Style.RESET_ALL)

printwithgradient(catart)

def printwordwithgradient(word):
    """Prints a word with a gradient."""
    gradient_colors = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,
        Fore.BLUE,
        Fore.MAGENTA,
    ]
    
    gradient_length = len(gradient_colors)
    word_length = len(word)
    
    step = word_length / gradient_length
    
    colored_word = ''
    
    for i, char in enumerate(word):
        color_index = min(int(i // step), gradient_length - 1)  
        colored_word += f"{gradient_colors[color_index]}{char}"
    
    print(colored_word + Style.RESET_ALL)

logging = LOGGING 

@bot.event
async def on_message_delete(message):
    """logs deleted messages"""
    if logging == True:
        if message.author == bot.user:
            return
        elif message.guild is None:
            printwordwithgradient(f"user: {message.author} | deleted message: {message.content} | in: Direct messages")
        else:
            printwordwithgradient(f"user: {message.author} | deleted message: {message.content} | in: {message.guild}")

 

@bot.before_invoke
async def log_command(ctx):
    """logs commands to the terminal"""
    commandused = ctx.command.name
    messagesent = ctx.message.content
    args = messagesent[len(ctx.prefix) + len(commandused):].strip()
    command_info = f"Command: `{commandused}` | Arguments: `{args}`"
    printwordwithgradient(command_info)

@bot.command()
async def clear(ctx):
    """clears the terminal"""
    await ctx.message.delete()  
    cls()
    printwithgradient(catart)

@bot.command()
async def terminaloutput(ctx, art):
    """prints out a message with a gradient"""
    await ctx.message.delete()
    printwithgradient(art)

@bot.command()
async def guilds(ctx):
    """prints all guilds the user is in"""
    await ctx.message.delete()
    printwordwithgradient(f"list of guilds {bot.user} is in")
    for guild in bot.guilds:
        guild_name = f" Guild: {guild.name} "  
        boxwidth = len(guild_name)
        #makes it look all pretty and adds boxes around the guild name
        printwordwithgradient("+" + "-" * boxwidth + "+")
        printwordwithgradient("|" + guild_name + "|")
        printwordwithgradient("+" + "-" * boxwidth + "+")

languagenames = {code: name.capitalize() for code, name in LANGUAGES.items()}

@bot.command()
async def translate(ctx, language: str, *, text: str):
    """
    Translates text to the specified language
    """
    await ctx.message.delete()
    try:
        # translates text to the specified language
        translation = translator.translate(text, dest=language)
        # gets the full language name
        fulllangname = languagenames.get(language, language)
        # sends the translated text
        await ctx.send(f"**Language {fulllangname}:**\n{translation.text}")
    except Exception as e:
        # error handling
        await ctx.send(f"Error: {str(e)}")
        
@bot.command()
async def cat(ctx):
    """sends a random cat image"""
    await ctx.message.delete()
    caturl = "https://api.thecatapi.com/v1/images/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(caturl) as response:
            catdata = await response.json()
            catimage = catdata[0]['url']
            await ctx.send(catimage)

@bot.command()
async def dog(ctx):
    """sends a random dog image"""
    await ctx.message.delete()
    dogurl = "https://dog.ceo/api/breeds/image/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(dogurl) as response:
            dogdata = await response.json()
            dogimage = dogdata['message']
            await ctx.send(dogimage)

def check_username(username):
    websites = {
        # Social Media
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}/",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Tumblr": f"https://{username}.tumblr.com",
        
        # Developer Platforms
        "Stack Overflow": f"https://stackoverflow.com/users/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Bitbucket": f"https://bitbucket.org/{username}/",
        "CodePen": f"https://codepen.io/{username}",
        
        # Other Platforms
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "Vimeo": f"https://vimeo.com/{username}",
        "WordPress": f"https://{username}.wordpress.com",
    }

    found_accounts = []

    for site, url in websites.items():
        response = requests.get(url)
        if response.status_code == 200:
            found_accounts.append((site, url))

    return found_accounts

@bot.command()
async def usersearch(ctx, username: str):
    """checks for accounts with the same username"""
    await ctx.message.delete()
    found_accounts = check_username(username)
    if found_accounts:
        accounts_text = "\n".join([f"[{site}]({url})" for site, url in found_accounts])
        printwordwithgradient(f"Found accounts with the username \n {username}\n{accounts_text}")

@bot.command()
async def massping(ctx, meowsage: str):
    """pings everyone in the server individually with an optional message"""
    try:
        await ctx.message.delete()
        for member in ctx.guild.members:
                if member != ctx.author:
                    await ctx.send(f"{member.mention} {meowsage}")
    except Exception as e: 
        printwordwithgradient(f"Error: {e}")

@bot.command()
async def massdm(ctx, meowsage: str):
    """direct messages every member in the server with a message"""
    try:
        await ctx.message.delete()
        for member in ctx.guild.members:
            if member != ctx.author:
                try:
                    await member.send(meowsage)
                except discord.Forbidden:
                    printwordwithgradient(f"Could not message: {member}")
    except Exception as e:
        printwordwithgradient(f"Error: {e}")
        pass

@bot.command()
async def catfact(ctx):
    """sends a random cat fact"""
    await ctx.message.delete()
    catfacturl = "https://catfact.ninja/fact"
    async with aiohttp.ClientSession() as session:
        async with session.get(catfacturl) as response:
            catfactdata = await response.json()
            catfact = catfactdata['fact']
            await ctx.send(f"catfact: {catfact}")


crypto_map = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ltc": "litecoin",
    "doge": "dogecoin",
    "xrp": "ripple",
    "ada": "cardano",
    "sol": "solana",
    "dot": "polkadot",
    "bnb": "binancecoin",
    "matic": "matic-network",
    "xmr": "monero",
}

@bot.command()
async def crypto(ctx, cryptocurrency: str):
    """Gets the current price of a cryptocurrency"""
    await ctx.message.delete()

    crypto_name = crypto_map.get(cryptocurrency.lower(), cryptocurrency.lower())

    cryptourl = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(cryptourl) as response:
            if response.status == 200:
                data = await response.json()
                if crypto_name in data:
                    price = data[crypto_name]['usd']
                    await ctx.send(f"{cryptocurrency.upper()}: ${price}")
                else:
                    await ctx.send("Cryptocurrency not found. Please try another.")
            else:
                await ctx.send("Failed to retrieve data. Please try again later.")

@bot.command()
async def uwuify(ctx, *, message: str):
    """UwUifies a message with a chance to stutter the first word."""
    await ctx.message.delete()
    

    words = message.split()
    if words and random.random() < 0.3: 
        words[0] = f"{words[0][0]}-{words[0][0]}-{words[0]}" #30% chance to stutter the first word
    
    #uwuifies the message
    message = " ".join(words)
    uwuified = (
        message.replace('r', 'w')
               .replace('l', 'w')
               .replace('R', 'W')
               .replace('L', 'W')
               .replace("ove", "uv")
               .replace("th", "ff")
               .replace("you", "uu")
               .replace("!", " uwu")
    )
    
    await ctx.send(uwuified) #sends the uwuified message

bot.run(TOKEN, log_handler=None)
