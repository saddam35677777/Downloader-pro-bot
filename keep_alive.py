from flask import Flask
import threading
from config import PORT

app = Flask(__name__)

@app.route('/')
def home():
    return "Pro Media Downloader Bot is Alive!", 200

def run():
    app.run(host='0.0.0.0', port=PORT)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
