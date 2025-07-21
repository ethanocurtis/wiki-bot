import discord
from discord import app_commands
import wikipediaapi
import os
import openai

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not set in environment")

# Initialize OpenAI (optional)
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Initialize Discord bot
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Wikipedia API (with user agent required by Wikipedia)
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='WikiBot/1.0 (https://github.com/ethanocurtis/wiki-bot; contact: ethan@curtwurk.com)'
)


async def summarize_text(text, max_words=50):
    """Summarize text using OpenAI if available, otherwise truncate."""
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

    # Fallback: truncate if OpenAI isn't used
    return " ".join(text.split()[:max_words]) + "..."


# Global slash command (works everywhere, but may take time to show)
@tree.command(
    name="wiki",
    description="Search Wikipedia and get a short summary"
)
async def wiki_search(interaction: discord.Interaction, query: str):
    try:
        await interaction.response.defer(thinking=True)  # Show "thinking" indicator
        page = wiki.page(query)
        if not page.exists():
            await interaction.followup.send(f"❌ No results found for **{query}**.")
            return

        summary = await summarize_text(page.summary)
        await interaction.followup.send(f"**{page.title}**\n{summary}\n<{page.fullurl}>")

    except Exception as e:
        await interaction.followup.send(f"⚠️ An error occurred: `{e}`")
        print(f"Command error: {e}")


@bot.event
async def on_ready():
    await tree.sync()  # Global sync only
    print(f"🤖 Bot is online as {bot.user}")
    print("Global slash commands synced (may take up to 1 hour to appear).")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
