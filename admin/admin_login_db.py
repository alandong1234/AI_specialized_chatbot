import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('admin/admin_info')  # replace according to your need
        return conn
    except Error as e:
        print(e)

    return conn

def create_admin_table(conn):
    try:
        sql = '''CREATE TABLE admins (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );'''
        conn.execute(sql)
    except Error as e:
        print(e)

def insert_admin(conn, admin):
    try:
        sql = '''INSERT INTO admins(username, password) VALUES(?, ?)'''
        conn.execute(sql, admin)
        conn.commit()
    except Error as e:
        print(e)

def get_admin(conn, username, password):
    try:
        sql = '''SELECT * FROM admins WHERE username = ? AND password = ?'''
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        return cur.fetchone()
    except Error as e:
        print(e)