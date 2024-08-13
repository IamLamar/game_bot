import telebot
from telebot import types
from config import TOKEN
from main import varian_game
import psycopg2  
from datetime import datetime

conn = psycopg2.connect(dbname = 'game', user='lamar2', password='1234', host = 'localhost',port=5432)
cursor = conn.cursor()
conn.autocommit = True
# cursor.execute("create table game_bot1(id serial primary key, data varchar, time date)")
# print("yes")
# cursor.execute("select * from game_bot1")
# print(cursor.fetchall())

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])


def start_game(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("🪨")
    b2 = types.KeyboardButton("✂️")
    b3 = types.KeyboardButton("📄")
    menu.add(b1,b2,b3)
    bot.send_message(message.chat.id, f"Привет <b>{message.from_user.first_name}!</b> Давай поиграем в игру Камень - Ножницы - Бумага",reply_markup=menu,parse_mode='html')

@bot.message_handler(content_types=['text'])

def start_game(message):
    if message.chat.type == 'private':
        current_time = datetime.now()
        if message.text == "🪨":
            result = varian_game(1)
            cursor.execute("insert into game_bot1 (data,time) values (%s,%s)", (result,current_time))
            bot.send_message(message.chat.id, result)
        elif message.text == "✂️":
            result = varian_game(2)
            cursor.execute("insert into game_bot1 (data,time) values (%s,%s)", (result,current_time))
            bot.send_message(message.chat.id, result)
        elif message.text == "📄":
            result = varian_game(3)
            cursor.execute("insert into game_bot1 (data,time) values (%s,%s)", (result,current_time))
            bot.send_message(message.chat.id,result)
        else:
            bot.send_message(message.chat.id,"<b>введите корректные данные</b>",parse_mode='html')
       
bot.polling(non_stop=True)

cursor.close()
conn.close()