import os, psycopg, base64
from Crypto.Cipher import AES
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()

last_cache = None
def decrypt(ciphertext_b64):
	cipher = AES.new(os.getenv('encryption_key').encode(), AES.MODE_ECB)
	decrypted = cipher.decrypt(base64.b64decode(ciphertext_b64))
	pad = decrypted[-1]
	return decrypted[:-pad].decode('utf-8')

db = os.getenv('db_url')
conn = pyscopg2.connect(db)
cur = conn.cursor()
msg = ""
author = ""
id = 13543
while(msg != "u dont like the idea?"):
	cur.execute("SELECT author, message FROM public.last_message WHERE id = %s",
		(id,))
	row = cur.fetchone()
	auth, last_msg = row
	msg = decrypt(msg)
	author = decrypt(auth)
	if(author == "Tuuxa"):
		print(msg)
	id -= 1