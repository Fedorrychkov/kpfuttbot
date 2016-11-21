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
today=now.strftime("%w")
datenow=now.strftime("%d-%m-%Y")

tommorow=int(today)+1
daynumbert=1
print ("Номер недели: ", weeknumber)
print ("Номер дня: ", today)
print ("Дата: ", datenow)
group=4081

def evod():
	evod=0
	if float(weeknumber)%2==0:
		evod=2
	else:
		evod=1
	return evod
	
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
	/alltt - вывод расписания на всю неделю.\n/mysettings - команда для настройки вашего расписания. \n/allweek - вывод расписания по дням.'''
	bot.send_message(message.chat.id, starttext)

@bot.message_handler(commands=['today'])
def handle_alltt(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist, lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=%s and (evod=0 or evod=%d)" % (group, today,evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на сегодня:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)

@bot.message_handler(commands=['tommorow'])
def handle_alltt(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=%s and (evod=0 or evod=%d)" % (group, tommorow,evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на завтра:")
	if result==[]:
		bot.send_message(message.chat.id, "Завтра у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
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

@bot.message_handler(commands=['allweek'])
def handle_start_help(message):
	markup = types.ReplyKeyboardMarkup()
	'''markup.row('Бизнес информатика', 'Прикладная математика и информатика')
	markup.row('Прикладная математика','Програмная инженерия')
	markup.row('Фундаментальная информатика и ИТ', 'Информационная безопасность')
	markup.row('Прикладная информатика','Информационные системы и технологии')
	bot.send_message(message.chat.id, "Выберите факультет:", reply_markup=markup)'''
	markup.row('Понедельник','Вторник')
	markup.row('Среда','Четверг')
	markup.row('Пятница','Суббота')
	bot.send_message(message.chat.id, "Выберите день который вы хотите проверить:", reply_markup=markup)


def connect():
	try:
		con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
		cur=con.cursor()
	except Error as e:
		print(e)
	finally:
		con.close()




@bot.message_handler(regexp="Понедельник")
def handle_message(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=1 and (evod=0 or evod=%d)" % (group, evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на Понедельник:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)


@bot.message_handler(regexp="Вторник")
def handle_message(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=2 and (evod=0 or evod=%d)" % (group, evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на Вторник:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)


@bot.message_handler(regexp="Среда")
def handle_message(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=3 and (evod=0 or evod=%d)" % (group, evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на Среду:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)


@bot.message_handler(regexp="Четверг")
def handle_message(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=4 and (evod=0 or evod=%d)" % (group, evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на Четверг:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)


@bot.message_handler(regexp="Пятница")
def handle_message(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=5 and (evod=0 or evod=%d)" % (group,evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на Пятницу:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)


@bot.message_handler(regexp="Суббота")
def handle_message(message):
	bot_reply=[]
	#connect()
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod FROM timetable, alllessons  WHERE lessid=alllessons.id and GroupNum='%d' and DayNum=6 and (evod=0 or evod=%d)" % (group,evod()))
	result=cur.fetchall()
	bot.send_message(message.chat.id, "Расписание на Субботу:")
	if result==[]:
		bot.send_message(message.chat.id, "Сегодня у вас занятий нет!")	
	else:
		for row in result:
			bot_reply=["с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"]
			print (bot_reply)
			bot.send_message(message.chat.id, bot_reply)




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
