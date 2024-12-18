from flask import Flask, render_template
import sqlite3

server = Flask(__name__)


def init_db():
    conn = sqlite3.connect('instance/database_parking.db')
    conn.execute('CREATE TABLE IF NOT EXISTS spaces (id INTEGER)')
    conn.close()




@server.before_request
def before_request():
    init_db()
    # insert_db(2)
    # insert_db(4)

@server.route('/')
def index():
    conn = sqlite3.connect('instance/database_parking.db')
    free_spaces = conn.execute('SELECT * FROM spaces').fetchall()
    conn.close()
    return render_template('base.html', free_spaces=free_spaces)

server.run()

