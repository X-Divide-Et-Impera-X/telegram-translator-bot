from bot_token import TOKEN

from telebot.async_telebot import AsyncTeleBot
from gtts import gTTS
from googletrans import Translator
from langdetect import detect
import os
import re
import asyncio

bot = AsyncTeleBot(TOKEN)


# Handle /start command
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, "Send me some Russian text, and I'll convert it to speech and provide an English translation!")

# Handle text messages
@bot.message_handler(content_types=['text', 'photo', 'video'])
async def handle_text(message):
    async with Translator() as translator:

        if message.content_type != 'text':
            text = message.caption
            print(text, text is not None)
            if not text: return
        else:
            text = message.text

        lang = detect(text)

        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)

        # Translate Russian to English
        translation = await translator.translate(text, src=lang, dest='en')

        translated_text = translation.text

        # Send the audio file
        with open(audio_file, 'rb') as audio:
            await bot.send_audio(message.chat.id, audio, caption=translated_text)


        # Clean up the audio file
        os.remove(audio_file)


asyncio.run(bot.polling())
