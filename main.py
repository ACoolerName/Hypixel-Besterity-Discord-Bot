from get_userdata import savedata
from discord.ext import commands, tasks
from sort_top import *
import dailytask
import weeklytask
import discord
import discord.ui
import os
import sys
import requests
import datetime
import time

botversion = "Release 1.0"

day = 0
week = 0

currenttime = datetime.datetime.now()
unixtime = int(time.mktime(currenttime.timetuple()))
datarefreshtime = unixtime
dailyrefreshtime = unixtime
weeklyrefreshtime = unixtime

# Button booleans
def resetrow1buttons():
    global t1buttonpressed
    global t2buttonpressed
    global allbuttonpressed
    t1buttonpressed = False
    t2buttonpressed = False
    allbuttonpressed = False

def resetrow2buttons():
    global dailybuttonpressed
    global weeklybuttonpressed
    global totalbuttonpressed
    dailybuttonpressed = False
    weeklybuttonpressed = False
    totalbuttonpressed = False

def resetallbuttons():
    global t1buttonpressed
    global t2buttonpressed
    global allbuttonpressed
    t1buttonpressed = False
    t2buttonpressed = False
    allbuttonpressed = False
    global dailybuttonpressed
    global weeklybuttonpressed
    global totalbuttonpressed
    dailybuttonpressed = False
    weeklybuttonpressed = False
    totalbuttonpressed = False

# Add the parent folder to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(parent_dir)

# Get discord bot token
with open(os.path.join(parent_dir, 'discord_bot_token.txt')) as readtoken:
    discordsecret = readtoken.readline()   


## BOT

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents) # The prefix is not used, its just a requirement to have it.

# Event to run when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    scheduled_data_save.start()
    scheduled_daily_refresh.start()
    scheduled_weekly_refresh.start()
    print(f'Logged in as {bot.user.name}')

# Event to run when the bot is resumed
@bot.event
async def on_resumed():
    print('Bot has resumed.')
    if not scheduled_data_save.is_running():
        scheduled_data_save.start()  # Restart the loop after resuming
    if not scheduled_daily_refresh.is_running():
        scheduled_daily_refresh.start()  # Restart the loop after resuming
    if not scheduled_weekly_refresh.is_running():
        scheduled_weekly_refresh.start()  # Restart the loop after resuming


# Commands
def t1totalembed():
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 1 Total Leaderboard", color=discord.Color(0x6b0000))
    
    subfolder_path = os.path.join(parent_dir, "userkills")
    result_total = get_top_tier1_kills(subfolder_path)

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{datarefreshtime}:R>_")

    return embed

def t2totalembed():
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 2 Total Leaderboard", color=discord.Color(0x6b0000))
    
    subfolder_path = os.path.join(parent_dir, "userkills")
    result_total = get_top_tier2_kills(subfolder_path)

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{datarefreshtime}:R>_")

    return embed
    
def alltotalembed():
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Total Leaderboard", color=discord.Color(0x6b0000))
    
    subfolder_path = os.path.join(parent_dir, "userkills")
    result_total = get_top_total_kills(subfolder_path)

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{datarefreshtime}:R>_")

    return embed

def t1dailyembed():
    global day
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 1 Daily Leaderboard", color=discord.Color(0x6b0000))
    
    result_t1, _, _ = dailytask.compare_t1_t2_kills()
    result_total = result_t1

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"_Day: #{day}_", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{dailyrefreshtime}:R>_")

    return embed

def t2dailyembed():
    global day
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 2 Daily Leaderboard", color=discord.Color(0x6b0000))
    
    _, result_t2, _ = dailytask.compare_t1_t2_kills()
    result_total = result_t2

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"_Day: #{day}_", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{dailyrefreshtime}:R>_")

    return embed

def alldailyembed():
    global day
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Total Daily Leaderboard", color=discord.Color(0x6b0000))
    
    _, _, result_all = dailytask.compare_t1_t2_kills()
    result_total = result_all

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"_Day: #{day}_", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{dailyrefreshtime}:R>_")

    return embed

def t1weeklyembed():
    global week
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 1 Weekly Leaderboard", color=discord.Color(0x6b0000))
    
    result_t1, _, _ = weeklytask.compare_t1_t2_kills()
    result_total = result_t1

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"_Week: #{week}_", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{weeklyrefreshtime}:R>_")

    return embed

def t2weeklyembed():
    global week
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 2 Weekly Leaderboard", color=discord.Color(0x6b0000))
    
    _, result_t2, _ = weeklytask.compare_t1_t2_kills()
    result_total = result_t2

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"_Week: #{week}_", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{weeklyrefreshtime}:R>_")

    return embed

