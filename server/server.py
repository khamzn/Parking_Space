from flask import Flask, render_template, request, jsonify
import sqlite3

server = Flask(__name__)
database = "instance/database_parking.db"


def init_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spaces (
            id INTEGER PRIMARY KEY,
            cords VARCHAR,
            color VARCHAR,
            status BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()


def delete_db(path):
    conn = sqlite3.connect(path)
    conn.execute('DELETE FROM spaces')
    conn.commit()
    conn.close()


def insert_into_db(data):
    delete_db(database)
    conn = sqlite3.connect(database)
    conn.executemany('INSERT INTO spaces VALUES(?, ?, ?, ?)', data)
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
    cords = []
    print(rows)
    for i in range(len(rows)):
        if rows[i][3]:
            free_spaces += 1
        cords.append(rows[i][1])
        colors.append(rows[i][2])
    conn.close()
    return render_template('base.html', free_spaces=free_spaces, quads=zip(cords, colors))


@server.route('/add_data', methods=['POST'])
def add_data():
    try:
        data = request.json
        insert_into_db(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


server.run()
