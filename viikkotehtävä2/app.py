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
        # adjust timezone
        finland_time = server_time.astimezone(pytz.timezone('Europe/Helsinki'))
        return server_time, finland_time
    else:
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def time():
    server_time, finland_time = get_current_time()
    
    if server_time and finland_time:
        response = {
            'server_time': server_time.strftime("%H:%M:%S %d.%m.%Y"),
            'finland_time': finland_time.strftime("%H:%M:%S %d.%m.%Y")
        }
    else:
        response = {
            'server_time': None,
            'finland_time': None
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
