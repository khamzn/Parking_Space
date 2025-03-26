from flask import Flask, render_template, request
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

# RESTAPI requests
# See URL: https://habr.com/ru/articles/246699/
@server.route('/api/spaces', methods=['GET'])
def on_request_get_all_spaces():
    print('GET request : api/spaces')
    return '<b>All</b> spaces were requested'

@server.route('/api/spaces/getfree', methods=['GET'])
def on_request_get_free_spaces():
    print('GET request : api/spaces/getfree')
    return '<font color="#009900">Free</font> spaces only were requested'

@server.route('/api/spaces/getoccupied', methods=['GET'])
def on_request_get_occupied_spaces():
    print('GET request : api/spaces/getoccupied')
    return '<font color="#990000">Occupied</font> spaces only were requested'

@server.route('/api/spaces/setfree', methods=['GET'])
def on_request_set_free_space():
    print('GET request : api/spaces/setfree')
    return f'Space #{request.args["place"]} is now free'

@server.route('/api/spaces/setoccupied', methods=['GET'])
def on_request_set_occupied_space():
    print('GET request : api/spaces/setoccupied')
    return f'Space #{request.args["place"]} is now occupied'

server.run()
