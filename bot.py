import discord
from discord import app_commands
from discord.ext import commands

# 1. Setup Bot Permissions (Intents)
intents = discord.Intents.default()
intents.members = True  # Required to interact with server members and send DMs

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced successfully!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


# 2. Define the Link Button View with your specific Duolingo URL
class DuolingoButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        # Link button styled to point exactly to your family plan invite link
        self.add_item(discord.ui.Button(
            label="Activate Super Duolingo", 
            style=discord.ButtonStyle.url, 
            url="https://invite.duolingo.com/family-plan/2-611M-73D5-N4TP-528A"
        ))


# 3. Create the Slash Command with your exact title and description requirements
@bot.tree.command(name="send_giveaway", description="Sends the Duolingo Super giveaway reward to a server member.")
@app_commands.describe(target_user="The member who won the giveaway")
async def send_giveaway_command(interaction: discord.Interaction, target_user: discord.Member):
    # Acknowledge the command quickly to prevent timeouts
    await interaction.response.defer(ephemeral=True)

    # Build the embed exactly as requested
    embed = discord.Embed(
        title="FREE DUOLINGO SUPER GIVEAWAY",
        description=(
            f"Dear {target_user.mention} from Mine! Leo Server :\n"
            "You’ve won this giveaway, to activate your super Duolingo plan, "
            "please click on the button below and it will open your web browser shortly.."
        ),
        color=discord.Color.green()  # Green theme to match Duolingo branding
    )

    try:
        # Create or open the DM channel with the winner
        dm_channel = target_user.dm_channel or await target_user.create_dm()
        
        # Send the DM with the custom embed and interactive link button
        await dm_channel.send(embed=embed, view=DuolingoButtonView())
        
        # Confirmation message visible only to you
        await interaction.followup.send(f"✅ Successfully sent the giveaway DM to {target_user.name}!", ephemeral=True)
        
    except discord.Forbidden:
        # Inform you if your friend's privacy settings are blocking direct messages
        await interaction.followup.send(
            f"❌ Failed to DM {target_user.name}. Their privacy settings are blocking direct messages. "
            f"Please ask them to temporarily allow DMs from server members so the bot can deliver the link.", 
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"⚠️ An unexpected error occurred: {e}", ephemeral=True)

# Run your bot (Be sure to replace this placeholder with your actual bot token)
bot.run('MTU0ODMzMDU2MTg3MjA3Mjc3NA.GurFwO.OkOO0EzdV-TxGo7sTYPlEihxszVKlhI9mnM6fY')
