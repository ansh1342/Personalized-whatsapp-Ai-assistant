from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from db import get_user, create_user, save_chat, get_last_chats
from ai import generate_reply

app = Flask(__name__)

@app.route("/")
def home():
    return "WhatsApp AI Bot is Running Successfully!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    phone = request.values.get("From", "")

    create_user(phone)
    user = get_user(phone)

    last_chats = get_last_chats(phone, limit=5)

    bot_reply = generate_reply(user, last_chats, incoming_msg)

    save_chat(phone, incoming_msg, bot_reply)

    response = MessagingResponse()
    response.message(bot_reply)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
