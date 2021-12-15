"""
This module contains user information including ID, password, and role
(student/instructor).
"""
import sqlite3

conn = sqlite3.connect('user_data.db', check_same_thread=False)
c = conn.cursor()

def create_usertable():
    """
    create a new table for DB if not exist.
    """
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT PRIMARY KEY, password TEXT, role TEXT)')

def add_userdata(username, password, role):
    """
    add a new user to DB.
    
    Parameters
    ----------
    username: student ID number
    password: stduent password
    role: student or instructor

    return
    ----------
    None
    """
    c.execute('INSERT OR IGNORE INTO usertable(username, password, role) VALUES (?,?,?)', (username, password, role))
    conn.commit()

def get_userdata(username, password, role):
    """
    retrieve a user data in DB.
    
    Parameters
    ----------
    username: student ID number
    password: stduent password
    role: student or instructor

    return
    ----------
    a list of user data
    """
    c.execute('SELECT * FROM usertable WHERE username = ? AND password = ? AND role = ?', (username, password, role))
    data = c.fetchall()
    return data

def view_all_users():
    """
    retrieve all user data in DB.
    
    Parameters
    ----------
    username: student ID number
    password: stduent password
    role: student or instructor

    return
    ----------
    a list of user data where each row represents a student data
    """
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

def delete_usertable():
    """
    delete user table if exists.
    """
    c.execute('DROP TABLE IF EXISTS usertable')
    conn.commit()