import os
import telebot
from telebot.types import InlineKeyboardButton
import global_var as gv
import database_backend

os.system('cls' if os.name=='nt' else 'clear')

API_KEY = os.getenv("API_KEY") if os.getenv("API_KEY")!=None else "5406129862:AAGv2A-45MrAqqvUVo6aLfwqzOQqdT7nJVk"
bot = telebot.TeleBot(API_KEY)  
 
Gender = telebot.types.InlineKeyboardMarkup()
Quota = telebot.types.InlineKeyboardMarkup()

GENDER = {
    "Male 👦🏻" : "Male",
    "Female 👩🏻" : "Female"
}

QUOTA = {
    "General" : "GEN",
    "EWS" : "EWS",
    "OBC-NCL": "OBC",
    "SC" : "SC",
    "ST" : "ST",
}

genders = list(GENDER.keys())
quotas = list(QUOTA.keys())

Gender.add(
    InlineKeyboardButton(genders[0],callback_data=genders[0]),
    InlineKeyboardButton(genders[1],callback_data=genders[1])
    )

Quota.add(
    InlineKeyboardButton(quotas[0],callback_data=quotas[0]),
    InlineKeyboardButton(quotas[1],callback_data=quotas[1]),
    InlineKeyboardButton(quotas[2],callback_data=quotas[2]),
    InlineKeyboardButton(quotas[3],callback_data=quotas[3]),
    InlineKeyboardButton(quotas[4],callback_data=quotas[4])
    )
@bot.message_handler(commands=['start'])
def start(message):
    msg = r"""*FocusRankNavigator* simplifies the college selection process based on your JEE Mains and Advanced Ranks\. Just provide your ranks, and *FocusRankNavigator* will swiftly generate a tailored list of colleges that match your eligibility\.
    
For more info contact [Saikat Das](https://saikat.in)"""

    bot.send_photo(chat_id=message.chat.id, caption=msg, photo=open("data/pfp.jpg","rb"), parse_mode="MarkdownV2")
    sent_name = bot.send_message(chat_id=message.chat.id,text="Could you kindly share your name with me?")

    bot.register_next_step_handler(sent_name, name)

def name(message):
    gv.stud_name = message.text
    bot.send_message(chat_id=message.chat.id,text="What is your gender?",reply_markup=Gender)

def jee_mains(message):
    gv.main_rank = message.text
    msg = r"""📌 *Note:* Please Provide your __Category Rank__ _\(If you belong to any category, else give CRL Rank\)_
If you are not qualified please enter 0\."""
    bot.send_message(chat_id=message.chat.id,text=r"*What is your JEE Advance Rank?*", parse_mode="MarkdownV2")
    send_advance = bot.send_message(chat_id=message.chat.id,text=msg, parse_mode="MarkdownV2")
    bot.register_next_step_handler(send_advance, jee_advance)

def jee_advance(message):
    gv.advance_rank = message.text
    database_backend.database_backend()

    filename_main = f'output/{gv.quota}_{gv.stud_name}_mains_{gv.main_rank}.csv'
    filename_advance = f'output/{gv.quota}_{gv.stud_name}_advance_{gv.advance_rank}.csv'
    filename_csab = f'output/{gv.quota}_{gv.stud_name}_csab_{gv.main_rank}.csv'

    bot.send_document(chat_id=message.chat.id,data =open(filename_main, 'rb'))
    try:
        bot.send_document(chat_id=message.chat.id,data =open(filename_advance, 'rb'))
    except Exception as e: pass
    bot.send_document(chat_id=message.chat.id,data =open(filename_csab, 'rb'))

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data in GENDER.keys():
        gv.gender = GENDER.get(call.data)
        bot.send_message(chat_id=call.message.chat.id,text="Which Category you belong to?",reply_markup=Quota)

    if call.data in QUOTA.keys():
        gv.quota = QUOTA.get(call.data)

        msg = r"""📌 *Note:* Please Provide your __Category Rank__ _\(If you belong to any category, else give CRL Rank\)_"""

        bot.send_message(chat_id=call.message.chat.id,text=r"*What is your JEE Mains Rank?*", parse_mode="MarkdownV2")
        send_main = bot.send_message(chat_id=call.message.chat.id,text=msg, parse_mode="MarkdownV2")
        bot.register_next_step_handler(send_main, jee_mains)    

bot.polling()