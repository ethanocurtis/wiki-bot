FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user for safety
RUN useradd -m botuser
USER botuser

# Environment variables (override via docker-compose or .env)
ENV DISCORD_TOKEN=""
ENV OPENAI_API_KEY=""

CMD ["python", "bot.py"]
