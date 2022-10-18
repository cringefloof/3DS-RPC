from flask import Flask
import sqlite3
from api import *

app = Flask(__name__)

def accessDB():
    con = sqlite3.connect('sqlite/fcLibrary.db')
    cursor = con.cursor()
    return con, cursor

@app.route('/user/<int:friendCode>/', methods=['GET'])
def userPresence(friendCode:int):
    con, cursor = accessDB()
    try:
        principalId = convertFriendCodeToPrincipalId(friendCode)
        cursor.execute('SELECT * FROM friends WHERE friendCode = %s' % friendCode)
        result = cursor.fetchone()
        if not result:
            raise Exception('friendCode not recognized')
        if result[1] != 0:
            presence = {
                'titleID': result[2],
                'updateID': result[3],
            }
        else:
            presence = {}
        return {
            'Exception': False,
            'User': {
                'principalId': principalId,
                'friendCode': convertPrincipalIdtoFriendCode(principalId),
                'online': bool(result[1]),
                'Presence': presence,
            }
        }
    except Exception as e:
        return {
            'Exception': {
                'Error': str(e),
            }
        }

@app.route('/user/c/<int:friendCode>/', methods=['POST'])
def createUser(friendCode:int):
    con, cursor = accessDB()
    try:
        convertFriendCodeToPrincipalId(friendCode)
        #cursor.execute('SELECT COUNT(1) FROM friends WHERE friendCode = %s' % friendCode)
        #if cursor.fetchone()[0] != 0:
            #raise Exception()
        cursor.execute('INSERT INTO friends (friendCode, online, titleID, updID) VALUES (%s, %s, %s, %s)' % (friendCode, False, '0', '0'))
        con.commit()
        return {
            'Exception': False,
        }
    except Exception as e:
        return {
            'Exception': {
                'Error': str(e),
            }
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2277)
