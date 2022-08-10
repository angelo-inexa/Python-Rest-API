# -*- coding: utf-8 -*-
# Librarys
from flask import Flask, render_template,jsonify,abort,request,url_for
import psycopg2

import os,json,random,datetime

from flask_mail import Mail, Message

# Variables
app = Flask(__name__)

# Settings
app.config['SECRET_KEY'] = 's3cr3t'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'armeldrey@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxxxxxxxxx'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)



db = psycopg2.connect(
	user = "postgres",
	password = "xxxxxxxxxxxxxxxxxx",
	host = "127.0.0.1",
	port = "5432",
	database = "api"
)

cursor = db.cursor()

#toujours en cours de developpement
def control_key(k):	
	sql = """SELECT * FROM apikey WHERE key='{}' AND date_expiration >= NOW()""".format(k)
	
	cursor.execute(sql)
	s = cursor.fetchone()
	return s


def traitement_file():
	data = []
	file_name = "static/files/sante.csv"
	if os.path.exists(file_name):
		with open(file_name,'r',encoding='utf-8',) as file:	
			k = 0
			for f in file:
				k = k + 1
				dataset = f.strip('\n')
				dataset = dataset.strip()
				dataset = dataset.split(",")
				for i in range(2,len(dataset)):
					dataset[i] = float(dataset[i])
					
				del dataset[1] #suppression de la colonne annee

				data.append(dataset)	
		return data
	else:
		print("ce fichier n'existe pas")


def insert_data_in_database():
	data = []
	cursor.execute("TRUNCATE infos")
	for i in range(len(traitement_file())):
		sql_insert = """
		INSERT INTO infos(id,nom, enf_m5, enf_sp, enf_mn, t_cfm, t_ps, t_mi, t_cmfm, t_f15_49, t_m5, t_va) VALUES({},'{}',{},{},{},{},{},{},{},{},{},{})
		"""
		sql = sql_insert.format(i+1,traitement_file()[i][0],traitement_file()[i][1],traitement_file()[i][2],traitement_file()[i][3],traitement_file()[i][4],traitement_file()[i][5],traitement_file()[i][6],traitement_file()[i][7],traitement_file()[i][8],traitement_file()[i][9],traitement_file()[i][10])
		cursor.execute(sql)
		db.commit()
	return True

insert_data_in_database()


#
#	CLEF D'AUTHENTIFICATION
#
def api_key():
	lettres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	taille = 54
	i = 0
	key = ""
	while i < taille:
		key = key + random.choice(lettres)
		i = i + 1
	return key

apikey = "XkoesDjmK25mlHJGQu3YZe1o0UymnGN4c3HkUWoYYCD7JCFv5mQrUG"


#
#	INFO POUR TOUTES LES REGIONS
#

def query_all():
	data = []
	cursor.execute("SELECT * FROM infos")
	sortie = cursor.fetchall()
	for i in range(len(sortie)):
		dic = {
			'id': sortie[i][0],
			'nom': sortie[i][1],
			'enf_m5': sortie[i][2],
			'enf_sp': sortie[i][3],
			'enf_mn': sortie[i][4],
			't_cfm': sortie[i][5],
			't_ps': sortie[i][6],
			't_mi': sortie[i][7],
			't_cmfm': sortie[i][8],
			't_f15_49': sortie[i][9],
			't_m5': sortie[i][10],
			't_va': sortie[i][11]
		}
		data.append(dic)
	return data

def query_all_limit(limit):
	data = []
	cursor.execute("SELECT * FROM infos ORDER BY id LIMIT {}".format(limit))
	sortie = cursor.fetchall()
	for i in range(len(sortie)):
		dic = {
			'id': sortie[i][0],
			'nom': sortie[i][1],
			'enf_m5': sortie[i][2],
			'enf_sp': sortie[i][3],
			'enf_mn': sortie[i][4],
			't_cfm': sortie[i][5],
			't_ps': sortie[i][6],
			't_mi': sortie[i][7],
			't_cmfm': sortie[i][8],
			't_f15_49': sortie[i][9],
			't_m5': sortie[i][10],
			't_va': sortie[i][11]
		}
		data.append(dic)
	return data


@app.route('/datasante/api/v0.1/apikey=<string:apikey>/regions', methods=['GET'])
def all_data(apikey):
	verif = control_key(apikey)
	if verif == None:
		if apikey != 'XkoesDjmK25mlHJGQu3YZe1o0UymnGN4c3HkUWoYYCD7JCFv5mQrUG':
			abort(404)
		else:
			#ajouter des restrictions pour ceux qui n'ont pas la clé
			limit = 3
			return jsonify(query_all_limit(limit)),200

	return jsonify(query_all()),200