def allweeklyembed():
    global week
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Total Weekly Leaderboard", color=discord.Color(0x6b0000))
    
    _, _, result_all = weeklytask.compare_t1_t2_kills()
    result_total = result_all

    # Sample leaderboard data
    leaderboard_data = [
        ("User1", 100),
        ("User2", 90),
        ("User3", 80),
        ("User4", 70),
        ("User5", 60)
    ]

    # Update the leaderboard with total kills
    for i, entry in enumerate(result_total, start=1):
        user, score = entry.split(":")
        user = user.strip()
        score = int(score.strip())
        leaderboard_data[i-1] = (user, score)

    # Display the updated leaderboard
    for i, (user, score) in enumerate(leaderboard_data, start=1):
        # Change UUID to Username
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user}").json()
        data = data["name"]
        embed.add_field(name=f"#{i} - {data}", value=f"Kills: {score}", inline=False)
    embed.add_field(name=" ", value=f"_Week: #{week}_", inline=False)
    embed.add_field(name=" ", value=f"\n_Refreshes: <t:{weeklyrefreshtime}:R>_")

    return embed


# Buttons
class SimpleView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_timeout(self) -> None:
        print("Timeout")
        if self.instance:  # Check if self.instance is set
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True


    # Function to enable all buttons
    def enable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = False
    
    # Function to enable all buttons in row 1
    def enable_row1_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.row == 1:
                child.disabled = False

    # Function to enable all buttons in row 2
    def enable_row2_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.row == 2:
                child.disabled = False

    # Function to disable all buttons
    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True


    # Row 1
    @discord.ui.button(label="Tier 1", style=discord.ButtonStyle.primary, row=1)
    async def t1button(self, interaction: discord.Interaction, button: discord.ui.Button):
        resetrow1buttons()
        global t1buttonpressed
        t1buttonpressed = True
        print("T1 - Button Pressed") # Debug line
        if dailybuttonpressed == True:
            embed = t1dailyembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif weeklybuttonpressed == True:
            embed = t1weeklyembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif totalbuttonpressed == True:
            embed = t1totalembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        view.enable_row1_buttons()
        

    @discord.ui.button(label="Tier 2", style=discord.ButtonStyle.primary, row=1)
    async def t2button(self, interaction: discord.Interaction, button: discord.ui.Button):
        resetrow1buttons()
        global t2buttonpressed
        t2buttonpressed = True
        print("T2 - Button Pressed") # Debug line
        if dailybuttonpressed == True:
            embed = t2dailyembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif weeklybuttonpressed == True:
            embed = t2weeklyembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif totalbuttonpressed == True:
            embed = t2totalembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()

    @discord.ui.button(label="All", style=discord.ButtonStyle.primary, row=1)
    async def t1totalbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        resetrow1buttons()
        global allbuttonpressed
        allbuttonpressed = True
        print("All - Button Pressed") # Debug line
        if dailybuttonpressed == True:
            embed = alldailyembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif weeklybuttonpressed == True:
            embed = allweeklyembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif totalbuttonpressed == True:
            embed = alltotalembed()
            view = SimpleView(timeout=120)
            view.enable_row1_buttons()
            button.disabled = True
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        

    # Row 2
    @discord.ui.button(label="Daily", style=discord.ButtonStyle.success, row=2)
    async def dailybutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        resetrow2buttons()
        global dailybuttonpressed       
        dailybuttonpressed = True
        print("Daily - Button Pressed") # Debug line
        if t1buttonpressed == True:
            embed = t1dailyembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif t2buttonpressed == True:
            embed = t2dailyembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif allbuttonpressed == True:
            embed = alldailyembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()

    @discord.ui.button(label="Weekly", style=discord.ButtonStyle.success, row=2)
    async def weeklybutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        resetrow2buttons()
        global weeklybuttonpressed
        weeklybuttonpressed = True
        print("Weekly - Button Pressed") # Debug line
        if t1buttonpressed == True:
            embed = t1weeklyembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif t2buttonpressed == True:
            embed = t2weeklyembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif allbuttonpressed == True:
            embed = allweeklyembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
       
    @discord.ui.button(label="Total", style=discord.ButtonStyle.success, row=2)
    async def totalbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        #view.enable_row2_buttons() ***add this back when daily and weekly stuff are added
        button.disabled = True
        resetrow2buttons() # Reset the row 2 button
        global totalbuttonpressed 
        totalbuttonpressed = True
        print("Total - Button Pressed") # Debug line
        if t1buttonpressed == True:
            embed = t1totalembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif t2buttonpressed == True:
            embed = t2totalembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()
        elif allbuttonpressed == True:
            embed = alltotalembed()
            view = SimpleView(timeout=120)
            message = await interaction.response.edit_message(embed=embed, view=view)
            view.message = message
            await view.wait()


# Define /t1total command
@bot.tree.command(name="t1total", description="Displays alltime leaderboard for total of Tier 1 kills.")
async def t1total(ctx):
    resetallbuttons()
    global t1buttonpressed
    global totalbuttonpressed 
    t1buttonpressed = True
    totalbuttonpressed = True
    print("T1 Total - command called") # Debug line
    
    embed = t1totalembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /t2total command
