import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("TOKEN")

OWNER_ROLE_ID = 1513093428920061972

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

GAMEMODES = [
    "Crystal",
    "Sword",
    "Axe",
    "UHC",
    "NethPot",
    "SMP",
    "Mace",
    "All Gamemodes"
]

RANKS = [
    "Unranked",
    "LT5",
    "LT4",
    "LT3",
    "LT2",
    "LT1",
    "HT5",
    "HT4",
    "HT3",
    "HT2",
    "HT1"
]

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@app_commands.command(
    name="setrank",
    description="Create a SharkSMP rank test result."
)
@app_commands.describe(
    user="Player tested",
    minecraft_username="Minecraft username",
    gamemode="Gamemode tested",
    previous_rank="Previous rank",
    new_rank="Rank earned"
)
@app_commands.choices(
    gamemode=[
        app_commands.Choice(name=g, value=g)
        for g in GAMEMODES
    ],
    previous_rank=[
        app_commands.Choice(name=r, value=r)
        for r in RANKS
    ],
    new_rank=[
        app_commands.Choice(name=r, value=r)
        for r in RANKS
    ]
)
async def setrank(
    interaction: discord.Interaction,
    user: discord.Member,
    minecraft_username: str,
    gamemode: app_commands.Choice[str],
    previous_rank: app_commands.Choice[str],
    new_rank: app_commands.Choice[str]
):

    if not any(role.id == OWNER_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message(
            "❌ Only Owners can use this command.",
            ephemeral=True
        )
        return

    skin_url = f"https://mc-heads.net/player/{minecraft_username}/256"

    embed = discord.Embed(
        title="🏆 SharkSMP Rank Test",
        color=0x50C7FF
    )

    embed.add_field(
        name="👤 Player",
        value=user.mention,
        inline=False
    )

    embed.add_field(
        name="🎮 Minecraft Username",
        value=minecraft_username,
        inline=False
    )

    embed.add_field(
        name="🧪 Tester",
        value=interaction.user.mention,
        inline=False
    )

    embed.add_field(
        name="⚔️ Gamemode",
        value=gamemode.value,
        inline=True
    )

    embed.add_field(
        name="📜 Previous Rank",
        value=previous_rank.value,
        inline=True
    )

    embed.add_field(
        name="🏅 Rank Earned",
        value=new_rank.value,
        inline=True
    )

    embed.set_image(url=skin_url)

    embed.set_footer(
        text="SharkSMP Rank System"
    )

    await interaction.response.send_message(embed=embed)

    msg = await interaction.original_response()

    for emoji in ["👑", "🤯", "💀", "😂", "😭"]:
        await msg.add_reaction(emoji)

bot.tree.add_command(setrank)

bot.run(TOKEN)
