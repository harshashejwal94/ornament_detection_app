# Load Database Pkg
import streamlit as st

import sqlite3

conn = sqlite3.connect("data.db",check_same_thread=False)
c = conn.cursor()


def do_work(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM my_table")
    rows = c.fetchall()
    print(rows)
    conn.close()

'''@st.cache(allow_output_mutation=True, hash_funcs={sqlite3.Connection: id})conn = sqlite3.connect('data.db')
def get_connection():
    conn = sqlite3.connect("data.db")
    return conn

c = conn.cursor()'''

'''conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS mytable (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()'''





# Fxn
'''def create_page_visited_table():
	c.execute('CREATE TABLE IF NOT EXISTS pageTrackTable(pagename TEXT,timeOfvisit TIMESTAMP)')'''

def create_page_visited_table():
    with sqlite3.connect('test.db', check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS pageTrackTable(pagename TEXT,timeOfvisit TIMESTAMP)')
        conn.commit()


def add_page_visited_details(pagename,timeOfvisit):
	c.execute('INSERT INTO pageTrackTable(pagename,timeOfvisit) VALUES(?,?)',(pagename,timeOfvisit))
	conn.commit()

def view_all_page_visited_details():
	c.execute('SELECT * FROM pageTrackTable')
	data = c.fetchall()
	return data


# Fxn To Track Input & Prediction
def create_emotionclf_table():
	c.execute('CREATE TABLE IF NOT EXISTS emotionclfTable(rawtext TEXT,prediction TEXT,probability NUMBER,timeOfvisit TIMESTAMP)')

def add_prediction_details(rawtext,prediction,probability,timeOfvisit):
	c.execute('INSERT INTO emotionclfTable(rawtext,prediction,probability,timeOfvisit) VALUES(?,?,?,?)',(rawtext,prediction,probability,timeOfvisit))
	conn.commit()

def view_all_prediction_details():
	c.execute('SELECT * FROM emotionclfTable')
	data = c.fetchall()
	return data



import threading

'''def do_work(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM my_table")
    rows = c.fetchall()
    print(rows)
    conn.close()'''

if __name__ == '__main__':
    conn = sqlite3.connect('data.db')
    t1 = threading.Thread(target=do_work, args=(conn,))
    t2 = threading.Thread(target=do_work, args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
