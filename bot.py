import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#startup
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(1412831975147962472)
    await channel.send("Hey gamers!")

#logging
def log_command(command_name, ctx):
    guild_name = "DMs" if ctx.guild is None else ctx.guild.name
    print(f"{ctx.author} triggered {command_name} in {guild_name}.")

#ping
@bot.command(help="Sends pong")
async def ping(ctx):
    log_command("ping", ctx)
    await ctx.send("pong!")

#echo
@bot.command(help="Sends back the message after the command")
async def echo(ctx, *, arg):
    log_command("echo", ctx)
    await ctx.send(arg)

#say
@bot.command(help="Sends back the message after the command and deletes the original message")
async def say(ctx, *, arg):
    log_command("say", ctx)
    await ctx.message.delete()
    await ctx.send(arg)

#upper
@bot.command(help="Sends back the message after the command in upper case")
async def upper(ctx, *, arg):
    log_command("upper", ctx)
    await ctx.send(arg.upper())

#lower
@bot.command(help="Sends back the message after the command in lower case")
async def lower(ctx, *, arg):
    log_command("lower", ctx)
    await ctx.send(arg.lower())

#title
@bot.command(help="Sends back the message after the command in title case")
async def title(ctx, *, arg):
    log_command("title", ctx)
    newMessage = ""
    for word in arg.split():
        word = word[0].upper() + word[1:].lower()
        newMessage += word + " "
    await ctx.send(newMessage)

#site
@bot.command(help="Sends a link to my cool site")
async def site(ctx):
    log_command("site", ctx)
    await ctx.send("Doesn't exist yet sorry but it might one day!")

#info
@bot.command(help="Sends details about the bot")
async def info(ctx):
    log_command("info", ctx)
    mention = f"<@432316900735713290>"
    embed = discord.Embed(title="MC Gamer Bot", description=f"A bot by {mention}", colour=discord.Colour.blurple())
    embed.add_field(name="Email", value="christopher.jones2559@gmail.com", inline=False)
    embed.add_field(name="Version", value="0.1.0", inline=False)
    embed.add_field(name="Last updated", value="04/09/2025", inline=False)
    await ctx.send(embed=embed)

#roll
@bot.command(help="Sends a random number from 1 — input")
async def roll(ctx, arg: int):
    log_command("roll", ctx)
    if arg < 1:
        await ctx.send("Please provide an integer greater than 0.")
    else:
        result = random.randint(1, arg)
        if result == arg:
            await ctx.send(f"{result}! Nice!")
        elif result == 1:
            await ctx.send(f"{result}. Unlucky!")
        else:
            await ctx.send(f"{result}.")

#help
bot.remove_command("help")  # remove the default help so it can be replaced
@bot.command(help="Shows this message")
async def help(ctx):
    log_command("help", ctx)
    embed = discord.Embed(title="Help", colour=discord.Colour.blurple())

    commandsSorted = sorted(bot.commands, key=lambda c: c.name)  # Sort commands alphabetically
    for cmd in commandsSorted:
        if cmd.name == "help":
            pass # help goes at the end of help
        else:
            embed.add_field(name=f"!{cmd.name}", value=cmd.help or "No description", inline=False)
    embed.add_field(name=f"!help", value="Shows this message", inline=False)
    await ctx.send(embed=embed)

#error
@bot.event
async def on_command_error(ctx, error):
    log_command("error", ctx)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    else:
        await ctx.send("An error occurred while processing the command.")
        print(f"Error: {error}")

#token and run
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)