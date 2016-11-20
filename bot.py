# -*- coding: utf-8 -*-

import config
import telebot
from telebot import types
#from mysqlconnector import connect

import mysql.connector
from mysql.connector import Error

import datetime
import time
now = datetime.datetime.now()

print ("Текущий день: %d" % now.day)
weeknumber=now.strftime("%W")
daynumber=now.strftime("%w")
datenow=now.strftime("%d-%m-%Y")
daynumbert=1
#print (now.strftime("Week: %W, %w, %d-%m-%Y "))
print ("Номер недели: ", weeknumber)
print ("Номер дня: ", daynumber)
print ("Дата: ",	datenow)

#print (datetime.isoweekday("Today: "))
"""from telegram import Updater, Emoji, ParseMode
import telegram
from time import sleep
import logging
import requests, json
import urllib.request, urllib.parse,urllib
import urllib.request
import re, sys, os, platform
import random  as  random_number"""

con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
cur=con.cursor()
	

#help_text = '8:30-10:00, Математический Анализ, 108 \n 10:10-11:40, Теория вероятности, 1008 \n 11:50-13:20, Математический Анализ, 903'
welcome_text = 'Текст, который будет выводиться, когда юзер заходит в чат'
#replylist=['ff']
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	starttext ='''KPFU Time Table Bot предназначен для студентов Казанского Приволжского Федерального Университета. 
	На данный момент KPFUttBot находится в альфа версии. Сейчас поддерживается только 1 институт, 1 факультет и 1 группа. 
	09-408. \nСписок Команд:\n/today -вывод расписания на сегодня.\n/tommorow - вывод расписания на завтра.\n
	/alltt - вывод расписания на всю неделю.\n/mytt - команда для настройки вашего расписания.'''
	bot.send_message(message.chat.id, starttext)

@bot.message_handler(commands=['today'])
def handle_alltt(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT * FROM lessons WHERE GroupNum='408.1' and DayID=%s" % daynumber)
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на: " + datenow)
	for row in result:
		bot_reply=(row[6]+", "+row[7]+", "+row[9]+", "+str(row[8])+"\n")
		bot.send_message(message.chat.id, bot_reply)

@bot.message_handler(commands=['mysettings'])
def handle_start_help(message):
	markup = types.ReplyKeyboardMarkup()
	'''markup.row('Бизнес информатика', 'Прикладная математика и информатика')
	markup.row('Прикладная математика','Програмная инженерия')
	markup.row('Фундаментальная информатика и ИТ', 'Информационная безопасность')
	markup.row('Прикладная информатика','Информационные системы и технологии')
	bot.send_message(message.chat.id, "Выберите факультет:", reply_markup=markup)'''
	markup.row('408.1','408.2')
	bot.send_message(message.chat.id, "Выберите группу\подгруппу:", reply_markup=markup)
	
	print (reply_markup)



def connect():
	try:
		con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
		cur=con.cursor()
	except Error as e:
		print(e)
	finally:
		con.close()

errorf = 'kfubot находится на стадии альфа тестирования, в рабочем режиме находится только Фундаментальная информатика и информационные технологии'
donee = "В разработке"
@bot.message_handler(regexp="Бизнес информатика")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Прикладная математика и информатика")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Прикладная информатика")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Прикладная математика")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Програмная инженерия")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Информационная безопасность")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Информационные системы и технологии")
def handle_message(message):
		bot.send_message(message.chat.id, errorf)
@bot.message_handler(regexp="Фундаментальная информатика и ИТ")
def handle_message(message):
		bot.send_message(message.chat.id, donee)


if __name__ == '__main__':
     bot.polling(none_stop=True)
     connect()
