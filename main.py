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
import profit_calc
import asyncio

botversion = "Release 2.1"

datarefreshtime = 0
dailyrefreshtime = 0
weeklyrefreshtime = 0
day = 0
week = 0

# Function to get current Unix time
def get_unixtime():
    currenttime = datetime.datetime.now()
    return int(time.mktime(currenttime.timetuple()))

# Function to calculate the next interval in seconds (for 15 minutes, 24 hours, or 7 days)
def calculate_next_interval(interval_seconds):
    current_time = datetime.datetime.now()
    seconds_since_epoch = int(current_time.timestamp())
    seconds_until_next_interval = interval_seconds - (seconds_since_epoch % interval_seconds)
    return seconds_until_next_interval

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
bot = commands.Bot(command_prefix="!", intents=intents) # The prefix is used for the !sync command

# Event to run when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.add_cog(SyncCog(bot))
    await start_task_schedulers()
    print(f'Logged in as {bot.user.name}')

# Event to run when the bot is resumed
@bot.event
async def on_resumed():
    print('Bot has resumed.')
    # Check if tasks are already running
    if not scheduled_data_save.is_running() or not scheduled_daily_refresh.is_running() or not scheduled_weekly_refresh.is_running():
        await start_task_schedulers()  # Start all task schedulers

# Commands
def t1profitembed():
    formatted_money_made = "{:,}".format(round((t1_profit_calc[1])+(t1_profit_calc[2]), 2))
    formatted_cost = "{:,}".format(t1_profit_calc[2])
    formatted_profit = "{:,}".format(t1_profit_calc[1])
    embed=discord.Embed(title="Profit Calculator", description="Tier 1", color=discord.Color(0x00b36e))
    embed.add_field(name="Number of Bosses", value=f"{t1_profit_calc[0]}", inline=False)
    embed.add_field(name="Money Made", value=f"${formatted_money_made}", inline=True)
    embed.add_field(name="Total Cost", value=f"${formatted_cost}", inline=True)
    embed.add_field(name="Profit", value=f"${formatted_profit}", inline=False)
    return embed

def t2profitembed():
    formatted_money_made = "{:,}".format(round((t2_profit_calc[1])+(t2_profit_calc[2]), 2))
    formatted_cost = "{:,}".format(t2_profit_calc[2])
    formatted_profit = "{:,}".format(t2_profit_calc[1])
    embed=discord.Embed(title="Profit Calculator", description="Tier 2", color=discord.Color(0x00b36e))
    embed.add_field(name="Number of Bosses", value=f"{t2_profit_calc[0]}", inline=False)
    embed.add_field(name="Money Made", value=f"${formatted_money_made}", inline=True)
    embed.add_field(name="Total Cost", value=f"${formatted_cost}", inline=True)
    embed.add_field(name="Profit", value=f"${formatted_profit}", inline=False)
    return embed          

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

class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx):
        fmt_global = await ctx.bot.tree.sync()
        fmt_guild = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt_global) + len(fmt_guild)} commands.")

# Define /t1profit command
@bot.tree.command(name="t1profit", description="Arachne tier 1 profit calculator.")
async def profitcalc(ctx, callings: int):
    global t1_profit_calc
    print("T1Profit - command called")
    await ctx.response.defer()
    t1_profit_calc = await profit_calc.t1(callings)
    embed = t1profitembed()
    await ctx.followup.send(embed=embed)   


# Define /t2profit command
@bot.tree.command(name="t2profit", description="Arachne tier 2 profit calculator.")
async def profitcalc(ctx, crystals: int):
    global t2_profit_calc
    print("T2Profit - command called")
    await ctx.response.defer()
    t2_profit_calc = await profit_calc.t2(crystals)
    embed = t2profitembed()
    await ctx.followup.send(embed=embed)   
    


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
    # Check if tasks are already running
    if not scheduled_data_save.is_running() or not scheduled_daily_refresh.is_running() or not scheduled_weekly_refresh.is_running():
        await start_task_schedulers()  # Start all task schedulers
        await ctx.response.send_message('The loop has been started.', ephemeral=True)
    else:
        await ctx.response.send_message('The loop is already running.', ephemeral=True)

# Define /info command
@bot.tree.command(name="info", description="Displays the changelog of the bot.")
async def info(ctx):
    print(f"Info - command called") # Debug line
    print(f"Bot Version: {botversion}")
    embed = discord.Embed(title="**Bot Info**",
    description=f"**Version**\n{botversion}\n\n**ChangeLog**\n- Fixed refresh times displaying incorrectly for the 7th time\n- Updated API requests to new endpoints \n- Code cleanup", colour=0x5c5c5c)
    embed.set_footer(text="Bot by @t_cr1ck", icon_url="https://cdn.discordapp.com/avatars/559636250148208641/a8bc7e17e3e584adf2395e576a2a43f3.webp")
    await ctx.response.send_message(embed=embed)

