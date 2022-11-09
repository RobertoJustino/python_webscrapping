from flask import Flask, render_template
import mysql.connector

app=Flask(__name__,template_folder='templates')

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'gamesdb'
}

# READ ALL DATA
def games():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM games')
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results

@app.route('/')
def index():
    return render_template('index.html', data=games())


if __name__ == '__main__':
    app.run(host='0.0.0.0')


