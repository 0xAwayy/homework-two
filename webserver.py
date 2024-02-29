from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        points INTEGER NOT NULL
    )
    ''')

    initial_data = [
        ('Steve Smith', 211, 80),
        ('Jian Wong', 122, 92),
        ('Chris Peterson', 213, 91),
        ('Sai Patel', 524, 94),
        ('Andrew Whitehead', 425, 99),
        ('Lynn Roberts', 626, 90),
        ('Robert Sanders', 287, 75)
    ]

    cursor.executemany('INSERT INTO users (name, id, points) VALUES (?, ?, ?)', initial_data)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)


@app.route('/create', methods=['POST'])
def create_user():
    name = request.form['name']
    id = request.form['id']
    points = request.form['points']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, id, points) VALUES (?, ?, ?)', (name, id, points))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/search', methods=['GET'])
def search_user():
    user_name = request.args.get('name')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE name = ?', (user_name,)).fetchone()
    conn.close()
    return jsonify(dict(user))


@app.route('/update', methods=['POST'])
def update_user():
    original_name = request.form['original_name']
    new_id = request.form['new_id']
    new_points = request.form['new_points']
    print(f"original_name: {original_name}, new_id: {new_id}, new_points: {new_points}")
    conn = get_db_connection()
    conn.execute('UPDATE users SET id = ?, points = ? WHERE name = ?',
                 (new_id, new_points, original_name))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/delete', methods=['POST'])
def delete_user():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)