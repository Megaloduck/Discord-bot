import discord
import random 
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord import Intents, Activity, ActivityType

TOKEN = 'MTIyNDk3MDQ2MTIwOTk1NjM1Mw.Gqj-Oa.3t_UZyustvemPUK_XEu5IbgKWX5koZz6QDnrWk'

# Channel IDs
WELCOME_CHANNEL_ID = 1215484754225532959  # ID Informational-Greetings channel
MEMBER_COUNTER_CHANNEL_ID = 1228695484638564402  # ID saluran untuk member counter
RULES_CHANNEL_ID = 1225299558683381820  

# Role IDs
NOBODY_ROLE_ID = 1215482614757199882  
RESEARCHER_ROLE_ID = 1215480387950870640  
ARTIST_ROLE_ID = 1215490688771166208  
ENGINEER_ROLE_ID = 1215480767631593553  

REACTION_ROLE_MAPPING = {
    '🔬 Researcher': RESEARCHER_ROLE_ID,
    '🎨 Artist': ARTIST_ROLE_ID,
    '🔧 Engineer': ENGINEER_ROLE_ID
}

# Intents untuk bot
intents = Intents.all()

# Bot instance
bot = commands.Bot(
    command_prefix='/',
    intents=intents,
    activity=Activity(type=ActivityType.watching, name="your every steps")
)

# Loop untuk memperbarui jumlah anggota setiap 10 menit
@tasks.loop(minutes=2)
async def update_member_counter():
    for guild in bot.guilds:
        member_counter_channel = guild.get_channel(MEMBER_COUNTER_CHANNEL_ID)
        if member_counter_channel:
            member_count = guild.member_count
            await member_counter_channel.edit(topic=f"Total Members: {member_count}")
    print("Member counter updated.")

@bot.event
async def on_ready():
    print(f'Bot {bot.user} telah online!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}! Jangan lupa bernapas :)')

@bot.command()
async def makan(ctx):
    await ctx.send(f'Jangan lupa makan, {ctx.author.name}! :)')

@bot.command()
async def member_count(ctx):
    guild = ctx.guild  # Mendapatkan server (guild) tempat perintah dipanggil
    member_count = guild.member_count  # Mendapatkan jumlah member di guild
    await ctx.send(f"Jumlah anggota di server ini: {member_count} anggota.")

# Rules
@bot.command()
async def rules(ctx):
    embed = discord.Embed(
        title="📜 Server Rules 📜",
        description="**Welcome to our server!** Please follow the rules to ensure a great experience for everyone.",
        color=discord.Color.dark_red()
    )

    embed.add_field(name="1. Be respectful", value="Treat everyone with kindness and respect.", inline=False)
    embed.add_field(name="2. No spamming", value="Avoid spamming messages or emojis.", inline=False)
    embed.add_field(name="3. Keep it PG-13", value="No inappropriate content.", inline=False)
    embed.add_field(name="4. Follow the server's theme", value="Stick to the designated channels for specific topics.", inline=False)

    embed.set_footer(text="Enjoy your time here! 😊")  
    file = discord.File(r"D:\Neuroscience\Python\redrules.jpeg", filename="redrules.jpeg")
    embed.set_thumbnail(url="attachment://redrules.jpeg") # Optional: add a thumbnail image

    await ctx.send(embed=embed, file=file)

@bot.command()
async def send_button(ctx):
    # Subclassing View to create a custom view with a button
    class ButtonView(View):
        def __init__(self):
            super().__init__()
            # Add the button to the view
            self.add_item(Button(label="Click Me!", style=discord.ButtonStyle.green))

        @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.green)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Respond when the button is clicked
            await interaction.response.send_message("Button clicked!", ephemeral=True)

    # Instantiate the view
    view = ButtonView()

    # Send the message with the button
    await ctx.send("This is a message with a button:", view=view)

@bot.command()
async def coinflip(ctx):
    """Let the user choose Heads or Tails and flip a coin."""
    
    # Create an embed for the choice
    embed = discord.Embed(
        title="🪙 Coin Flip",
        description="Choose your side: Head or Tail!",
        color=discord.Color.gold()
    )

    # Create buttons for Heads and Tails
    class CoinFlipView(discord.ui.View):
        def __init__(self):
            super().__init__()
        
        @discord.ui.button(label="Head", style=discord.ButtonStyle.primary)
        async def head_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.resolve_coinflip(interaction, "Head")
        
        @discord.ui.button(label="Tail", style=discord.ButtonStyle.danger)
        async def tail_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.resolve_coinflip(interaction, "Tail")

        async def resolve_coinflip(self, interaction: discord.Interaction, choice: str):
            # Simulate the coin flip
            result = random.choice(["Head", "Tail"])
            outcome = "Win!" if result == choice else "Lose!"
            
            # Send the result back
            await interaction.response.send_message(
                f"You chose **{choice}**. The coin landed on **{result}**. You {outcome}!",
                ephemeral=True
            )
            # Disable the buttons after a choice
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)

    # Send the embed with buttons
    await ctx.send(embed=embed, view=CoinFlipView())

bot.run(TOKEN)