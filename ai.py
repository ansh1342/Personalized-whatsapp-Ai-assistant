import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(user, last_chats, message):

    name = user.get("name") if user else None
    preferences = user.get("preferences") if user else None

    system_prompt = "You are a helpful WhatsApp AI assistant."

    if name:
        system_prompt += f" The user's name is {name}."

    if preferences:
        system_prompt += f" User preferences: {preferences}."

    conversation = [{"role": "system", "content": system_prompt}]

    for chat in last_chats:
        conversation.append({"role": "user", "content": chat["user_message"]})
        conversation.append({"role": "assistant", "content": chat["bot_reply"]})

    conversation.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )

    return response.choices[0].message.content