#
# POUR UNE REGION TOUTES LES DONNEES
#
@app.route('/datasante/api/v0.1/apikey=<string:apikey>/region/<string:region>', methods=['GET'])
def recherche_region(apikey,region):
	data_r = []

	verif = control_key(apikey)
	if verif == None:
		if apikey != 'XkoesDjmK25mlHJGQu3YZe1o0UymnGN4c3HkUWoYYCD7JCFv5mQrUG':
			abort(404)
		else:
			#ajouter des restrictions pour ceux qui n'ont pas la clé
			limit = 3
			sortie = query_all_limit(limit)
			for i in range(len(sortie)):
				
				if sortie[i]["nom"] == region:
					dic = {
						'id': sortie[i]['id'],
						'nom': sortie[i]['nom'],
						'enf_m5': sortie[i]['enf_m5'],
						'enf_sp': sortie[i]['enf_sp'],
						'enf_mn': sortie[i]['enf_mn'],
						't_cfm': sortie[i]['t_cfm'],
						't_ps': sortie[i]['t_ps'],
						't_mi': sortie[i]['t_mi'],
						't_cmfm': sortie[i]['t_cmfm'],
						't_f15_49': sortie[i]['t_f15_49'],
						't_m5': sortie[i]['t_m5'],
						't_va': sortie[i]['t_va']
					}
					data_r.append(dic)

			if len(data_r) == 0:
				return "Pas de resultat"
			return jsonify(data_r),200


	
	cursor.execute("SELECT * FROM infos")
	sortie = cursor.fetchall()

	for i in range(len(sortie)):
		if sortie[i][1] == region:
			dic = {
				'id': sortie[i][0],
				'nom': sortie[i][1],
				'enf_m5': sortie[i][2],
				'enf_sp': sortie[i][3],
				'enf_mn': sortie[i][4],
				't_cfm': sortie[i][5],
				't_ps': sortie[i][6],
				't_mi': sortie[i][7],
				't_cmfm': sortie[i][8],
				't_f15_49': sortie[i][9],
				't_m5': sortie[i][10],
				't_va': sortie[i][11]
			}
			data_r.append(dic)		

	return jsonify(data_r),200

	

#
#	RECHERCHE PAR CARACTERISTIQUE (5 elements)
#
@app.route('/datasante/api/v0.1/apikey=<string:apikey>/variables/<string:var>', methods=['GET'])
def recherche_caracteristique(apikey,var):
	data_rc = []	
	verif = control_key(apikey)
	if verif == None:
		if apikey != 'XkoesDjmK25mlHJGQu3YZe1o0UymnGN4c3HkUWoYYCD7JCFv5mQrUG':
			abort(404)
		else:
			#ajouter des restrictions pour ceux qui n'ont pas la clé
			data_rc = []
			limit = 3
			# sql = "SELECT id,"+var+" FROM infos ORDER BY "+var+" DESC LIMIT 3"
			# cursor.execute(sql)
			# sortie = cursor.fetchall()
			sortie = query_all_limit(limit)

			for i in range(len(sortie)):		
				dic = {
					'id': sortie[i]['id'],
					var: sortie[i][var]
				}
				data_rc.append(dic)		

			return jsonify(data_rc),200

	
	sql = "SELECT id,"+var+" FROM infos ORDER BY "+var+" DESC LIMIT 5"
	cursor.execute(sql)
	sortie = cursor.fetchall()

	for i in range(len(sortie)):		
		dic = {
			'id': sortie[i][0],
			var: sortie[i][1]
		}
		data_rc.append(dic)		

	return jsonify(data_rc),200


#
#	POUR UNE REGION ET POUR UNE CATACTERISTIQUE
#
@app.route('/datasante/api/v0.1/apikey='+apikey+'/<string:reg>/<string:var>', methods=['GET'])
def recherche_region_variable(reg,var):
	data_rv = []
	sql = "SELECT id,nom,"+var+" FROM infos WHERE nom='"+reg+"'"
	cursor.execute(sql)
	sortie = cursor.fetchall()

	# if len(sortie) == 0:
	# 	abort(404)

	for i in range(len(sortie)):		
		dic = {
			'id': sortie[i][0],
			'nom': sortie[i][1],
			var: sortie[i][2]
		}
		data_rv.append(dic)		

	return jsonify(data_rv),200


