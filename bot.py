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

# Initialize OpenAI client (v1.x style)
client = None
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not set. Bot will only return truncated Wikipedia summaries.")
else:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    print("✅ OpenAI API key loaded. AI features enabled.")

# Initialize Discord bot
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Wikipedia API client
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='WikiBot/1.0 (https://github.com/ethanocurtis/wiki-bot; contact: ethan@curtwurk.com)'
)

async def summarize_with_openai(text, max_words=50):
    """Summarize text using GPT-3.5-turbo if API key is available, else truncate."""
    if client:
        try:
            print("🔹 Using OpenAI to summarize text...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Summarize the following text in {max_words} words or fewer, factual and concise."},
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error (summary): {e}")
            return f"⚠️ OpenAI summarization failed: `{e}`"

    # Fallback: simple truncation
    return " ".join(text.split()[:max_words]) + "..."

async def ask_openai_question(question):
    """Ask GPT-3.5-turbo any question if Wikipedia has no answer or for /ask."""
    if not client:
        return "❌ I couldn't find anything on Wikipedia, and OpenAI is not configured."
    try:
        print(f"🔹 Using OpenAI to answer question: {question}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a factual assistant. Answer concisely and clearly."},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error (question): {e}")
        return f"⚠️ OpenAI request failed: `{e}`"

# /wiki command: Wikipedia + AI fallback
@tree.command(
    name="wiki",
    description="Search Wikipedia and get a short summary, or ask AI if no page is found."
)
async def wiki_search(interaction: discord.Interaction, query: str):
    try:
        await interaction.response.defer(thinking=True)  # Show "thinking" indicator
        page = wiki.page(query)

        if page.exists():
            summary = await summarize_with_openai(page.summary)
            await interaction.followup.send(f"**{page.title}**\n{summary}\n<{page.fullurl}>")
        else:
            ai_answer = await ask_openai_question(query)
            await interaction.followup.send(f"**No Wikipedia page found for '{query}'.**\nHere’s what I found:\n{ai_answer}")

    except Exception as e:
        await interaction.followup.send(f"⚠️ An error occurred in /wiki: `{e}`")
        print(f"Command error (/wiki): {e}")

# /ask command: Direct AI Q&A
@tree.command(
    name="ask",
    description="Ask GPT-3.5-turbo any question directly (bypasses Wikipedia)."
)
async def ask_ai(interaction: discord.Interaction, question: str):
    try:
        await interaction.response.defer(thinking=True)
        ai_answer = await ask_openai_question(question)
        await interaction.followup.send(f"**AI Answer:**\n{ai_answer}")
    except Exception as e:
        await interaction.followup.send(f"⚠️ An error occurred in /ask: `{e}`")
        print(f"Command error (/ask): {e}")

@bot.event
async def on_ready():
    await tree.sync()
    print(f"🤖 Bot is online as {bot.user}")
    print("Global slash commands synced (may take up to 1 hour to appear).")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
