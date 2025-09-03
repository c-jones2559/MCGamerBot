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

@bot.command(help="Echos back the message after the command")
async def echo(ctx, *, arg):
    print(f"Echo triggered.")
    await ctx.send(arg)

@bot.command(help="Echos back the message after the command in upper case")
async def upper(ctx, *, arg):
    print(f"Upper triggered.")
    await ctx.send(arg.upper())

@bot.command(help="Echos back the message after the command in lower case")
async def lower(ctx, *, arg):
    print(f"Lower triggered.")
    await ctx.send(arg.lower())

@bot.command(help="Echos back the message after the command in title case")
async def title(ctx, *, arg):
    print(f"Title triggered.")
    newMessage = ""
    for word in arg.split():
        word = word[0].upper() + word[1:].lower()
        newMessage += word + " "
    await ctx.send(newMessage)

@bot.command(help="Sends a link to my cool site")
async def site(ctx):
    print(f"Site triggered.")
    await ctx.send("Doesn't exist yet sorry but it might one day!")

@bot.command(help="Gives details about the bot")
async def info(ctx):
    print(f"Info triggered.")
    mention = f"<@432316900735713290>"
    embed = discord.Embed(title="MC Gamer Bot", description=f"A bot by {mention}", color=discord.Color.blue())
    embed.add_field(name="Email", value="christopher.jones2559@gmail.com", inline=False)
    embed.add_field(name="Version", value="0.1.0", inline=False)
    embed.add_field(name="Last updated", value="03/09/2025", inline=False)
    await ctx.send(embed=embed)

bot.remove_command("help")  # remove the default help so it can be replaced
@bot.command(help="Shows this message")
async def help(ctx):
    print(f"Help triggered.")
    embed = discord.Embed(title="Help", description="Here are the commands", color=discord.Color.blurple())
    for cmd in bot.commands:
        embed.add_field(name=f"!{cmd.name}", value=cmd.help or "No description", inline=False)
    await ctx.send(embed=embed)



# Load token and run
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)