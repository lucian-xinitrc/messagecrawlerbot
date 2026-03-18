import os, disnake, requests, psycopg2, base64
from disnake.ext import tasks
from Crypto.Cipher import AES
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()

bot = commands.Bot(
	intents=disnake.Intents.all(), 
	allowed_mentions=disnake.AllowedMentions(everyone=True)
)

last_cache = None
def decrypt(ciphertext_b64):
	    cipher = AES.new(os.getenv('encryption_key').encode(), AES.MODE_ECB)
	    decrypted = cipher.decrypt(base64.b64decode(ciphertext_b64))
	    pad = decrypted[-1]
	    return decrypted[:-pad].decode('utf-8')

@tasks.loop(seconds=2)
async def watcher():
	global last_cache
	try
		db = os.getenv('db_url')
		conn = psycopg2.connect(db)
		cur = conn.cursor()

		cur.execute("SELECT author, message FROM public.last_message WHERE id = 1")
		row = cur.fetchone()

		cur.close()
		conn.close()
		if not row:
		    return

		if row != last_cache:
		    last_cache = row

		    author, msg = row
		    channel = bot.get_channel(1473044902492246219)
		    decryptedMsg = decrypt(msg)
		    check = True
		    if channel:
		        for word in ["login", "register", "msg", "/give"]:
		        	if word in decryptedMsg:
		        		check = False
		        		break
		        if check:
		        	await channel.send(f"**{decrypt(author)}**: {decrypt(msg)}")

	except:
		print("[ PostgreSQL - issue ] Issues with postgresSQL data retrieval")


try:
	watcher.start()
except:
	print("No message intercepted, still searching.")
  
@bot.event
async def on_ready():
	activity = disnake.Game(name="Scanning for messages...")
	await bot.change_presence(status=disnake.Status.idle, activity=activity)

if __name__ == "__main__":
	bot.run(os.getenv('bot_token'))