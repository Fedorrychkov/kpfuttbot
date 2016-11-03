import mysql.connector
from mysql.connector import Error
def connect():
    """ Connect to MySQL database """
    try:
        con = mysql.connector.connect(host='localhost',database='kpfubott',user='root',password='')
        cur=con.cursor()
        cur.execute("SELECT * FROM lessons WHERE DayID=1 and GroupNum='408.1'")
        result=cur.fetchall()
        for row in result:
            print (row[6],row[7],row[9],row[8])

        if con.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        con.close()




if __name__ == '__main__':
    connect()