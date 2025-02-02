import telebot
import openai
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

TELEGRAM_BOT_TOKEN = "8072657227:AAFZ5hvKtODzCA_r3KcdsLvDscw47C2Iupw" 
OPENAI_API_KEY = "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"

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
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar sua pergunta.")

bot.polling()
