from flask import Flask, jsonify
from flask_serial import Serial
import mysql.connector
import requests
import json

app = Flask(__name__)
app.config['SERIAL_TIMEOUT'] = 0.2
app.config['SERIAL_PORT'] = '/dev/ttyACM0'
app.config['SERIAL_BAUDRATE'] = 115200
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1


mydb = mysql.connector.connect(host="localhost",user="root",password="",database="db_ecole")
mycursor = mydb.cursor()


ser =Serial(app)

b = []

@app.route('/')
def use_serial():
    with open("/opt/lampp/htdocs/lkc/test.txt", "r") as f:
        reponse = jsonify(f.readline())
    reponse.headers.add('Access-Control-Allow-Origin', '*')
    return reponse

@ser.on_message()
def handle_message(msg):
    #print("receive a message:", msg)
    # send a msg of str
    #ser.on_send("send a str message!!!")
    # send a msg of bytes

    #ser.on_send('')
    b = 1

@ser.on_log()
def handle_logging(level, info):
    b = ''
    for i in info:
        if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            b = b + i
    if b != '':
        insert(b)

    print(level, info)

def insert(values):
    url = "http://localhost/lkc/api.php?nom="
    url = url + ""+values
    payload = json.dumps({
        "nom": values
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)


if __name__ == '__main__':
    app.run(debug=True)