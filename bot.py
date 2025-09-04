import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(1412831975147962472)
    await channel.send("Hey gamers!")

def log_command(command_name, ctx):
    guild_name = "DMs" if ctx.guild is None else ctx.guild.name
    print(f"{ctx.author} triggered {command_name} in {guild_name}.")

@bot.command(help="Responds with pong")
async def ping(ctx):
    log_command("ping", ctx)
    await ctx.send("pong!")

@bot.command(help="Echos back the message after the command")
async def echo(ctx, *, arg):
    log_command("echo", ctx)
    await ctx.send(arg)

@bot.command(help="Echos back the message after the command in upper case")
async def upper(ctx, *, arg):
    log_command("upper", ctx)
    await ctx.send(arg.upper())

@bot.command(help="Echos back the message after the command in lower case")
async def lower(ctx, *, arg):
    log_command("lower", ctx)
    await ctx.send(arg.lower())

@bot.command(help="Echos back the message after the command in title case")
async def title(ctx, *, arg):
    log_command("title", ctx)
    newMessage = ""
    for word in arg.split():
        word = word[0].upper() + word[1:].lower()
        newMessage += word + " "
    await ctx.send(newMessage)

@bot.command(help="Sends a link to my cool site")
async def site(ctx):
    log_command("site", ctx)
    await ctx.send("Doesn't exist yet sorry but it might one day!")

@bot.command(help="Gives details about the bot")
async def info(ctx):
    log_command("info", ctx)
    mention = f"<@432316900735713290>"
    embed = discord.Embed(title="MC Gamer Bot", description=f"A bot by {mention}", colour=discord.Colour.blurple())
    embed.add_field(name="Email", value="christopher.jones2559@gmail.com", inline=False)
    embed.add_field(name="Version", value="0.1.0", inline=False)
    embed.add_field(name="Last updated", value="03/09/2025", inline=False)
    await ctx.send(embed=embed)

bot.remove_command("help")  # remove the default help so it can be replaced
@bot.command(help="Shows this message")
async def help(ctx):
    log_command("help", ctx)
    embed = discord.Embed(title="Help", description="Here are the commands", colour=discord.Colour.blurple())
    for cmd in bot.commands:
        embed.add_field(name=f"!{cmd.name}", value=cmd.help or "No description", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    log_command("error", ctx)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    else:
        await ctx.send("An error occurred while processing the command.")
        print(f"Error: {error}")

# Load token and run
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)