__author__ = 'krishnateja'

import logging
import datetime
from flaskext.mysql import MySQL
from flask import Flask, render_template
from flask_ask import Ask, statement, question

mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config['MYSQL_DATABASE_USER'] = 'conference'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qJ32wxcN'
app.config['MYSQL_DATABASE_DB'] = 'conference'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def new_conference():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("SpeakerIntent")
def ask_if_speaker(speaker_name):
    speaker_name = speaker_name
    message = ""
    rowcount = 0
    modifier = ""

    cursor = mysql.connect().cursor()

    cursor.execute(
        "SELECT * from conference.talk JOIN conference.speaker "
        "ON conference.talk.speaker = conference.speaker.speakerid "
        "JOIN conference.slot "
        "ON conference.talk.slot = conference.slot.slotid "
        "WHERE conference.speaker.name LIKE '%" + speaker_name + "%';")

    data = cursor.fetchall()
    if data is None:
        message = "There was no speaker by that name."
    else:
        for row in data:
            rowcount = rowcount + 1
            if rowcount > 1:
                modifier = " also "
                modifier = "{:%d, %b %Y}".format(row[9])
            message += modifier + "I found a session called '%s' by %s at %s. " % (row[1], row[6], row[9])

    return statement(message)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
