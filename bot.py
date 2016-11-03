# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
#from mysqlconnector import connect

import mysql.connector
from mysql.connector import Error

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
goodbuy_text = 'Текст, который будет выводиться, когда юзер выходит из чата'
#replylist=['ff']
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	starttext ='''KPFU Time Table Bot предназначен для студентов Казанского Приволжского Федерального Университета. 
	На данный момент KPFUttBot находится в альфа версии. Сейчас поддерживается только 1 институт, 1 факультет и 1 группа. 
	09-408. \nСписок Команд:\n/today -вывод расписания на сегодня.\n/tommorow - вывод расписания на завтра.\n
	/alltt - вывод расписания на всю неделю.'''
	bot.send_message(message.chat.id, starttext)


@bot.message_handler(commands=['alltt'])
def handle_alltt(message):
	bot_reply=[]
	connect()
	cur.execute("SELECT * FROM lessons WHERE DayID=1 and GroupNum='408.1'")
	result=cur.fetchall()
	for row in result:
		bot_reply=(row[6]+", "+row[7]+", "+row[9]+", "+str(row[8])+"\n")
		#print (bot_reply)
		bot.send_message(message.chat.id, bot_reply)



def connect():
	try:
		con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
		cur=con.cursor()
	except Error as e:
		print(e)
	finally:
		con.close()


if __name__ == '__main__':
     bot.polling(none_stop=True)
     connect()
