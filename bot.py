import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta, time, timezone

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
        synced = await bot.tree.sync()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    #start daily subscriptions
    sendSubscriptions.start()
    channel = bot.get_channel(1412831975147962472)
    await channel.send("Hey gamers!")

#logging
def log_command(command_name, interaction, arg=None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if interaction is None:
        output = f"{current_time} Scheduled task {command_name} ran."
        print(output)
        with open("/app/data/bot.log", "a", buffering=1) as f:
            f.write(f"{output}\n")
        return
    guild_name = "DMs" if interaction.guild is None else interaction.guild.name
    channel_name = "" if interaction.guild is None else f"{interaction.channel.name} of "
    arg_name = "" if arg is None else f" with argument \"{arg}\""

    output = f"{current_time} {interaction.user} triggered {command_name} in {channel_name}{guild_name}{arg_name}."
    print(output)
    with open("/app/data/bot.log", "a", buffering=1) as f:
        f.write(f"{output}\n")


@bot.tree.command(name="ping", description="Sends pong and latency.", guild = GUILD_ID)
async def ping(interaction: discord.Interaction):
    log_command("ping", interaction)

    before = datetime.now()
    # Send the message and grab the actual Message object
    message = await interaction.response.send_message("Pong!")

    # Discord stores message.created_at as an aware datetime in UTC
    latency = (message.created_at - before).total_seconds() * 1000

    await interaction.response.edit_message(content=f"Pong! `{latency:.2f}ms`")

#echo
@bot.tree.command(name="echo", description="Sends back the message after the command.")
async def echo(interaction, *, message: str):
    log_command("echo", interaction, message)
    await interaction.response.send_message(message)

#say
@bot.tree.command(description="Sends back the message after the command and deletes your message.", name="say")
async def say(interaction, *, message: str):
    log_command("say", interaction, message)
    if interaction.guild is None:
        await interaction.response.send_message("This command can only be used in a server. Maybe use /echo instead?")
        return
    await interaction.channel.send(message)
    await interaction.response.send_message("Message sent.", ephemeral=True)
    

#upper
@bot.tree.command(description="Sends back the message after the command in upper case.", name="upper")
async def upper(interaction, *, message: str):
    log_command("upper", interaction, message)
    await interaction.response.send_message(message.upper())

#lower
@bot.tree.command(description="Sends back the message after the command in lower case.", name="lower")
async def lower(interaction, *, message: str):
    log_command("lower", interaction, message)
    await interaction.response.send_message(message.lower())

#title
@bot.tree.command(description="Sends back the message after the command in title case.", name="title")
async def title(interaction, *, message: str):
    log_command("title", interaction, message)
    newMessage = ""
    for word in message.split():
        word = word[0].upper() + word[1:].lower()
        newMessage += word + " "
    await interaction.response.send_message(newMessage)

#site
@bot.tree.command(description="Sends a link to my cool site.", name="site")
async def site(interaction):
    log_command("site", interaction)
    await interaction.response.send_message("https://cjones.cymru")

#info
@bot.tree.command(description="Sends details about the bot.", name="info")
async def info(interaction):
    log_command("info", interaction)
    mention = f"<@432316900735713290>"
    embed = discord.Embed(title="MC Gamer Bot", description=f"A bot by {mention}", colour=discord.Colour.blurple())
    embed.add_field(name="Email", value="christopher.jones2559@gmail.com", inline=False)
    embed.add_field(name="Version", value="0.1.0", inline=False)
    embed.add_field(name="Last updated", value="04/09/2025", inline=False)
    await interaction.response.send_message(embed=embed)

#invite
@bot.tree.command(description="Sends a link for you to add the bot to your server.", name="invite")
async def invite(interaction):
    log_command("invite", interaction)
    await interaction.response.send_message("https://bot.cjones.cymru")

#roll
class RollView(discord.ui.View):
    def __init__(self, max: int):
        super().__init__()
        self.max = max
    
    @discord.ui.button(label="Roll Again", style=discord.ButtonStyle.primary)
    async def roll_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        max=self.max
        log_command("reroll", interaction, max)
        result = random.randint(1, max)
        if result == max:
            await interaction.response.send_message(f"{result}! Nice!")
        elif result == 1:
            await interaction.response.send_message(f"{result}! Unlucky!")
        else:
            await interaction.response.send_message(f"{result}!")

@bot.tree.command(description="Sends a random number from 1 to a given value.", name="roll")
async def roll(interaction, max: int):
    log_command("roll", interaction, max)
    if max < 1:
        await interaction.response.send_message("Please provide an integer greater than 0.")
    else:
        result = random.randint(1, max)
        if result == max:
            await interaction.response.send_message(f"{result}! Nice!", view=RollView(max))
        elif result == 1:
            await interaction.response.send_message(f"{result}! Unlucky!", view=RollView(max))
        else:
            await interaction.response.send_message(f"{result}!", view=RollView(max))
    

#rolle
@bot.tree.command(description="Sends a random number from 1 to a given value. (but embed :O)", name="rolle")
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
@bot.tree.command(description="Sends a random quote from Morgan Pritchard.", name="quote")
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
@bot.tree.command(description="Sends a message to a given channel at a given time.", name="schedule")
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
@bot.tree.command(description="Sends a message to someone for you after searching for them by id or username.", name="dm")
async def dm(interaction, username: str, *, message: str):
    log_command("dm", interaction, f"{username} {message}")
    userid=username
    if not userid.isdigit():
        if interaction.guild is None:
            await interaction.response.send_message("Please provide a user ID when using this command in DMs.", ephemeral=True)
            return
        userid = await findUser(interaction, username=userid)
        if userid is None:
            await interaction.response.send_message("I couldn't find that user. Please make sure the username is correct. I can only search for usernames in this server.", ephemeral=True)
            return
        #print(f"Found user ID: {userID}")

    if userid == 1412830085429330142:
        await interaction.response.send_message("I can't DM myself!", ephemeral=True)
        return
    userid = int(userid)

    user = bot.get_user(userid) #check cache first to limit API calls
    if user is None:
        user = await bot.fetch_user(userid)
    if user is None:
        await interaction.response.send_message("I couldn't find that user. Please make sure the ID is correct. I can't DM people who haven't shared a server with me or who have DMs off.", ephemeral=True)
        return
    await user.send(message)
    await interaction.response.send_message(f"Message sent to {user}.", ephemeral=True)
    
#dmuser
class UserSelect(discord.ui.UserSelect):
    def __init__(self, message):
        self.message = message
        super().__init__(placeholder="Pick a user...", min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        picked_user = self.values[0]
        #await interaction.followup.send_message(f"You picked: {picked_user.mention}", ephemeral=True)
        if picked_user.id == 1412830085429330142:
            await interaction.followup.send("I can't DM myself!", ephemeral=True)
            return
       
        await picked_user.send(self.message)
        await interaction.followup.send(f"Message sent to {picked_user.mention}.", ephemeral=True)

class MyView(discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.add_item(UserSelect(message))

@bot.tree.command(description="Sends a message to someone for you after picking them from a dropdown list.", name="dmuser")
async def dmuser(interaction, message: str):
    log_command("dmuser", interaction, message)
    if interaction.guild is None:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return
    await interaction.response.send_message("Select a user to DM:", view=MyView(message), ephemeral=True)

startTime = datetime.now()
#online
@bot.tree.command(description="Sends how long the bot has been online.", name="online")
async def online(interaction):
    log_command("online", interaction)
    delta = datetime.now() - startTime
    total_seconds = int(delta.total_seconds())
    months, remainder = divmod(total_seconds, 2592000)  # 30*24*60*60
    days, remainder = divmod(remainder, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if months:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    uptime_str = ", ".join(parts)
    await interaction.response.send_message(f"I have been online for {uptime_str}.")


#tictactoe


class Board:
    def __init__(self, difficulty):
        self.board = ["." for _ in range(9)]  # A list to hold the board state
        self.difficulty = difficulty  # 0=Noob, 1=Pro, 2=Hacker, 3=human
    
    def return_board(self):
        boardStr = ""
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            boardStr += ("| " + " | ".join(row) + " |")
            boardStr += "\n"
        return boardStr
    
    def checkWin(self):
        # Check rows, columns, and diagonals for a win
        for row in range(3):
            if self.board[row*3] == self.board[row*3 + 1] == self.board[row*3 + 2] != ".":
                if self.board[row*3] == "X":
                    return 1
                return 2
        for col in range(3):
            if self.board[col] == self.board[col + 3] == self.board[col + 6] != ".":
                if self.board[col] == "X":
                    return 1
                return 2
        if self.board[0] == self.board[4] == self.board[8] != ".":
            if self.board[4] == "X":
                return 1
            return 2
        if self.board[2] == self.board[4] == self.board[6] != ".":
            if self.board[4] == "X":
                return 1
            return 2
        for i in range(9):
            if self.board[i] == ".":
                return 0
        return -1  # Draw
    
    def updateWin(self):
        for row in range(3):
            if self.board[row*3] == self.board[row*3 + 1] == self.board[row*3 + 2] != ".":
                if self.board[row*3] == "X":
                    self.board[row*3] = "~~X~~"
                    self.board[row*3+1] = "~~X~~"
                    self.board[row*3+2] = "~~X~~"
                    return
                elif self.board[row*3] == "O":
                    self.board[row*3] = "~~O~~"
                    self.board[row*3+1] = "~~O~~"
                    self.board[row*3+2] = "~~O~~"
                    return
        for col in range(3):
            if self.board[col] == self.board[col + 3] == self.board[col + 6] != ".":
                if self.board[col] == "X":
                    self.board[col] = "~~X~~"
                    self.board[col+3] = "~~X~~"
                    self.board[col+6] = "~~X~~"
                    return
                elif self.board[col] == "O":
                    self.board[col] = "~~O~~"
                    self.board[col+3] = "~~O~~"
                    self.board[col+6] = "~~O~~"
                    return
        if self.board[0] == self.board[4] == self.board[8] != ".":
            if self.board[4] == "X":
                self.board[0] = "~~X~~"
                self.board[4] = "~~X~~"
                self.board[8] = "~~X~~"
                return
            elif self.board[4] == "O":
                self.board[0] = "~~O~~"
                self.board[4] = "~~O~~"
                self.board[8] = "~~O~~"
                return
        if self.board[2] == self.board[4] == self.board[6] != ".":
            if self.board[4] == "X":
                self.board[2] = "~~X~~"
                self.board[4] = "~~X~~"
                self.board[6] = "~~X~~"
                return
            elif self.board[4] == "O":
                self.board[2] = "~~O~~"
                self.board[4] = "~~O~~"
                self.board[6] = "~~O~~"
                return
    
    def getValue(self, int):
        return self.board[int]
        

class TicTacToeButton(discord.ui.Button):
    def __init__(self, row: int, col: int, board: Board):
        super().__init__(style=discord.ButtonStyle.secondary, label=str(row*3+col+1), row=row, disabled=False if board.board[row*3+col] == "." else True)
        self.row_index = row
        self.col_index = col
        self.board = board

    async def callback(self, interaction: discord.Interaction):
        # You can pass the move to your playGame function here
        #await interaction.response.send_message(
        #    f"You clicked row {self.row_index + 1}, column {self.col_index + 1}!",
        #    ephemeral=True
        #)
        for item in self.view.children:
            item.disabled = True
        self.board.board[self.row_index * 3 + self.col_index] = "X" 
        
        if self.board.checkWin() == 1:
            self.board.updateWin()
            await interaction.response.edit_message(content=f"{self.board.return_board()}\nYou played X", view=self.view)
            await interaction.followup.send("You win! GG!\nNow try a harder difficulty!")
            return
        elif self.board.checkWin() == -1:
            await interaction.response.edit_message(content=f"{self.board.return_board()}\nYou played X", view=self.view)
            await interaction.followup.send("It's a draw! GG!\nRematch?")
            return

        if self.board.difficulty == "Noob":
            playNoob(self.board)
        elif self.board.difficulty == "Pro":
            playPro(self.board)
        elif self.board.difficulty == "Hacker":
            playHacker(self.board)
        elif self.board.difficulty == "God":
            playGod(self.board)
        elif self.board.difficulty == "Human":
            pass
            #await interaction.followup.send("Your opponent's turn. Please wait for them to click a button.")
            #return
        if self.board.checkWin() == 2:
            self.board.updateWin()
        await interaction.response.edit_message(content=f"{self.board.return_board()}\nYou played X\nI played O", view=self.view)
        if self.board.checkWin() == 2:
            await interaction.followup.send("I win! GG!")
            return
        await playGame(interaction, self.board)


class TicTacToeView(discord.ui.View):
    def __init__(self, board: Board):
        super().__init__(timeout=None)
        for row in range(3):
            for col in range(3):
                self.add_item(TicTacToeButton(row, col, board))

#tictactoe
def playNoob(board: Board):
    for i in range(9):
        if board.board[i] == ".":
            break
        elif i == 8: #full board
            return
    i = random.randint(0, 8)
    while board.board[i] != ".":
        i = random.randint(0, 8)
    board.board[i] = "O"
    return     
def playPro(board: Board):
    #check if can win
    for i in range(9):
        if board.board[i] == ".":
            board.board[i] = "O"
            if board.checkWin() == 2:
                return
            board.board[i] = "."
    #check if player can win next turn, block them
    for i in range(9):
        if board.board[i] == ".":
            board.board[i] = "X"
            if board.checkWin() == 1:
                board.board[i] = "O"
                return
            board.board[i] = "."
    #otherwise play Noob
    playNoob(board)
def playHacker(board: Board):
    empty = 0
    for i in range(9):
        if board.board[i] == ".":
            empty += 1
    if empty == 8:
        if board.board[4] == ".":
            board.board[4] = "O"
            return
        else:
            board.board[0] = "O"
            return
    elif empty == 6:
        if board.board[4] == "X":
            if board.board[0] == ".":
                board.board[0] = "O"
                return
            elif board.board[2] == ".":
                board.board[2] = "O"
                return
            elif board.board[6] == ".":
                board.board[6] = "O"
                return
            elif board.board[8] == ".":
                board.board[8] = "O"
                return
        elif (board.board[0] == "X" and board.board[8]) == "X" or (board.board[2] == "X" and board.board[6]) == "X":
            if board.board[1] == ".":
                board.board[1] = "O"
                return
            elif board.board[3] == ".":
                board.board[3] = "O"
                return
            elif board.board[5] == ".":
                board.board[5] = "O"
                return
            elif board.board[7] == ".":
                board.board[7] = "O"
                return
        else:
            playPro(board)
            return
    else:
        playPro(board)
    return
def playGod(board: Board):
    for i in range(9):
        if board.board[i] == ".":
            board.board[i] = "O"
    return

async def playGame(interaction, board: Board): #0=Noob, 1=Pro, 2=Hacker, 3=human
    view = TicTacToeView(board)
    board_str = f"{board.return_board()}\nChoose your move:"
    try:
        await interaction.response.send_message(board_str, view=view)
    except discord.InteractionResponded:
        await interaction.followup.send(board_str, view=view)
    
    #await interaction.response.send_message(board.return_board())

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Noob"),
            discord.SelectOption(label="Pro"),
            discord.SelectOption(label="Hacker"),
            discord.SelectOption(label="God"),
            discord.SelectOption(label="Human", description="Play with a friend"),
        ]
        super().__init__(placeholder="Pick your opponent.", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        #await interaction.response.send_message(f"You picked: {self.values[0]}", ephemeral=True)
        
        if self.values[0] == "Human":
            await interaction.response.send_message("This feature is coming soon!")
            return
        await playGame(interaction, Board(self.values[0]))
        #await interaction.followup.send("This feature is coming soon!")

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

@bot.tree.command(description="Play a game of tic tac toe with another user, or against a bot.", name="tictactoe")
async def tictactoe(interaction):
    log_command("tictactoe", interaction)
    await interaction.response.send_message("Choose an option:", view=DropdownView())

#subscriptions
@tasks.loop(time=time(hour=12, tzinfo=timezone.utc))  # Adjust the time as needed (UTC)
async def sendSubscriptions():
    log_command("sendSubscriptions", None)
    with open("/app/data/subscriptions.txt", "r", encoding="utf-8") as f:
        contents = f.read()
    
    userIDs = contents.split("\n")
    index = int(userIDs[0])
    userIDs = userIDs[1:]
    with open("quotes.txt", "r", encoding="utf-8") as f:
        quotes = f.readlines()
        quote = quotes[index % len(quotes)].strip()
    index += 1
    with open("/app/data/subscriptions.txt", "w", buffering=1) as f:
        contents = str(index) + "\n" + "\n".join(userIDs) + "\n"
        f.write(contents)

    for userID in userIDs:
        if userID == "":
            continue
        userID = int(userID)
        user = bot.get_user(userID) #check cache first to limit API calls
        if user is None:
            user = await bot.fetch_user(userID)
        if user is None:
            continue
        await user.send(f"Quote of the day #{index}:\n{quote}")

#subscribe
@bot.tree.command(description="Subscribes to daily messages.", name="subscribe")
async def subscribe(interaction):
    log_command("subscribe", interaction)
    with open("/app/data/subscriptions.txt", "r", encoding="utf-8") as f:
        contents = f.read()
    if str(interaction.user.id) in contents:
        await interaction.response.send_message("You are already subscribed.")
        return
    with open("/app/data/subscriptions.txt", "a", buffering=1) as f:
        f.write(f"{interaction.user.id}\n")
    await interaction.response.send_message("You have subscribed to daily Morgan Pritchard quotes!\nQuotes are delivered in DMs at 12pm UTC.\nUse /unsubscribe to stop receiving them.")

#unsubscribe
@bot.tree.command(description="Unsubscribes from daily messages.", name="unsubscribe")
async def unsubscribe(interaction):
    log_command("unsubscribe", interaction)
    with open("/app/data/subscriptions.txt", "r", encoding="utf-8") as f:
        contents = f.read()
    if str(interaction.user.id) in contents:
        contents = contents.replace(f"{interaction.user.id}\n", "")
        with open("/app/data/subscriptions.txt", "w", buffering=1) as f:
            f.write(contents)
    await interaction.response.send_message("You have unsubscribed from daily Morgan Pritchard quotes.\nUse /subscribe to subscribe again.")

#broadcast
@bot.tree.command(description="Sends a message out to all subscribers.", name="broadcast")
async def broadcast(interaction, message: str):
    log_command("broadcast", interaction, message)
    if interaction.user.id != 432316900735713290:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    with open("/app/data/subscriptions.txt", "r", encoding="utf-8") as f:
        contents = f.read()
    
    userIDs = contents.split("\n")
    userIDs = userIDs[1:]

    for userID in userIDs:
        if userID == "":
            continue
        userID = int(userID)
        user = bot.get_user(userID) #check cache first to limit API calls
        if user is None:
            user = await bot.fetch_user(userID)
        if user is None:
            continue
        await user.send(message)
    await interaction.response.send_message("Message sent to all subscribers.", ephemeral=True)

#forceSubscriptions
@bot.tree.command(description="Force send the daily message to all subscribers.", name="force_subscriptions")
async def forceSubscriptions(interaction):
    log_command("forceSubscriptions", interaction)
    if interaction.user.id != 432316900735713290:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    with open("/app/data/subscriptions.txt", "r", encoding="utf-8") as f:
        contents = f.read()
    
    userIDs = contents.split("\n")
    index = int(userIDs[0])
    userIDs = userIDs[1:]
    with open("quotes.txt", "r", encoding="utf-8") as f:
        quotes = f.readlines()
        quote = quotes[index % len(quotes)].strip()
    index += 1
    with open("/app/data/subscriptions.txt", "w", buffering=1) as f:
        contents = str(index) + "\n" + "\n".join(userIDs) + "\n"
        f.write(contents)

    for userID in userIDs:
        if userID == "":
            continue
        userID = int(userID)
        user = bot.get_user(userID) #check cache first to limit API calls
        if user is None:
            user = await bot.fetch_user(userID)
        if user is None:
            continue
        await user.send(f"Quote of the day #{index}:\n{quote}")
    await interaction.response.send_message("Message sent to all subscribers.", ephemeral=True)

#view logs
@bot.tree.command(description="Sends recent bot logs to DMs.", name="view_logs")
async def view_logs(interaction):
    log_command("view_logs", interaction)
    if interaction.user.id != 432316900735713290:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    with open("/app/data/bot.log", "r", encoding="utf-8") as f:
        contents = f.read()
    if len(contents) > 1900:
        contents = contents[-1900:] 
        contents = "...\n" + contents
    user = bot.get_user(432316900735713290)
    if user is None:
        user = await bot.fetch_user(432316900735713290)
    if user is None:
        await interaction.response.send_message("I couldn't find that user. Please make sure the ID is correct. I can't DM people who haven't shared a server with me or who have DMs off.", ephemeral=True)
        return
    await user.send(f"```\n{contents}\n```")
    await interaction.response.send_message("Logs sent to your DMs.", ephemeral=True)

#help
bot.remove_command("help")  #remove the default help so it can be replaced
@bot.tree.command(description="Sends a help message.", name="help")
async def help(interaction):
    log_command("help", interaction)
    embed = discord.Embed(title="Help", colour=discord.Colour.blurple())

    commandsSorted = sorted(bot.tree.get_commands(), key=lambda c: c.name)  #sort commands alphabetically
    for cmd in commandsSorted:
        if cmd.name == "help":
            pass #help goes at the end of help
        else:
            embed.add_field(name=f"/{cmd.name}", value=cmd.description or "No description", inline=False)
    embed.add_field(name=f"/help", value="Sends this message.", inline=False)
    await interaction.response.send_message(embed=embed)

#error
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    #log_command("error", ctx)
    print(f"                    Error: {error}")
    if isinstance(error, discord.InteractionResponded):
        await interaction.response.send_message("This interaction has already been responded to.")
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command.")
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("I don't have permission to use this command.")
    else:
        await interaction.response.send_message("An error occurred while processing the command.")

#log dms
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output=f"{current_time} DM from {message.author}: {message.content}"
        print(output)
        with open("/app/data/bot.log", "a", buffering=1) as f:
            f.write(f"{output}\n")
        
        user = bot.get_user(432316900735713290) #check cache first to limit API calls
        if user is None:
            user = await bot.fetch_user(432316900735713290)
        await user.send(f"DM from {message.author.mention} ({message.author.id}):\n{message.content}")
    
    await bot.process_commands(message)



#token and run
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)