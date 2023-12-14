import telebot
import os
from telebot.types import Message
import time
import mqtt
import tempfile
from datetime import datetime

TOKEN = os.getenv("TOKEN")


bot = telebot.TeleBot(TOKEN)
pending_responses =[]
@bot.message_handler(commands=['start'])
def start(message:Message):
    bot.send_message(message.chat.id,"hola soy un bot creado por David para ayudarte a regar tus plantas\n Si necesitas ayuda llama /help, para regar tus plantas dale /regar ") 
    
@bot.message_handler(commands=['help'])
def start(message:Message):
    bot.send_message(message.chat.id,"hola soy un bot creado por David para ayudarte a regar tus plantas\n Si necesitas ayuda llama /help, para regar tus plantas dale /regar \n /photo toma una foto de tus plantas") 
    
    
@bot.message_handler(commands=['regar'])
def regar(message:Message):
    bot.send_message(message.chat.id,"Voy a regar las plantas..") 
    pending_responses.append(message.chat.id)
    mqtt.regar()
    #time.sleep(10)
    #bot.send_message(message.chat.id,"Regue tus plantas con mucho amor") 

@bot.message_handler(commands=['photo'])
def photo(message:Message):
    bot.send_message(message.chat.id,"Veamos como va todo!!") 
    pending_responses.append(message.chat.id)
    mqtt.photo()
    #time.sleep(10)
    #bot.send_message(message.chat.id,"Regue tus plantas con mucho amor") 

#@bot.message_handler(func=lambda m:True)
@bot.message_handler(content_types=["text"])
def start(message:Message):
    bot.reply_to(message,message.text)
    
    
def on_message(client, userdata, msg):
    chat_id = pending_responses.pop()
    
    print(msg.topic)
    if msg.topic == "lorris_plants/regar/response":
        if 'ok' in str(msg.payload):
            bot.send_message(chat_id,"Regue tus plantas con mucho amor!!") 
        else:
            bot.send_message(chat_id,"Ocurrio un problema") 
            
    elif msg.topic == "lorris_plants/photo/response":

        file = "/images/"+str(datetime.now())+".jpg"
        with  open(file,"wb") as f:
            f.write(msg.payload)
            f.flush()
            
        bot.send_photo(chat_id,open(file,'rb'))
        ##print(msg.topic+" - "+str(msg.payload))
     
 
if __name__=="__main__":
    print("Iniciando Bot")

    bot.set_my_commands([
        telebot.types.BotCommand("/start","Bienvenida"),
        telebot.types.BotCommand("/help","Ayuda"),
        telebot.types.BotCommand("/regar","Riega las plantas"),
        telebot.types.BotCommand("/photo","Tomar foto")
        
    ])
    mqtt.connect(on_message)
    bot.polling(non_stop=True,restart_on_change=False)
    
