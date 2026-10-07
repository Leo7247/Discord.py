import os
import discord
from discord import app_commands
from discord.ext import commands

# 1. Configure Global Application Permissions (Intents)
intents = discord.Intents.default()
intents.members = True          # Allows the bot to find server members and open DMs
intents.message_content = True  # Resolves the privileged message content intent warning

class MineLeoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    # Automatically synchronizes slash commands with the Discord API on startup
    async def setup_hook(self):
        await self.tree.sync()
        print("⚡ Slash commands synced successfully to Discord API!")

bot = MineLeoBot()

@bot.event
async def on_ready():
    print(f"========================================")
    print(f"🤖 Bot Status: ONLINE")
    print(f"Logged in as : {bot.user.name} (ID: {bot.user.id})")
    print(f"========================================")


# 2. Setup the Interactive Component View with High-Visibility Button Style
class DuolingoRewardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout=None keeps the link button persistent
        
        # Injected the exact family plan reward url you specified
        self.add_item(discord.ui.Button(
            label="Activate Super Duolingo", 
            style=discord.ButtonStyle.url, 
            url="https://duolingo.com"
        ))


# 3. Create the Slash Command with your Exact Text and Embed Layout
@bot.tree.command(name="send_giveaway", description="Delivers the Duolingo Super family invitation to the winner via DM.")
@app_commands.describe(target_user="Select the server member who won the giveaway")
async def send_giveaway_command(interaction: discord.Interaction, target_user: discord.Member):
    # Defer response immediately to avoid a 3-second Gateway timeout error
    await interaction.response.defer(ephemeral=True)

    # Constructing the exact user layout and strings requested
    embed = discord.Embed(
        title="FREE DUOLINGO SUPER GIVEAWAY",
        description=(
            f"Dear {target_user.mention} from Mine! Leo Server :\n"
            "You’ve won this giveaway, to activate your super Duolingo plan, "
            "please click on the button below and it will open your web browser shortly.."
        ),
        color=discord.Color.from_rgb(88, 196, 26)  # High-visibility vibrant Duolingo Green
    )
    embed.set_footer(text=f"Mine! Leo Server • Official Giveaway Reward Distribution")

    try:
        # Establish or reuse the private DM pipeline with the target winner
        dm_channel = target_user.dm_channel or await target_user.create_dm()
        
        # Broadcast the embed package containing the link component view
        await dm_channel.send(embed=embed, view=DuolingoRewardView())
        
        # Confirm completion back to the moderator executing the command
        await interaction.followup.send(f"✅ Successfully dispatched giveaway DM to **{target_user.name}**!", ephemeral=True)
        
    except discord.Forbidden:
        # Catch exception if the winner has closed or limited their private messages
        await interaction.followup.send(
            f"❌ **Delivery Failed:** {target_user.name} has their Direct Messages disabled.\n"
            f"Please notify them to open their Privacy Settings for this server so the bot can send the link.", 
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"⚠️ Runtime Error encountered: `{e}`", ephemeral=True)


# 4. Safe Execution Engine
# Looks directly into Railway App's internal variables for safety instead of reading plaintext keys
TOKEN = os.environ.get('MTU0ODMzMDU2MTg3MjA3Mjc3NA.GVJorv.9qPfvI17ZwaovDiSYpI9ZTbCHFAS02aFf-6f1Y')

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ CRITICAL ERROR: Could not find 'DISCORD_TOKEN' inside your Environment Variables!")
        print("Please add a variable named 'DISCORD_TOKEN' inside your host dashboard configuration.")
