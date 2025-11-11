from flask import Flask, render_template, jsonify
from datetime import datetime
import mysql.connector 
import pytz

app = Flask(__name__)


def get_current_time():
    conn = mysql.connector.connect(
        host="localhost",
        user="user",
        password="StrongP@ssw0rd!",
        database="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")  # get server time
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        server_time = row[0]
        result = server_time.astimezone(pytz.timezone('Europe/Helsinki'))
    else: 
        result = None
    
    return result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def time():
    current_time = get_current_time()
    return jsonify({'time': str(current_time.strftime("%Y-%m-%d %H:%M:%S"))})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)