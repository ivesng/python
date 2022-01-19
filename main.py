#

from flask import Flask, jsonify

app = Flask(__name__)

list_etudiants = [
				{'id': 1, 'nom':'NGALAMULUME', 'cotes':[5, 6, 4, 7]},
				{'id': 2, 'nom':'JUDITH CAROLE', 'cotes':[5, 6, 4, 7]},
				{'id': 3, 'nom':'YAN ', 'cotes':[5, 6, 4, 7]},
				{'id': 4, 'nom':'NAOMI NANA KETCHUP', 'cotes':[5, 6, 4, 7]},
				{'id': 5, 'nom':'ESTHER', 'cotes':[5, 6, 4, 7]}
				
			]
@app.route('/list_etudiants')
def get_all_etudiants():
	reponse = jsonify(list_etudiants)
	reponse.headers.add('Access-Control-Allow-Origin', '*')
	return reponse

@app.route('/<int:id>')
def get_by_id(id):
	for x in list_etudiants:
		if x['id'] == id:
			return jsonify(x)


if __name__ == '__main__':
	app.run(debug=True)