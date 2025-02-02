import telebot
import openai
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
print(f"TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN}")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Função para responder mensagens
@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response['choices'][0]['message']['content'])
    except Exception as e:
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar sua pergunta.ok?")

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

# Iniciar o Flask em uma thread separada
threading.Thread(target=run_flask).start()

bot.polling()
