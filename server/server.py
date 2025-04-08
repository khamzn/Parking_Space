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
            status BOOLEAN,
            resX INT,
            resY INT
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
    conn.executemany('INSERT INTO spaces VALUES(?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()


@server.before_request
def before_request():
    init_db('instance/database_parking.db')


@server.route('/')
def index():
    conn = sqlite3.connect('instance/database_parking.db')
    rows = conn.execute('SELECT * FROM spaces').fetchall()
    free_spaces = conn.execute("SELECT COUNT(status) FROM spaces WHERE status = 1").fetchone()[0]
    colors = [row[0] for row in conn.execute('SELECT color FROM spaces').fetchall()]
    cords = [row[0] for row in conn.execute('SELECT cords FROM spaces').fetchall()]
    resX = conn.execute("SELECT resX FROM spaces").fetchone()[0]
    resY = conn.execute("SELECT resY FROM spaces").fetchone()[0]
    conn.close()
    return render_template('base.html', free_spaces=free_spaces, quads=zip(cords, colors), resX = resX, resY = resY)


@server.route('/add_data', methods=['POST'])
def add_data():
    try:
        data = request.json
        insert_into_db(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@server.route('/api/spaces/getfree', methods=['GET'])
def on_request_get_free_spaces():
    conn = sqlite3.connect('instance/database_parking.db')
    print('GET request : api/spaces/getfree')
    return f'<font color="#009900">{conn.execute("SELECT COUNT(status) FROM spaces WHERE status = 1").fetchone()[0]}</font> spaces only were requested'


server.run()
