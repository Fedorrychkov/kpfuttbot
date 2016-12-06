# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
#from mysqlconnector import connect

import mysql.connector
from mysql.connector import MySQLConnection, Error
import datetime
import botan

now = datetime.datetime.now()
weeknumber=now.strftime("%W");today=now.strftime("%w");datenow=now.strftime("%d-%m-%Y");tommorow=int(today)+1
print ("Номер недели: ", weeknumber);print ("Номер дня: ", today);print ("Дата: ", datenow)
group=0
nameweek=''
thisUsername=''
thisChatID=0
userInstitute=''
userInstID=0
regUser=True
regInst=False
regFac=False
regCourse=False
regGroup=False

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
con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
cur=con.cursor()
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	global regUser, thisUsername, thisChatID, regInst, regFac, regCourse, regGroup
	starttext ='''KPFU Time Table Bot предназначен для студентов Казанского Приволжского Федерального Университета. 
	На данный момент KPFUttBot находится в альфа версии. Сейчас поддерживается только 1 институт, 1 факультет и 1 группа. 
	09-408. \nСписок Команд:\n/today -вывод расписания на сегодня.\n/tommorow - вывод расписания на завтра.\n
	/mysettings - команда для настройки вашего расписания. \n/allweek - вывод расписания по дням. ''' 

	bot.send_message(message.chat.id, starttext + "\nКстати, сейчас {name} ;)".format(name=nameweek()))
	thisUsername=message.chat.username
	thisChatID=message.chat.id
		
	bot_reply=''
	cur.execute("SELECT UserID FROM users  WHERE UserID=%d" % thisChatID)
	result=cur.fetchall()
	if result==[]:
		regUser=False
		regInst=False
		regFac=False
		regCourse=False
		regGroup=False
		newuser(message)

	botan.track(config.botan_key, message.chat.id, message, 'type /start or /help')
	return


    
#@bot.message_handler(commands=['new'])
def newuser(message):
	#newUser=bot.send_message(message.chat.id, "Добро пожаловать! Так как вы зашли первый раз вам придётся пройти небольшую процедуру настройки своего аккаунта!\nПриступим!")
	bot.send_message(message.chat.id, "Добро пожаловать! Так как вы зашли первый раз вам придётся пройти небольшую процедуру настройки своего аккаунта!\nПриступим!")
	if regInst==False:
		register1(message)
	elif regFac==False:
		register2(message)

def register1(message):
	global regUser, thisUsername, thisChatID, userInstitute, regInst, userInstID
	markup = types.ReplyKeyboardMarkup()
	bot_reply=''
	cur.execute("SELECT InstID, InstName FROM institute")
	result=cur.fetchall()
	for row in result:
		bot_reply+=str(row[1])+"\n"
		markup.row(str(row[1]))
	print ("Нахожусь в register1")
	bot.send_message(message.chat.id, "Выберите свой институт из списка доступных: ", reply_markup=markup)
	userInstitute=message.text #написать обработчик и сравнивать данные из бд и тут.
	print (userInstitute, "из Reg1")
	if userInstitute[0]!='/':
		bot.send_message(message.chat.id, userInstitute)
		cur.execute("SELECT InstID, InstName FROM institute WHERE InstName='%s'" % userInstitute)
		result2=cur.fetchall()
		for row in result2:
			userInstID=str(row[0])
			print (userInstID + "UserinstID")	
			insertInst(message)


def register2(message):
	global regUser, thisUsername, thisChatID
	bot.send_message(message.chat.id, "Регистрация2")

	#insertto()

def insertInst(message):
	global regUser, thisUsername, thisChatID, userInstitute, FacID
	bot.send_message(message.chat.id, userInstitute + "from instInst")
	cur.execute("INSERT into Users (UserID, Username, InstID, FacID, Course, GroupID) values ('%d', '%s','%s','1','3','4081')" % (thisChatID, thisUsername, userInstID))
	con.commit()
#@bot.message_handler(commands=['settings'])
#def handle_settings(message):
#	return
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
	
def haveuser():
	cur.execute("SELECT UserID FROM users  WHERE UserID=%d" % thisChatID)
	result=cur.fetchall()
	if regUser==True and result==[]:
		return False

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_words(message):
	global regUser, thisUsernawme, thisChatID, userInstitute, group, regInst, regFac, regCourse, regGroup
	thisUsername=message.chat.username
	thisChatID=message.chat.id
	day_name=''
	none_day=''
	bot_reply=''
	print ("Нахожусь в handle_words", userInstitute)
	#print (thisUsername) print (thisChatID)
	aint=message.text
	cur.execute("SELECT UserID, GroupID FROM users  WHERE UserID=%d" % thisChatID)
	result=cur.fetchall()
	for row in result:
		group=str(row[1])
	if regUser==True and result==[]:
		if aint=='Понедельник' or aint=='Вторник' or aint=='Среда' or aint=='Четверг' or aint=='Пятница' or aint=='Суббота':
			day_name=message.text
			none_day=''
			print (message.text, "Слова дней недели")
			handle_days(message)
		elif aint=='Сегодня' or aint=='сегодня' or aint=='/today':
			handle_today(message)
		elif aint=='Завтра' or aint=='завтра'or aint=='/tommorow':
			handle_tommorow(message)
		#elif aint[0]=="/":
		#	error_text=''
		else:
			print (aint, "from else, textobr first ELSE")
			error_text='... Ай, что то пошло не так:( \nПроверьте доступные команды '
			bot.send_message(message.chat.id, "%s" % error_text)
			handle_start_help(message)
	else:
		bot.send_message(message.chat.id, "Простите, но перед тем как получить список занятий, вам нужно настроить свой аккаунт - %d" % thisChatID)
#		if userInstitute=='/start':

#		bot.send_message(message.chat.id, userInstitute)
		
		register1(message)

	#connect()

def handle_days(message):
	bot_reply=''
	day_name=message.text
	cur.execute("SELECT timelist,lessid,lesstype,room, alllessons.id,lessname, Evod, DayName FROM timetable, alllessons, Days  WHERE lessid=alllessons.id and DayName='%s' and DayID=DayNum and GroupNum='%d' and (evod=0 or evod=%d)" % (day_name, group, evod()))
	result=cur.fetchall()
	bot_reply+="Расписание на %s \n\n" % day_name
	if result==[]:
		bot_reply+="В этот день у вас занятий нет!"	
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
	bot_reply+="Расписание на сегодня:\n\n"
	if result==[]:
		bot_reply+="Сегодня у вас занятий нет!"	
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
	bot_reply+="Расписание на завтра:\n\n"
	if result==[]:
		bot_reply+="Завтра у вас занятий нет!"	
	else:
		for row in result:
			bot_reply+="с " +str(row[0])+' '+str(row[2])+' по "'+str(row[5])+'" в '+str(row[3])+"\n"
			print (bot_reply)
	bot.send_message(message.chat.id, bot_reply)
	botan.track(config.botan_key, message.chat.id, message, 'Type /tommorow command or Завтра')



if __name__ == '__main__':
     bot.polling(none_stop=True)
     connect()
