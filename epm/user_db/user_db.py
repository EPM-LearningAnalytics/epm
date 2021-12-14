# DB Management
import sqlite3

conn = sqlite3.connect('user_data.db', check_same_thread=False)
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT PRIMARY KEY, password TEXT, role TEXT)')

def add_userdata(username, password, role):
    c.execute('INSERT OR IGNORE INTO usertable(username, password, role) VALUES (?,?,?)', (username, password, role))
    conn.commit()

def get_userdata(username, password, role):
    c.execute('SELECT * FROM usertable WHERE username = ? AND password = ? AND role = ?', (username, password, role))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

def delete_usertable():
    c.execute('DROP TABLE IF EXISTS usertable')
    conn.commit()