import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
GUILD_ID = discord.Object(id=1412831973726224556)

#startup
@bot.event
async def on_ready():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} Logged in as {bot.user}.")
    try:
        synced = await bot.tree.sync(guild=GUILD_ID)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    channel = bot.get_channel(1412831975147962472)
    await channel.send("Hey gamers!")

#logging
def log_command(command_name, interaction, arg=None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guild_name = "DMs" if interaction.guild is None else interaction.guild.name
    channel_name = "" if interaction.guild is None else f"{interaction.channel.name} of "
    arg_name = "" if arg is None else f" with argument \"{arg}\""

    print(f"{current_time} {interaction.user} triggered {command_name} in {channel_name}{guild_name}{arg_name}.")

#ping
@bot.tree.command(name="ping", description="Sends pong.", guild=GUILD_ID)
async def ping(interaction: discord.Interaction):
    log_command("ping", interaction)
    await interaction.response.send_message("pong!")

#echo
@bot.tree.command(name = "echo", description="Sends back the message after the command.", guild=GUILD_ID)
async def echo(interaction, *, message: str):
    log_command("echo", interaction, message)
    await interaction.response.send_message(message)

#say
@bot.tree.command(description="Sends back the message after the command and deletes your message.", name="say", guild=GUILD_ID)
async def say(interaction, *, message: str):
    log_command("say", interaction, message)
    if interaction.guild is None:
        await interaction.response.send_message("This command can only be used in a server. Maybe use /echo instead?")
        return
    await interaction.channel.send(message)
    await interaction.response.send_message("Message sent.", ephemeral=True)
    

#upper
@bot.tree.command(description="Sends back the message after the command in upper case.", name="upper", guild=GUILD_ID)
async def upper(interaction, *, message: str):
    log_command("upper", interaction, message)
    await interaction.response.send_message(message.upper())

#lower
@bot.tree.command(description="Sends back the message after the command in lower case.", name="lower", guild=GUILD_ID)
async def lower(interaction, *, message: str):
    log_command("lower", interaction, message)
    await interaction.response.send_message(message.lower())

#title
@bot.tree.command(description="Sends back the message after the command in title case.", name="title", guild=GUILD_ID)
async def title(interaction, *, message: str):
    log_command("title", interaction, message)
    newMessage = ""
    for word in message.split():
        word = word[0].upper() + word[1:].lower()
        newMessage += word + " "
    await interaction.response.send_message(newMessage)

#site
@bot.tree.command(description="Sends a link to my cool site.", name="site", guild=GUILD_ID)
async def site(interaction):
    log_command("site", interaction)
    await interaction.response.send_message("Doesn't exist yet sorry but it might one day!")

#info
@bot.tree.command(description="Sends details about the bot.", name="info", guild=GUILD_ID)
async def info(interaction):
    log_command("info", interaction)
    mention = f"<@432316900735713290>"
    embed = discord.Embed(title="MC Gamer Bot", description=f"A bot by {mention}", colour=discord.Colour.blurple())
    embed.add_field(name="Email", value="christopher.jones2559@gmail.com", inline=False)
    embed.add_field(name="Version", value="0.1.0", inline=False)
    embed.add_field(name="Last updated", value="04/09/2025", inline=False)
    await interaction.response.send_message(embed=embed)

#invite
@bot.tree.command(description="Sends a link for you to add the bot to your server.", name="invite", guild=GUILD_ID)
async def invite(interaction):
    log_command("invite", interaction)
    await interaction.response.send_message("https://bit.ly/4mGvKZb")

#roll
@bot.tree.command(description="Sends a random number from 1 to a given value.", name="roll", guild=GUILD_ID)
async def roll(interaction, max: int):
    log_command("roll", interaction, max)
    if max < 1:
        await interaction.response.send_message("Please provide an integer greater than 0.")
    else:
        result = random.randint(1, max)
        if result == max:
            await interaction.response.send_message(f"{result}! Nice!")
        elif result == 1:
            await interaction.response.send_message(f"{result}! Unlucky!")
        else:
            await interaction.response.send_message(f"{result}!")

#rolle
@bot.tree.command(description="Sends a random number from 1 to a given value. (but embed :O)", name="rolle", guild=GUILD_ID)
async def rolle(interaction, arg: int):
    log_command("rolle", interaction, arg)
    embed = discord.Embed(title=f"Roll {arg}", colour=discord.Colour.blurple())
    if arg < 1:
        await interaction.response.send_message("Please provide an integer greater than 0.")
    else:
        result = random.randint(1, arg)
        if result == arg:
            embed.description = f"{result}! Nice!"
        elif result == 1:
            embed.description = f"{result}! Unlucky!"
        else:
            embed.description = f"{result}!"
        await interaction.response.send_message(embed=embed)
    component = discord.components.Button(label="Roll Again", style=discord.ButtonStyle.primary)

#quote
@bot.tree.command(description="Sends a random quote from Morgan Pritchard.", name="quote", guild=GUILD_ID)
async def quote(interaction):
    log_command("quote", interaction)
    with open("quotes.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    if not lines:
        await interaction.response.send_message("No quotes found.")
        return
    quote = random.choice(lines).strip()
    await interaction.response.send_message(quote)

#schedule
@bot.tree.command(description="Sends a message to a given channel at a given time.", name="schedule", guild=GUILD_ID)
async def schedule(interaction, message: str, minutes_from_now: int = 0, channel_id: str = "0"):
    channel_id = int(channel_id)
    if channel_id == 0:
        channel_id = interaction.channel.id
        print(channel_id)
    log_command("schedule", interaction, f"{message} {channel_id} {minutes_from_now}")
    if minutes_from_now < 0:
        await interaction.response.send_message("Please provide a non-negative integer for minutes from now.")
        return
    channel = bot.get_channel(channel_id)
    if channel is None:
        await interaction.response.send_message("I couldn't find that channel. Please make sure I have access to it and that the ID is correct. (Schedule doesn't work in DMs.)")
        return
    await interaction.response.send_message(f"Message scheduled to be sent in {minutes_from_now} minute(s).")
    await discord.utils.sleep_until(datetime.now() + timedelta(minutes=minutes_from_now))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} Sending {interaction.user}'s scheduled message to channel ID {channel_id}.")
    await channel.send(message)

#dm
async def findUser(interaction, *, username):
    # Search for a member in the current guild by username (case-insensitive)
    member = discord.utils.find(lambda m: m.name.lower() == username.lower(), interaction.guild.members)
    if member:
        return member.id
    return None
@bot.tree.command(description="Sends a message to someone for you.", name="dm", guild=GUILD_ID)
async def dm(interaction, userid: str, *, arg: str):
    log_command("dm", interaction, f"{userid} {arg}")
    
    if not userid.isdigit():
        if interaction.guild is None:
            await interaction.response.send_message("Please provide a user ID when using this command in DMs.")
            return
        userid = await findUser(interaction, username=userid)
        if userid is None:
            await interaction.response.send_message("I couldn't find that user. Please make sure the username is correct. I can only search for usernames in this server.")
            return
        #print(f"Found user ID: {userID}")

    if userid == 1412830085429330142:
        await interaction.response.send_message("I can't DM myself!")
        return
    userid = int(userid)

    user = bot.get_user(userid) #check cache first to limit API calls
    if user is None:
        user = await bot.fetch_user(userid)
    if user is None:
        await interaction.response.send_message("I couldn't find that user. Please make sure the ID is correct. I can't DM people who haven't shared a server with me or who have DMs off.")
        return
    await user.send(arg)
    await interaction.response.send_message(f"Message sent to {user}.")

#help
bot.remove_command("help")  #remove the default help so it can be replaced
@bot.tree.command(description="Sends a help message.", name="help", guild=GUILD_ID)
async def help(interaction):
    log_command("help", interaction)
    embed = discord.Embed(title="Help", colour=discord.Colour.blurple())

    commandsSorted = sorted(bot.tree.get_commands(guild=GUILD_ID), key=lambda c: c.name)  #sort commands alphabetically
    for cmd in commandsSorted:
        if cmd.name == "help":
            pass #help goes at the end of help
        else:
            embed.add_field(name=f"/{cmd.name}", value=cmd.description or "No description", inline=False)
    embed.add_field(name=f"/help", value="Sends this message.", inline=False)
    await interaction.response.send_message(embed=embed)

#error
@bot.event
async def on_command_error(interaction, error):
    #log_command("error", ctx)
    print(f"                    Error: {error}")
    if isinstance(error, commands.CommandNotFound):
        await interaction.response.send_message("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message("Missing required argument. Please check the command usage.")
    elif isinstance(error, commands.BadArgument):
        await interaction.response.send_message("Invalid argument type. Please check the command usage.")
    else:
        await interaction.response.send_message("An error occurred while processing the command.")

#log dms
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} DM from {message.author}: {message.content}")
    
    await bot.process_commands(message)

#token and run
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)