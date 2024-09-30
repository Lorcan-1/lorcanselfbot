# Lorcan Selfbot

This is a selfbot for Discord, developed using `discord.py-self`. This selfbot includes various commands for managing a Discord server, finding information online, automating messages and more. Note that using selfbots in Discord is against Terms of Service, and your account may be banned for using one.

## Features

- **`spam [Number] [message]`**: Sends a message a specified number of times.
- **`meow`**: Sends an ASCII art of a cat.
- **`deletechannels`**: Deletes all channels in the server.
- **`commands`**: Lists all available commands.
- **`lookup [TARGET_IP]`**: Looks up information for an IP address.
- **`ban [member] [reason]`**: Bans a user with an optional reason.
- **`kick [member]`**: Kicks a user from the server.
- **`unban [member]`**: Unbans a user.
- **`purge [amount]`**: Deletes a specified number of messages.
- **`createchannels [number] [channel_name]`**: Creates a specified number of text channels with a given name.
- **`massban [reason]`**: Bans all members in the server with a reason.
- **`webhookmessage [message] [user_name]`**: Sends a message via webhook with a specified username.
- **`webhookspam [amount] [message]`**: Spams a message a specified number of times using webhooks.
- **`nuke`**: Deletes all channels, creates new channels, deletes all roles, creates new roles, and bans all members.
- **`spamroles [number] [role_name]`**: Creates a specified number of roles with a given name.
- **`search [query]`**: Searches Google for a query.
- **`ascii [message]`**: Converts a message to ASCII art.
- **`lastraid [username]`**: Fetches the most recent raid completion for a Destiny 2 user.
- **`math [expression]`**: Evaluates a mathematical expression.
- **`weather [city_name]`**: Provides the current weather for a specified city.
- **`ipping [TARGET_IP]`**: Pings an IP address to check connectivity
- **`pcinfo`**: Displays the pc components of the computer hosting the selfbot
- **`time`**: Sends the current time formatted  
- **`generatenitro`**: Sends a random discord.gift link highly unlikely to ever be an actual link
- **`dictionary [word]`**: searches a word in the dictionary
- **`nitro sniper`**: reads messages for nitro gift links and redeems them for you
- **`qrcodegen [link]`**: generates a qr code for a given url
- **`activity [activity name]`**: changes your discord activity
- **`message logging`**: logs deleted messages to the terminal (can be turned off by setting "logging" to false)



## Description

This Lorcan Selfbot, developed using `discord.py-self`, is designed to automate and manage various tasks within a Discord server. It provides a range of commands for server administration, including managing channels, roles, and users, as well as performing various automated actions like spamming messages or creating webhooks. Additionally, it includes commands for interacting with the Bungie API to fetch Destiny 2 raid completion data.

**Note**: Using selfbots violates Discord's Terms of Service and can lead to account suspension or banning.

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/benson7618/Lorcanselfbot.git
    
    cd Lorcanselfbot
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `config.json` file** in the same directory as the script. This file should contain your Discord bot token in the following format:

    ```json
    {
        "TOKEN": "your_discord_token"
    }
    ```

   If the `config.json` file does not exist, the bot will prompt you to enter your token and will create the file for you automatically.

4. **Run the bot**:

    ```bash
    python sbmain.py
    ```
    
## Notes

- Ensure you have the required permissions to execute certain commands.
- Be cautious with commands like `nuke` and `massban` as they can significantly impact your server.
- Selfbots are against Discord's Terms of Service, and using them may result in account suspension.

## Repository

You can find the repository for this project at: [repository]([https://github.com/benson7618/Lorcanselfbot.git)]

-Lawcan
