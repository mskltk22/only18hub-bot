import telebot
from telebot import types
from flask import Flask, request
import json
import os

app = Flask(__name__)
TOKEN = "8445609804:AAEinBdJUcWfd4qKIPVUkCidFr_0DZWoSmY"
bot = telebot.TeleBot(TOKEN)

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"verified": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

stats = load_stats()

ADMIN_ID = 7203856546  # رقم حسابك

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'ok'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🔞 I'm 18+ | Enter", callback_data="verify")
    markup.add(btn)
    
    bot.send_message(message.chat.id,
        "🔞 *ADULT CONTENT (18+ ONLY)*\n\n"
        "You must be 18 or older to access.\n"
        "Click the button below to confirm.",
        parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global stats
    
    if call.data == "verify":
        stats["verified"] += 1
        save_stats(stats)
        
        markup = types.InlineKeyboardMarkup()
        link_btn = types.InlineKeyboardButton("🚪 Open Private Link", url="https://cfzy.us/s/ITy2fqT")
        markup.add(link_btn)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="✅ Age verified!\n\nYour private link is ready 👇",
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, 
            f"📊 *Bot Statistics*\n\n"
            f"🔞 Total verified users: `{stats['verified']}`\n"
            f"🕐 Since last reset",
            parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ Unauthorized")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RENDER_SERVICE_ID', 'only18hub-bot')}.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
