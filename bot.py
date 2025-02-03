import telebot
import openai
import os
from flask import Flask, request

# Carregar variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WEBHOOK_URL = f"https://seu-app-na-render.onrender.com/{TELEGRAM_BOT_TOKEN}"  # Altere para a URL do seu app na Render

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# Rota do webhook
@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

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
        print(f"Erro na API da OpenAI: {e}")
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar sua pergunta.")

# Configurar Webhook
@app.route("/")
def set_webhook():
    bot.remove_webhook()  # Remover qualquer webhook existente
    bot.set_webhook(url=WEBHOOK_URL)  # Definir o novo webhook
    return "Webhook configurado!", 200

# Iniciar servidor Flask
if __name__ == "__main__":
    # Certifique-se de que o polling não está sendo iniciado
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
