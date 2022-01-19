#

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, abort, reqparse
import mysql.connector
from flask_cors import CORS, cross_origin


app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




parser = reqparse.RequestParser()
parser.add_argument('nom')
parser.add_argument('prenom')
parser.add_argument('postnom')
parser.add_argument('date')
parser.add_argument('classe')
parser.add_argument('parent')
parser.add_argument('parent2')
parser.add_argument('idecole')





class CRUD():
    """docstring for CRUD"""
    def __init__(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
           database="db_ecole"
        )
        self.mycursor = self.mydb.cursor()
    def get_select(self, request):
        self.mycursor.execute(request)
        myresult =  self.mycursor.fetchall()
        a = [column[0] for column in self.mycursor.description]
        b = []
        for record in myresult:
          b.append(dict(zip(a, record)))
        self.get_close()
        return b
    def get_id(self, request):
        self.mycursor.execute(request)
        StrA = "".join(map(str, self.mycursor.fetchall()))
        t = ''
        for x in StrA:
          if(x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
            t = t + x
        return int(t)


    def get_close(self):
        self.mycursor.close()
        self.mydb.close()



class ListEleve(Resource):
    """docstring for Eleve"""
    def get(self):
        crud = CRUD()
        reponse = jsonify(crud.get_select("SELECT * FROM eleve"))
        reponse.headers.add('Access-Control-Allow-Origin', '*')
        return reponse

class ELeve(Resource):
    """docstring for ClassName"""
    @cross_origin()
    def post(self):
        arguments = parser.parse_args()
        nom = arguments['nom']
        postnom = arguments['postnom']
        prenom = arguments['prenom']
        date = arguments['date']
        classe = arguments['classe']
        parent = arguments['parent']
        parent2 = arguments['parent2']
        idecole = 1
        crud = CRUD()
        sql = 'INSERT INTO parent(pere,mere) VALUES (%s,%s)'
        val = (parent, parent2)
        crud.mycursor.execute(sql, val)
        crud.mydb.commit()
        crud.get_close()
        crud = CRUD()
        idparent = crud.get_id("SELECT id FROM parent ORDER BY id DESC LIMIT 1")
        crud.get_close()
        crud = CRUD()
        sql = 'INSERT INTO eleve(nom, postnom, prenom, date_naiss, classe, idparent, idecole) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        val = (nom,postnom, prenom, date, classe,idparent, idecole)
        crud.mycursor.execute(sql, val)
        crud.mydb.commit()
        crud.get_close()
        crud = CRUD()
        reponse = jsonify(crud.get_select("SELECT * FROM eleve"))
        reponse.headers.add('Access-Control-Allow-Origin', '*')
        return reponse


        
        
api.add_resource(ListEleve, '/')
api.add_resource(ELeve, '/eleve')


if __name__ == '__main__':
	app.run(debug=True)