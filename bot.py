import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#startup
@bot.event
async def on_ready():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} Logged in as {bot.user}.")
    channel = bot.get_channel(1412831975147962472)
    await channel.send("Hey gamers!")

#logging
def log_command(command_name, ctx, arg=None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guild_name = "DMs" if ctx.guild is None else ctx.guild.name
    channel_name = "" if ctx.guild is None else f"{ctx.channel.name} of "
    arg_name = "" if arg is None else f" with argument \"{arg}\""

    print(f"{current_time} {ctx.author} triggered {command_name} in {channel_name}{guild_name}{arg_name}.")



#ping
@bot.command(help="Sends pong.", usage = "!ping")
async def ping(ctx):
    log_command("ping", ctx)
    await ctx.send("pong!")

#echo
@bot.command(help="Sends back the message after the command.", usage = "!echo <message>")
async def echo(ctx, *, arg):
    log_command("echo", ctx, arg)
    await ctx.send(arg)

#say
@bot.command(help="Sends back the message after the command and deletes your message.", usage = "!say <message>")
async def say(ctx, *, arg):
    log_command("say", ctx, arg)
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server. Maybe use !echo instead?")
        return
    await ctx.message.delete()
    await ctx.send(arg)

#upper
@bot.command(help="Sends back the message after the command in upper case.", usage = "!upper <message>")
async def upper(ctx, *, arg):
    log_command("upper", ctx, arg)
    await ctx.send(arg.upper())

#lower
@bot.command(help="Sends back the message after the command in lower case.", usage = "!lower <message>")
async def lower(ctx, *, arg):
    log_command("lower", ctx, arg)
    await ctx.send(arg.lower())

#title
@bot.command(help="Sends back the message after the command in title case.", usage = "!title <message>")
async def title(ctx, *, arg):
    log_command("title", ctx, arg)
    newMessage = ""
    for word in arg.split():
        word = word[0].upper() + word[1:].lower()
        newMessage += word + " "
    await ctx.send(newMessage)

#site
@bot.command(help="Sends a link to my cool site.", usage = "!site")
async def site(ctx):
    log_command("site", ctx)
    await ctx.send("Doesn't exist yet sorry but it might one day!")

#info
@bot.command(help="Sends details about the bot.", usage = "!info")
async def info(ctx):
    log_command("info", ctx)
    mention = f"<@432316900735713290>"
    embed = discord.Embed(title="MC Gamer Bot", description=f"A bot by {mention}", colour=discord.Colour.blurple())
    embed.add_field(name="Email", value="christopher.jones2559@gmail.com", inline=False)
    embed.add_field(name="Version", value="0.1.0", inline=False)
    embed.add_field(name="Last updated", value="04/09/2025", inline=False)
    await ctx.send(embed=embed)

#invite
@bot.command(help="Sends a link for you to add the bot to your server.", usage = "!invite")
async def invite(ctx):
    log_command("invite", ctx)
    await ctx.send("https://bit.ly/4mGvKZb")

#roll
@bot.command(help="Sends a random number from 1 to a given value.", usage = "!roll <number>")
async def roll(ctx, arg: int):
    log_command("roll", ctx, arg)
    if arg < 1:
        await ctx.send("Please provide an integer greater than 0.")
    else:
        result = random.randint(1, arg)
        if result == arg:
            await ctx.send(f"{result}! Nice!")
        elif result == 1:
            await ctx.send(f"{result}! Unlucky!")
        else:
            await ctx.send(f"{result}.")

#rolle
@bot.command(help="Sends a random number from 1 to a given value. (but embed :O)", usage = "!rolle <number>")
async def rolle(ctx, arg: int):
    log_command("rolle", ctx, arg)
    embed = discord.Embed(title=f"Roll {arg}", colour=discord.Colour.blurple())
    if arg < 1:
        await ctx.send("Please provide an integer greater than 0.")
    else:
        result = random.randint(1, arg)
        if result == arg:
            embed.description = f"{result}! Nice!"
        elif result == 1:
            embed.description = f"{result}! Unlucky!"
        else:
            embed.description = f"{result}!"
        await ctx.send(embed=embed)

#quote
@bot.command(help="Sends a random quote from Morgan Pritchard.", usage = "!quote")
async def quote(ctx):
    log_command("quote", ctx)
    with open("quotes.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    if not lines:
        await ctx.send("No quotes found.")
        return
    quote = random.choice(lines).strip()
    await ctx.send(quote)

#schedule
@bot.command(help="Sends a message to a given channel at a given time.", usage = "!schedule <message> <minutes_from_now> <channel_id>")
async def schedule(ctx, arg, minutes_from_now: int = 0, channel_id: int = 0):
    if channel_id == 0:
        channel_id = ctx.channel.id
        print(channel_id)
    log_command("schedule", ctx, f"{arg} {channel_id} {minutes_from_now}")
    if minutes_from_now < 0:
        await ctx.send("Please provide a non-negative integer for minutes from now.")
        return
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("I couldn't find that channel. Please make sure I have access to it and that the ID is correct. (Schedule doesn't work in DMs.)")
        return
    await ctx.send(f"Message scheduled to be sent in {minutes_from_now} minute(s).")
    await discord.utils.sleep_until(datetime.now() + timedelta(minutes=minutes_from_now))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} Sending scheduled message to channel ID {channel_id}.")
    await channel.send(arg)

#DM
@bot.command(help="Sends a message to someone for you.", usage = "!DM <user> <message>")
async def DM(ctx, userID: int, arg):
    log_command("DM", ctx, f"{userID} {arg}")
    if userID == 1412830085429330142 :
        await ctx.send("I can't DM myself!")
        return
    user = bot.get_user(userID)
    if user is None:
        user = await bot.fetch_user(userID)
    if user is None:
        await ctx.send("I couldn't find that user. Please make sure the ID is correct. I can't DM people who haven't shared a server with me or who have DMs off.")
        return
    await user.send(arg)
    await ctx.send(f"Message sent to {user}.")

#help
bot.remove_command("help")  #remove the default help so it can be replaced
@bot.command(help="Shows this message.", usage = "!help")
async def help(ctx):
    log_command("help", ctx)
    embed = discord.Embed(title="Help", colour=discord.Colour.blurple())

    commandsSorted = sorted(bot.commands, key=lambda c: c.name)  #sort commands alphabetically
    for cmd in commandsSorted:
        if cmd.name == "help":
            pass #help goes at the end of help
        else:
            embed.add_field(name=f"{cmd.usage}", value=cmd.help or "No description", inline=False)
    embed.add_field(name=f"!help", value="Shows this message", inline=False)
    await ctx.send(embed=embed)

#error
@bot.event
async def on_command_error(ctx, error):
    log_command("error", ctx)
    print(f"                    Error: {error}")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument type. Please check the command usage.")
    else:
        await ctx.send("An error occurred while processing the command.")
        

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