from flask import Flask, render_template
import sqlite3

server = Flask(__name__)

def init_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spaces (
            id INTEGER PRIMARY KEY,
            coords VARCHAR,
            color VARCHAR,
            status BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()


@server.before_request
def before_request():
    init_db('instance/database_parking.db')


@server.route('/')
def index():
    conn = sqlite3.connect('instance/database_parking.db')
    rows = conn.execute('SELECT * FROM spaces').fetchall()
    free_spaces = 0
    colors = []
    coords = []
    print(rows)
    for i in range(len(rows)):
        if rows[i][3]:
            free_spaces += 1
        coords.append(rows[i][1])
        colors.append(rows[i][2])

    print(coords, colors)
    conn.close()
    return render_template('base.html', free_spaces=free_spaces, quads=zip(coords, colors))


server.run()