#
#	AJOUTER UNE REGION ET SES CARACTERISTIQUES
#
@app.route('/datasante/api/v0.1/apikey='+apikey+'/regions', methods=['POST'])
def ajout_de_donnee():
	dic = {
		"id": request.json['id'],
		"nom":request.json['nom'],
		"enf_m5": request.json['enf_m5'],
		"enf_sp": request.json['enf_sp'],
		"enf_mn": request.json['enf_mn'],
		"t_cfm": request.json['t_cfm'],
		"t_ps": request.json['t_ps'],
		"t_mi": request.json['t_mi'],
		"t_cmfm": request.json['t_cmfm'],
		"t_f15_49": request.json['t_f15_49'],
		"t_m5": request.json['t_m5'],
		"t_va": request.json['t_va']
	}
	x = query_all()
	x.append(dic)
	return jsonify(x),201


#
#	MODIFIER UNE REGION ET SES CARACTERISTIQUES CONNAISSANT LE ID
#
@app.route('/datasante/api/v0.1/apikey='+apikey+'/regions/<int:ide>', methods=['PUT'])
def modifier_de_donnee(ide):
	x = query_all()

	sql = "SELECT * FROM infos WHERE id ="+str(ide)
	cursor.execute(sql)
	s = cursor.fetchall()
	if len(s) == 1:
		dic = {
			"id": ide,
			"nom":request.json['nom'],
			"enf_m5": request.json['enf_m5'],
			"enf_sp": request.json['enf_sp'],
			"enf_mn": request.json['enf_mn'],
			"t_cfm": request.json['t_cfm'],
			"t_ps": request.json['t_ps'],
			"t_mi": request.json['t_mi'],
			"t_cmfm": request.json['t_cmfm'],
			"t_f15_49": request.json['t_f15_49'],
			"t_m5": request.json['t_m5'],
			"t_va": request.json['t_va']
		}
		x.append(dic)
	return jsonify(x)


@app.route("/datasante/api/v0.1/apikey=<string:apikey>/region/<int:ide>", methods=['DELETE'])
def delete(apikey,ide):
	verif = control_key(apikey) 

	if verif == None:
		if apikey != 'XkoesDjmK25mlHJGQu3YZe1o0UymnGN4c3HkUWoYYCD7JCFv5mQrUG':
			print("PAS DE RESULTAT")
			abort(404)
		else:
			#ajouter des restrictions pour ceux qui n'ont pas la clé
			limit = 3
			query = query_all_limit(limit)
			
			for i,q in enumerate(query):				
				if q["id"] == ide:
					del query[i]
			return jsonify(query), 200

	sql = "SELECT * FROM infos" # WHERE id ="+str(ide)
	cursor.execute(sql)
	query = list(cursor.fetchall())
	for i,q in enumerate(query):
		#q = list(q)
		if list(q)[0] == ide:
			del query[i]
	
	return jsonify(query)

# Views

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/getKey',methods=['POST','GET'])
def getKey():
    if request.method == 'POST':
    	key = api_key()
    	username = request.form['username']
    	email = request.form['email']

    	# date de creation et d'expiration
    	date_create = datetime.date.today()
    	date_expiration = datetime.date.today() + datetime.timedelta(days=30) #30 jours
    	
    	if username != "" and email != "":
	    	msg = Message("Récuperation de l'Api Key",sender="armeldrey@gmail.com",recipients=[email])
	    	msg.html = """
	    	<!DOCTYPE html>
			<html>
			<head>
				<title></title>
			</head>
			<body>
				<p>
					Hello {} <br>
				    La clé de l'APi est:  <b>{}<b> <br>
				    Elle expire le <b style='color:red;'>{}</b>
				</p>
				<p>
					<br> Cordialement
				</p>
			</body>
			</html>
	    	""".format(username,key,date_expiration)

	    	#envoi du mail
	    	mail.send(msg)

	    	#enregistrement dans la table apikey
	    	sql = "INSERT INTO apikey(key,username,date_create,date_expiration) VALUES('{}','{}','{}','{}')"
	    	cursor.execute(sql.format(key,username,date_create,date_expiration))
	    	db.commit()

	    	print("Terminé")
    return render_template('getKey.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def index():
    return render_template('index.html')



# Run
if __name__ == '__main__':
	# url = str(request.url_rule).split('/')
	# cle = url[4].split("=")[1]
	app.run(debug=True)
