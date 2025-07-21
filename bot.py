import discord
from discord import app_commands
import wikipediaapi
import os
import openai

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GUILD_ID = 123456789012345678  # Replace with your Discord server ID

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not set in environment")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Discord bot
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Wikipedia API with a required user agent
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='WikiBot/1.0 (https://github.com/ethanocurtis/wiki-bot; contact: ethan@curtwurk.com)'
)


async def summarize_text(text, max_words=50):
    """Summarize text with OpenAI if available, otherwise truncate."""
    if OPENAI_API_KEY:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Summarize this text in {max_words} words or less, concise and factual:\n{text}",
                max_tokens=120,
                temperature=0.3
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")

    return " ".join(text.split()[:max_words]) + "..."


# Slash command (guild + global registration)
@tree.command(
    name="wiki",
    description="Search Wikipedia and get a short summary",
    guild=discord.Object(id=GUILD_ID)  # Instant sync in your server
)
async def wiki_search(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    page = wiki.page(query)
    if not page.exists():
        await interaction.followup.send(f"❌ No results found for **{query}**.")
        return
    summary = await summarize_text(page.summary)
    await interaction.followup.send(f"**{page.title}**\n{summary}\n<{page.fullurl}>")


@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await tree.sync(guild=guild)  # Fast sync for your server
    await tree.sync()             # Global sync (for other servers, may take time)
    print(f"🤖 Bot is online as {bot.user}")
    print("Slash commands synced (guild + global).")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