# Define /copypasta command
@bot.tree.command(name="copypasta", description="What is Arachne?")
async def copypasta(ctx):
    part1 = (
        "Arachne is a boss in the spider island, it has two versions t1 which is spawned with 4 arachnes callings which you can buy off the bazaar, has a faster spawn time, is easier but makes less xp and less coins per hour, and then there's t2 Arachne which is spawned using an Arachne crystal which is crafted using Arachne frags which can also be purchased from the bazaar along with enchanted string and enchanted spider eyes. It has a consistent drop pool as long as you get top 5 damage dealt with no important rng based drops. All of the loot you get from it can either be salvaged for spider essence at the npc in the spider den or insta sold to npc for a consistent price unaffected by deflation of bazaar prices, so more people doing Arachne does not significantly affect the profits you get from it. On top of that, while doing t2 Arachne, you can spawn about 2-3 t4 tarantula slayer bosses because the Arachne broods give a large amount of combat xp per kill. There's also a method to skip half of the spawn animation saving a lot of time. When the boss is during its last phase of broods, go back to the altar and hold down right click with the crystal to spawn a new one the exact moment the last one gets killed by another player finishing off the boss."
    )
    
    part2 = (
        "You can only craft the Arachne crystals after finishing the entire archeologists relics quest and the shiny relics too. It's definitely worth doing that and crafting the crystals yourself as it saves a lot of coins. Also, the person who places the crystal gets an additional 12 soul string which makes up for about 2/3 of the cost of the crystal. The boss has a damage cap of 20k damage a hit, so you don't need much damage to get top 5 damage. Make sure you have at least 82% attack speed and are using a melee weapon as it is immune to all other sources of damage. If you are dying to the poison attack, use a cow head as your helmet as it gives complete immunity to the poison. Farming t2 Arachnes makes about 15-20m coins an hour."
    )
    
    await ctx.response.send_message(part1)
    await ctx.channel.send(part2)


# Schedule the save_data function to run every 15 mins
async def scheduled_data_save():
    global datarefreshtime
    
    while True:
        # Calculate time until the next 15-minute interval (900 seconds)
        sleep_duration = calculate_next_interval(900)
        
        # Update the refresh time for the embed
        datarefreshtime = get_unixtime() + sleep_duration
        
        # Run the data saving task
        savedata()
        
        # Print the next refresh time for debugging
        print(f"Next data refresh at: {datetime.datetime.fromtimestamp(datarefreshtime)}")
        
        # Wait until the next 15-minute mark
        await asyncio.sleep(sleep_duration)

# Schedule the daily function to run every day
async def scheduled_daily_refresh():
    global day
    global dailyrefreshtime
    
    while True:
        # Calculate time until the next 24-hour interval (86400 seconds)
        sleep_duration = calculate_next_interval(86400)
        
        # Update the daily refresh time
        dailyrefreshtime = get_unixtime() + sleep_duration
        
        # Increment the day counter
        day += 1
        
        # Run the daily refresh task
        dailytask.dailyrefresh()
        
        # Print the next daily refresh time for debugging
        print(f"Next daily refresh at: {datetime.datetime.fromtimestamp(dailyrefreshtime)}")
        
        # Wait until the next 24-hour mark
        await asyncio.sleep(sleep_duration)

# Schedule the weekly function to run every week
async def scheduled_weekly_refresh():
    global week
    global weeklyrefreshtime
    
    while True:
        # Calculate time until the next 7-day interval (604800 seconds)
        sleep_duration = calculate_next_interval(604800)
        
        # Update the weekly refresh time
        weeklyrefreshtime = get_unixtime() + sleep_duration
        
        # Increment the week counter
        week += 1
        
        # Run the weekly refresh task
        weeklytask.weeklyrefresh()
        
        # Print the next weekly refresh time for debugging
        print(f"Next weekly refresh at: {datetime.datetime.fromtimestamp(weeklyrefreshtime)}")
        
        # Wait until the next 7-day mark
        await asyncio.sleep(sleep_duration)

# Start all task schedulers
async def start_task_schedulers():
    # Schedule all tasks concurrently
    await asyncio.gather(
        scheduled_data_save(),
        scheduled_daily_refresh(),
        scheduled_weekly_refresh()
    )

# Run the bot
bot.run(discordsecret)
