# WikiBot

![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-0db7ed?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

WikiBot is a lightweight Discord bot that fetches **concise answers from Wikipedia**, and optionally uses **OpenAI GPT-3.5** as a fallback when:
- A topic isn’t found on Wikipedia.
- You want to ask general questions directly via `/ask`.

It’s simple to set up and runs via **Docker** or directly with Python.

---

## Features

- `/wiki <query>` – Searches Wikipedia for the topic and returns:
  - Title
  - Short summary (AI-generated if OpenAI is configured, otherwise truncated)
  - Link to the full page
  - Falls back to GPT-3.5 if no Wikipedia page exists.
- `/ask <question>` – Asks GPT-3.5 directly for concise, factual answers.
- Works **with or without OpenAI** (GPT-3.5 used only if API key is provided).
- Docker-ready for easy deployment.

---

## Requirements

- Python 3.9+
- Discord bot token
- (Optional) OpenAI API key (for enhanced summaries and AI Q&A)
- `docker` & `docker-compose` (if running via container)

---

## Setup (Manual)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ethanocurtis/wiki-bot.git
   cd wiki-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**

   Create a `.env` file in the project root:

   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here  # Optional
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

---

## Setup (Docker)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d --build
   ```

2. Environment variables can be set in your `.env` file (Docker will load it automatically).

---

## Usage

Invite your bot to a server (with `applications.commands` scope) and use:

- `/wiki python programming` → Wikipedia summary + link  
- `/wiki obscure topic` → Falls back to GPT-3.5 if not found  
- `/ask What is the capital of France?` → GPT-3.5 answer directly

The bot will display “thinking…” while fetching/summarizing results.

---

## Permissions

When inviting your bot, make sure it has:
- `applications.commands`
- `Send Messages`
- `Read Messages`
- `Use Slash Commands`

---

## Notes

- **Without OpenAI API key:**  
  - Summaries are truncated to 50 words (no GPT).
  - `/ask` will return a message saying AI isn’t configured.

- **With OpenAI API key:**  
  - GPT-3.5 is used for concise summaries and direct Q&A.
  - Each summary uses ~50–150 tokens; Q&A may use up to ~300 tokens (see OpenAI pricing).

---

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For issues, questions, or suggestions, feel free to contact me:  
[![Discord](https://img.shields.io/badge/Message%20me%20on%20Discord-ethanocurtis-5865F2?logo=discord&logoColor=white)](https://discordapp.com/users/167485961477947392)