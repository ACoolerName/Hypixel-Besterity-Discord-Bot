from get_userdata import savedata
from discord.ext import commands
from sort_top import *
import discord
import discord.ui
import os
import sys
import requests
import schedule
import asyncio

botversion = "Alpha 1"

# Add the parent folder to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(parent_dir)

# Get discord bot token
with open(parent_dir+'\\discord_bot_token.txt') as readtoken:
    discordsecret = readtoken.readline()   

## BOT

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event to run when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

class SimpleView(discord.ui.View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = None
        
    async def enable_all_items(self):
        for item in self.children:
            item.disabled = False
        await self.message.edit(view=self)

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    

    async def on_timeout(self) -> None:
        print("Timeout")
        await self.disable_all_items()


    # Row 1
    @discord.ui.button(label="Daily", style=discord.ButtonStyle.primary, row=1)
    async def dailybutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Daily (row 1) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, the buttons do not work in this version, please use the commands.", ephemeral=True)
        
    @discord.ui.button(label="Weekly", style=discord.ButtonStyle.primary, row=1)
    async def weeklybutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Weekly (row 1) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, the buttons do not work in this version, please use the commands.", ephemeral=True)
        
    @discord.ui.button(label="Total", style=discord.ButtonStyle.primary, row=1)
    async def totalbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Total (row 1) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, the buttons do not work in this version, please use the commands.", ephemeral=True)
        
    @discord.ui.button(label="Blocked", style=discord.ButtonStyle.danger, row=1)
    async def blockedbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Blocked (row 1) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, you do not have permission to view this.", ephemeral=True)


    # Row 2
    @discord.ui.button(label="Tier 1", style=discord.ButtonStyle.success, row=2)
    async def tier1button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Teir 1 (row 2) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, the buttons do not work in this version, please use the commands.", ephemeral=True)
        
    @discord.ui.button(label="Tier 2", style=discord.ButtonStyle.success, row=2)
    async def tier2button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Teir 2 (row 2) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, the buttons do not work in this version, please use the commands.", ephemeral=True)
        
    @discord.ui.button(label="Total", style=discord.ButtonStyle.success, row=2)
    async def tiertotalbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Total (row 2) - Button Pressed") # Debug line
        await interaction.response.send_message("Sorry, the buttons do not work in this version, please use the commands.", ephemeral=True)


# Define /t1total command
@bot.tree.command(name="t1total", description="Displays alltime leaderboard for total of Tier 1 kills.")
async def t1total(ctx):
    print("T1 Total - command called") # Debug line
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 1 Total Leaderboard", color=discord.Color(0x6b0000))
    
    subfolder_path = parent_dir+"\\userkills"
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

    embed.set_footer(text="Refreshes every 24h")

    view = SimpleView(timeout=240)

    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define /t2total command
@bot.tree.command(name="t2total", description="Displays alltime leaderboard for total of Tier 2 kills.")
async def t2total(ctx):
    print("T2 Total - command called") # Debug line
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Tier 2 Total Leaderboard", color=discord.Color(0x6b0000))
    
    subfolder_path = parent_dir+"\\userkills"
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

    embed.set_footer(text="Refreshes every 24h")

    view = SimpleView(timeout=240)

    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()

# Define the /alltotal command
@bot.tree.command(name="alltotal", description="Displays alltime leaderboard for total of both Tier 1 & Tier 2 kills.")
async def alltotal(ctx):
    print("All Total - command called") # Debug line
    # Create an embed for the leaderboard
    embed = discord.Embed(title="Total Leaderboard", color=discord.Color(0x6b0000))
    
    subfolder_path = parent_dir+"\\userkills"
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

    embed.set_footer(text="Refreshes every 24h")

    view = SimpleView(timeout=120)

    message = await ctx.response.send_message(embed=embed, view=view)
    view.message = message
    await view.wait()


# Define /t1daily command
@bot.tree.command(name="t1daily", description="Displays daily leaderboard for total of Tier 1 kills.")
async def t1daily(ctx):
    print("T1 Daily - command called") # Debug line
    await ctx.response.send_message("Sorry, only the 'total' commands work in this version.", ephemeral=True)

# Define /t2daily command
@bot.tree.command(name="t2daily", description="Displays daily leaderboard for total of Tier 2 kills.")
async def t2daily(ctx):
    print("T2 Daily - command called") # Debug line
    await ctx.response.send_message("Sorry, only the 'total' commands work in this version.", ephemeral=True)

# Define /alldaily command
@bot.tree.command(name="alldaily", description="Displays daily leaderboard for total of both Tier 1 & Tier 2 kills.")
async def alldaily(ctx):
    print("All Daily - command called") # Debug line
    await ctx.response.send_message("Sorry, only the 'total' commands work in this version.", ephemeral=True)


# Define /t1weekly command
@bot.tree.command(name="t1weekly", description="Displays weekly leaderboard for total of Tier 1 kills.")
async def t1weekly(ctx):
    print("T1 Weekly - command called") # Debug line
    await ctx.response.send_message("Sorry, only the 'total' commands work in this version.", ephemeral=True)

# Define /t2weekly command
@bot.tree.command(name="t2weekly", description="Displays weekly leaderboard for total of Tier 2 kills.")
async def t2weekly(ctx):
    print("T2 Weekly - command called") # Debug line
    await ctx.response.send_message("Sorry, only the 'total' commands work in this version.", ephemeral=True)

# Define /allweekly command
@bot.tree.command(name="allweekly", description="Displays weekly leaderboard for total of both Tier 1 & Tier 2 kills.")
async def allweekly(ctx):
    print("All Weekly - command called") # Debug line
    await ctx.response.send_message("Sorry, only the 'total' commands work in this version.", ephemeral=True)

# Define /version command
@bot.tree.command(name="version", description="Displays the current version of the bot")
async def version(ctx):
    print(f"Version {botversion} - command called") # Debug line
    await ctx.response.send_message(f"Version: {botversion}", ephemeral=True)


# Define a function to run the scheduling loop
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


# Asynchronous main function
async def main():
    await bot.start(discordsecret)
    await run_schedule()


# Run the bot
asyncio.run(main())