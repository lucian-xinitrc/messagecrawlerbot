# Engine 
FROM python:3.10-slim

# Working Directory
WORKDIR /app

# Copying files
COPY .env .
COPY bot.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Command that runs the bot
CMD ["python3", "bot.py"]