@bot.tree.command(name="t2total", description="Displays alltime leaderboard for total of Tier 2 kills.")
async def t2total(ctx):
    resetallbuttons()
    global t2buttonpressed
    global totalbuttonpressed
    t2buttonpressed = True
    totalbuttonpressed = True
    print("T2 Total - command called") # Debug line

    embed = t2totalembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define the /alltotal command
@bot.tree.command(name="alltotal", description="Displays alltime leaderboard for total of both Tier 1 & Tier 2 kills.")
async def alltotal(ctx):
    resetallbuttons()
    global allbuttonpressed
    global totalbuttonpressed
    allbuttonpressed = True
    totalbuttonpressed = True
    print("All Total - command called") # Debug line

    embed = alltotalembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /t1daily command
@bot.tree.command(name="t1daily", description="Displays daily leaderboard for total of Tier 1 kills.")
async def t1daily(ctx):
    resetallbuttons()
    global t1buttonpressed
    global dailybuttonpressed
    t1buttonpressed = True
    dailybuttonpressed = True
    print("T1 Daily - command called") # Debug line
    
    embed = t1dailyembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /t2daily command
@bot.tree.command(name="t2daily", description="Displays daily leaderboard for total of Tier 2 kills.")
async def t2daily(ctx):
    resetallbuttons()
    global t2buttonpressed
    global dailybuttonpressed
    t2buttonpressed = True
    dailybuttonpressed = True
    print("T2 Daily - command called") # Debug line
    
    embed = t2dailyembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /alldaily command
@bot.tree.command(name="alldaily", description="Displays daily leaderboard for total of both Tier 1 & Tier 2 kills.")
async def alldaily(ctx):
    resetallbuttons()
    global allbuttonpressed
    global dailybuttonpressed
    allbuttonpressed = True
    dailybuttonpressed = True
    print("All Daily - command called") # Debug line
    
    embed = alldailyembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /t1weekly command
@bot.tree.command(name="t1weekly", description="Displays weekly leaderboard for total of Tier 1 kills.")
async def t1weekly(ctx):
    resetallbuttons()
    global t1buttonpressed
    global weeklybuttonpressed
    t1buttonpressed = True
    weeklybuttonpressed = True
    print("T1 Weekly - command called") # Debug line
    
    embed = t1weeklyembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /t2weekly command
@bot.tree.command(name="t2weekly", description="Displays weekly leaderboard for total of Tier 2 kills.")
async def t2weekly(ctx):
    resetallbuttons()
    global t2buttonpressed
    global weeklybuttonpressed
    t2buttonpressed = True
    weeklybuttonpressed = True
    print("T2 Weekly - command called") # Debug line

    embed = t2weeklyembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /allweekly command
@bot.tree.command(name="allweekly", description="Displays weekly leaderboard for total of both Tier 1 & Tier 2 kills.")
async def allweekly(ctx):
    resetallbuttons()
    global allbuttonpressed
    global weeklybuttonpressed
    allbuttonpressed = True
    weeklybuttonpressed = True
    print("All Weekly - command called") # Debug line

    embed = allweeklyembed()
    view = SimpleView(timeout=120)
    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /check command
@bot.tree.command(name="check", description="Checks if the bot is refreshing data.")
async def check(ctx):
    print("Check - command called") # Debug line
    if not scheduled_data_save.is_running():
        scheduled_data_save.start()
        await ctx.response.send_message('The loop has been started.', ephemeral=True)
    else:
        await ctx.response.send_message('The loop is already running.', ephemeral=True)

# Define /info command
@bot.tree.command(name="info", description="Displays the changelog of the bot.")
async def info(ctx):
    print(f"Info - command called") # Debug line
    print(f"Bot Version: {botversion}")
    embed = discord.Embed(title="**Bot Info**",
    description=f"**Version**\n{botversion}\n\n**ChangeLog**\n- Changed embedded time format\n- Fixed bug in console", colour=0x5c5c5c)
    embed.set_footer(text="Bot by @t_cr1ck", icon_url="https://cdn.discordapp.com/avatars/559636250148208641/84af17c99cf95ba3127f9c1c296f348f.webp")
    await ctx.response.send_message(embed=embed)

# Schedule the save_data function to run every 15 mins
@tasks.loop(minutes=15)
async def scheduled_data_save():
    global datarefreshtime
    datarefreshtime += 900
    savedata()

# Schedule the daily function to run every day
@tasks.loop(hours=24)
async def scheduled_daily_refresh():
    global day
    global dailyrefreshtime
    day += 1
    dailyrefreshtime += 86400
    dailytask.dailyrefresh()

# Schedule the weekly function to run every week
@tasks.loop(hours=168)
async def scheduled_weekly_refresh():
    global week
    global weeklyrefreshtime
    week += 1
    weeklyrefreshtime += 604800
    weeklytask.weeklyrefresh()

# Run the bot
bot.run(discordsecret)
