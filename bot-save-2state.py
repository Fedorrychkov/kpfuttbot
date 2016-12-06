# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
#from mysqlconnector import connect

import mysql.connector
from mysql.connector import Error
import datetime
import botan

now = datetime.datetime.now()
print ("Текущий день: %d" % now.day)
weeknumber=now.strftime("%W")
today=now.strftime("%w")
datenow=now.strftime("%d-%m-%Y")
tommorow=int(today)+1
print ("Номер недели: ", weeknumber)
print ("Номер дня: ", today)
print ("Дата: ", datenow)
group=4081
nameweek=''

def evod():
	global today, weeknumber
	evod=0
	dopweek=0
	if float(today)>6:
		dopweek=float(weeknumber);weeknumber=dopweek+1
	if float(weeknumber)%2==0:
		evod=2
	else:
		evod=1
	return evod

def nameweek():
	evod=0
	if float(weeknumber)%2==0:
		nameweek='чётная неделя'
	else:
		nameweek='нечётная неделя'
	return nameweek

errorf = 'kfubot находится на стадии альфа тестирования, в рабочем режиме находится только Фундаментальная информатика и информационные технологии'
donee = "В разработке"

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
	/mysettings - команда для настройки вашего расписания. \n/allweek - вывод расписания по дням. ''' 

	bot.send_message(message.chat.id, starttext + "\nКстати, сейчас {name} ;)".format(name=nameweek()))
	thisUsername=message.chat.username
	thisChatID=message.chat.id
		
	"""bot_reply=''
	cur.execute("SELECT UserID FROM users  WHERE UserID=%d" % thisChatID)
	result=cur.fetchall()
	if result==[]:
		#newUser=bot.send_message(message.chat.id, "Добро пожаловать! Так как вы зашли первый раз вам придётся пройти небольшую процедуру настройки своего аккаунта!\nПриступим!")
		bot.send_message(message.chat.id, "Добро пожаловать! Так как вы зашли первый раз вам придётся пройти небольшую процедуру настройки своего аккаунта!\nПриступим!")
		register1(message)
"""
	register1(message)
	botan.track(config.botan_key, message.chat.id, message, 'type /start or /help')
	return


    
#@bot.message_handler(commands=['new'])
def register1(message):
	markup = types.ReplyKeyboardMarkup()
	bot_reply=''
	thisUsername=message.chat.username
	thisChatID=message.chat.id
	cur.execute("SELECT InstID, InstName FROM institute")
	result=cur.fetchall()
	for row in result:
		bot_reply+=str(row[0])+' '+str(row[1])+"\n"
		print (bot_reply)
		markup.row(str(row[1]))
		
	bot.send_message(message.chat.id, "Выберите свой институт из списка доступных: ", reply_markup=markup)

#@bot.message_handler(commands=['settings'])
#def handle_settings(message):
#	return
def register2(message):
	bot.send_message(message.chat.id, "Регистрация2")
@bot.message_handler(commands=['fastset'])
def get(message):
	sent=bot.send_message(message.chat.id, "Введите номер своей группы вместе с подгруппой. Например: 409 или 4081 (группа 408, подгруппа 1)")
	bot_reply=''
	groups=message.text
	bot.register_next_step_handler(sent, hello)

def hello(message):
    #bot.send_message(message.chat.id, 'Привет, {name}. Рад тебя видеть вновь!'.format(name=message.text))
    global group
    myg=message.text
    group=int(myg)
    print (myg)
#	get_answer
def connect():
	try:
		con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
		cur=con.cursor()
	except Error as e:
		print(e)
	finally:
		con.close()

@bot.message_handler(commands=['allweek'])
def handle_allweek(message):
	markup = types.ReplyKeyboardMarkup()
	markup.row('Понедельник','Вторник')
	markup.row('Среда','Четверг')
	markup.row('Пятница','Суббота')
	print (message.text, "команда allweek")
	bot.send_message(message.chat.id, "Выберите день который вы хотите проверить:", reply_markup=markup)
	botan.track(config.botan_key, message.chat.id, message, 'Type command /allweek')
	handle_words(message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_words(message):
	day_name=''
	none_day=''
	bot_reply=''
	aint=message.text
	cur.execute("SELECT InstID, InstName FROM institute")
	result=cur.fetchall()
	for row in result:
		if aint==str(row[1]):
			print (aint)
			register2(message)
	if aint=='Понедельник' or aint=='Вторник' or aint=='Среда' or aint=='Четверг' or aint=='Пятница' or aint=='Суббота':
		day_name=message.text
		none_day=''
		print (message.text, "Слова дней недели")
		handle_days(message)
	elif aint=='Сегодня':
		handle_today(message)
	elif aint=='Завтра':
		handle_allweek(message)
	elif aint[0]=="/":
		error_text=''
	else:
		error_text='... Ай, что то пошло не так:( '
		bot.send_message(message.chat.id, "%s" % error_text)
	

	#connect()
	

def handle_days(message):
	bot_reply=''
	day_name=message.text
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod, DayName FROM timetable, alllessons, Days  WHERE lessid=alllessons.id and DayName='%s' and DayID=DayNum and GroupNum='%d' and (evod=0 or evod=%d)" % (day_name, group, evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на %s" % day_name)
	if result==[]:
		bot.send_message(message.chat.id, "В этот день у вас занятий нет!")	
	else:
		for row in result:
			bot_reply+="с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"
			print (bot_reply)
	bot.send_message(message.chat.id, bot_reply)
	botan.track(config.botan_key, message.chat.id, message, 'Request TT from /allweek all type Dayname')

@bot.message_handler(commands=['today'])
def handle_today(message):
	bot_reply=''
	#connect()
	cur.execute("SELECT timelist, lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=%s and (evod=0 or evod=%d)" % (group, today,evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на сегодня:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply+="с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"
			print (bot_reply)
	bot.send_message(message.chat.id, bot_reply)
	botan.track(config.botan_key, message.chat.id, message, 'Type /today command or Сегодня')
	
@bot.message_handler(commands=['tommorow'])
def handle_tommorow(message):
	bot_reply=''
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=%s and (evod=0 or evod=%d)" % (group, tommorow,evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на завтра:")
	if result==[]:
		bot.send_message(message.chat.id, "Завтра у вас занятий нет!")	
	else:
		for row in result:
			bot_reply+="с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"
			print (bot_reply)
	bot.send_message(message.chat.id, bot_reply)
	botan.track(config.botan_key, message.chat.id, message, 'Type /tommorow command or Завтра')



if __name__ == '__main__':
     bot.polling(none_stop=True)
     connect()
