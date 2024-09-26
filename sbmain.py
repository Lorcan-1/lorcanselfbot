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
import wmi
import GPUtil
import psutil
import random
import string
import re
import httpx
import qrcode
import io

computer = wmi.WMI() 

folder_sb = os.path.dirname(os.path.realpath(__file__)) # checks for config.json within the file path if it is missing creates then reads from the file
json_file = os.path.join(folder_sb, 'config.json')
if os.path.exists(json_file):

    with open(json_file, 'r') as file:
        sb = json.load(file)
else:
    sb = {}

TOKEN = sb.get("TOKEN", "").strip() # checks for TOKEN within config.json if there is no TOKEN prompts the user to enter it then writes to the file
if not TOKEN:
    TOKEN = input("Enter your token >.< ")
    sb["TOKEN"] = TOKEN


    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)

WEATHERKEY = sb.get("WEATHERKEY", "").strip() # checks for WEATHERKEY within config.json if there is no WEATHERKEY sets a preset api key until replaced with your own
if not WEATHERKEY:
    WEATHERKEY = ("6eda74c50a8a47ba6d896888dae26c13")
    sb["WEATHERKEY"] = WEATHERKEY
    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)    

bot = commands.Bot(command_prefix='`', self_bot=True,) # sets the bot variable and sets the prefix for the bot

@bot.command()
async def webhookpurge(ctx): # checks if the message was sent in a channel then deletes any existing webhooks 
    """deletes all pre existing webhooks"""
    channel = ctx.channel  
    
    if channel is not None:
        try:
            existing_webhooks = await channel.webhooks()  
            for webhook in existing_webhooks:
                try:
                    await webhook.delete()
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
    await ctx.send('''```
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
```''')

@bot.command()
async def deletechannels(ctx): # deletes all channels in the guild the message was sent requires admin (needs exceptions adding)
    """deletes all channels"""
    await ctx.message.delete()
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
    return

@bot.command()
async def commands(ctx): # a guide to commands the bot has
    await ctx.message.delete()
    await ctx.send('''```
- skibidi toilet -

meow - sends an ASCII art of a cat
lookup - looks up an IP address
spam - sends a message as many times as you choose (input how many times, then the message)
ban - bans a user with an optional reason
kick - kicks a user from the server
unban - unbans a user
purge - deletes a specified number of messages
search - searches Google for a query (currently outdated)
deletechannels - deletes all channels in the server
createchannels - creates a specified number of text channels with a given name
massban - bans all members in the server with a reason
webhookmessage - sends a message via webhook with a specified username
webhookspam - spams a message a specified number of times using webhooks
nuke - deletes all channels, creates new channels, deletes all roles, creates new roles, and bans all members
spamroles - creates a specified number of roles with a given name
ascii - generates ASCII art for a given message
lastraid - fetches the most recent raid completion for a given Destiny username
nuke2 - deletes all channels, creates new channels, deletes all roles, creates new roles, and bans all members (alternate version with different behavior)
getpfp - retrieves the profile picture of a specified user or the command author if no user is specified
pc info - displays the pc components of the computer hosting the selfbot
ipping - pings an ip address 
math - uses eval to complete math equations for you
weather - gets the weather of a given city name
time - sends the current time formatted as Y-%m-%d %H:%M:%S
generatenitro - sends a random nitro.gift link
```''')

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
        await webhookpurge()
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
        await webhookpurge()
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
    """searches for the 1st six search results using google"""
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

API_KEY = 'a63ac83a451949e1ae91fe3bbf2ee450'#replace with your own api key if you want >.<
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
        username = "lawcan#7065"  
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

async def deletechannels_webhook(ctx): # uses webhooks to delete all channels
    """uses webhooks to delete every channel"""
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except discord.Forbidden:
            print(f"Cannot delete channel: {channel.name}. lf perms.")
        except discord.HTTPException as e:
            print(f"Failed to delete channel: {channel.name} due to an HTTP error >.<. {e}")

