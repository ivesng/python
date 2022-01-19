from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)
api = Api(app)

ETUDIANTS = {
	
	'17NN365':{'nom': 'Etudiant 1'},
	'16NN365':{'nom': 'Etudiant 2'},
	'15NN365':{'nom': 'Etudiant 3'},
	'15NN365':{'nom': 'Etudiant 4'}
}

parser = reqparse.RequestParser()
parser.add_argument('nom')
parser.add_argument('prenom')

class ListEtudiants(Resource):
	def get(self):
		return ETUDIANTS
source env/bin/activate

class Etudiant(Resource):
	def get(self, matricule):
		if matricule not in ETUDIANTS:
			abort(404, messagde=f'Le matricule {matricule} est incorrect')
		return ETUDIANTS[matricule]

	def post(self, matricule):
		arguments = parser.parse_args()
		if matricule in ETUDIANTS:
			abort(409, message=f'Le matricule existe deja')
		ETUDIANTS[matricule] = {'nom':arguments['nom'], 'prenom':arguments['prenom']}

		return 201, 'created succe'
	def put(self, matricule):
		arguments = parser.parse_args()
		if matricule in ETUDIANTS:
			ETUDIANTS[matricule] = {'nom':arguments['nom'], 'prenom':arguments['prenom']}
		ETUDIANTS[matricule] = {'nom':arguments['nom'], 'prenom':arguments['prenom']}
		return 'created succe', 201

	def delete(self, matricule):
		if matricule in ETUDIANTS:
			ETUDIANTS.pop(matricule, None)
			return 'delete succe', 201
		else:
			abort(409, message=f'Le matricule n\'existe pas')



#* Exposer les endpoints

api.add_resource(ListEtudiants, '/etudiants')
api.add_resource(Etudiant, '/etudiants/<string:matricule>')


if __name__ == '__main__':
	app.run(debug = True)
