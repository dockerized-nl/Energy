import pytz
from aiogram import Bot, Dispatcher, types
import rich
import telebot
import os
from datetime import timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import psutil
import subprocess


def handle_response():
    current_date = datetime.now(pytz.timezone('Europe/Amsterdam'))
    yesterday = current_date + timedelta(days=-1)

    URL = f"https://api.energyzero.nl/v1/energyprices?fromDate={yesterday.strftime('%Y-%m-%d')}T23:00:00.000Z&tillDate={current_date.strftime('%Y-%m-%d')}T23:00:00.000Z&interval=4&usageType=1&inclBtw=true"
    page = requests.get(URL)

    output_page = page.json()

    output = ""
    average = output_page['average']


    for item in output_page['Prices']:
        hour = int(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
        hour += 1
        if hour == 24:
            hour = 00
        elif hour == 25:
            hour = 1
        output += f"Tijd: {hour} Prijs: {item['price']}"
        output += "\n"
    labels = []
    values = []

    for item in output_page['Prices']:
        labels.append(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
        values.append(item['price'])

    return output

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['prijs'])
def logo(message: types.Message):
    current_date = datetime.now(pytz.timezone('Europe/Amsterdam'))
    output = handle_response()
    bot.send_photo(message.chat.id, open(
        f"/app/images/price_plot_{current_date.strftime('%Y-%m-%d')}.png", "rb"))
    bot.reply_to(message, f"{output}")

@bot.message_handler(commands=['help'])
def welcome(message: types.Message):
    bot.reply_to(message, "Using /disk /sysinfo /uptime /server ")

# disk usage (/disk)
@bot.message_handler(commands=['disk'])
def disk(message):
    diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))
    diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
    diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
    diskPercent = psutil.disk_usage('/').percent

    msg = '''
Disk Info
---------
Total = {} GB
Used = {} GB
Avail = {} GB
Usage = {} %\n'''.format(diskTotal,diskUsed,diskAvail,diskPercent)
    bot.send_message(message.chat.id,msg)


# cpu & ram (/sysinfo)
@bot.message_handler(commands=['sysinfo'])
def sysinfo(message):
    cpuUsage = psutil.cpu_percent(interval=1)
    ramTotal = int(psutil.virtual_memory().total/(1024*1024)) #GB
    ramUsage = int(psutil.virtual_memory().used/(1024*1024)) #GB
    ramFree = int(psutil.virtual_memory().free/(1024*1024)) #GB
    ramUsagePercent = psutil.virtual_memory().percent
    msg = '''
CPU & RAM Info
---------
CPU Usage = {} %
RAM
Total = {} MB
Usage = {} MB
Free  = {} MB
Used = {} %\n'''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)
    bot.send_message(message.chat.id,msg)

# uptime (/uptime)
@bot.message_handler(commands=['uptime'])
def uptime(message):
    upTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')
    msg = upTime
    bot.send_message(message.chat.id,msg)


# server desc (/server)
@bot.message_handler(commands=['server'])
def server(message):
    uname = subprocess.check_output(['uname','-rsoi']).decode('UTF-8')
    host = subprocess.check_output(['hostname']).decode('UTF-8')
    ipAddr = subprocess.check_output(['hostname','-I']).decode('UTF-8')
    msg ='''
Server Desc
---------
OS = {}
Hostname = {}
IP Addr = {}'''.format(uname,host,ipAddr)
    bot.send_message(message.chat.id,msg)

bot.infinity_polling()