async def massban_webhook(ctx, reason="lawcan"): 
    """uses webhooks to ban all users"""
    for member in ctx.guild.members:
        if member != ctx.bot.user:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden:
                print(f"Failed to ban {member}. lf perms.")
            except discord.HTTPException as e:
                print(f"Failed to ban {member} due to an HTTP error. {e}")

async def createchannels_webhook(ctx, number=50, channel_name="lawcan"): 
    """
    uses webhooks to max out channels
    """
    channel_amount = 0
    while channel_amount < number:
        try:
            await ctx.guild.create_text_channel(channel_name)
            channel_amount += 1
        except discord.Forbidden:
            print("lf perms")
            break
        except discord.HTTPException as e:
            print(f"Failed to create channel due to an HTTP error >.<. error is {e}")
            break

async def deleteroles_webhook(ctx): # deletes all roles
    """
    uses webhooks to delete all roles
    """
    roles = ctx.guild.roles
    roles_to_delete = [role for role in roles if role.name != "@everyone" and role != ctx.guild.me.top_role]
    for role in roles_to_delete:
        try:
            await role.delete()
        except discord.Forbidden:
            print("lf perms")
            return
        except discord.HTTPException as e:
            print(f"HTTP error occurred while deleting role {role.name}: {e}")
            return

async def spamroles_webhook(ctx, number=250, role_name="lawcan"):
    """
    uses webhooks to max out roles
    """
    role_amount = 0
    while role_amount < number:
        try:
            await ctx.guild.create_role(name=role_name)
            role_amount += 1
        except discord.Forbidden:
            print("lf perms")
            break
        except discord.HTTPException as e:
            print(f"HTTP error occurred while creating role: {e}")
            break

@bot.command()
async def nuke(ctx): # uses webhooks to nuke a server while avoiding ratelimits and minimising chance of discord detecting selfbotting
    await ctx.message.delete()
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You don't have perms silly :3.")
        return
    await webhookpurge()
    #Assign a webhook for each action
    webhookspam_channeldel = await ctx.channel.create_webhook(name="channeldelete_web")
    webhookspam_massban = await ctx.channel.create_webhook(name="massban_web")
    webhookspam_spamchannel = await ctx.channel.create_webhook(name="spamchannel_web")
    webhookspam_delroles = await ctx.channel.create_webhook(name="delroles_web")
    webhookspam_spamroles = await ctx.channel.create_webhook(name="spamroles_web")

    #delete all channels and roles at the same time avoiding ratelimits
    await asyncio.gather(
        deletechannels_webhook(ctx),
        deleteroles_webhook(ctx)
    )
    
    #i hate this
    tasks = [
        asyncio.create_task(massban_webhook(ctx, reason="lawcan")),
        asyncio.create_task(createchannels_webhook(ctx, number=50, channel_name="lawcan")),
        asyncio.create_task(spamroles_webhook(ctx, number=250, role_name="lawcan"))
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

def get_pc_parts():
    """
    returns each pc component
    """
    #get cpuname
    cpuname = ""
    for cpu in computer.Win32_Processor(): 
        cpuname = f"**CPU**: {cpu.Name}\n"

    #get gpu name
    gpuname = ""
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            gpuname += f"**GPU**: {gpu.name}\n"
    else:
        gpuname = "**GPU**: No dedicated GPU found\n"

    #getraminfo
    raminfo = ""
    for ram in computer.Win32_PhysicalMemory():
        raminfo += f"**RAM**: {ram.Manufacturer} {int(ram.Capacity) / (1024 ** 3):.2f} GB\n"

    #get diskinfo
    diskinfo = ""
    for disk in computer.Win32_DiskDrive():
        diskinfo += f"**Disk Drive**: {disk.Model} ({int(disk.Size) / (1024 ** 3):.2f} GB)\n"

    #get the total amount of ram
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    ostype = os.name
    if ostype == "nt":
        ostype = "windows"
    osname = f"**Operating system**: {ostype}"

    #list of everything
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
        
bot.run(TOKEN)
