from flask import Flask, request, jsonify, session, abort, Response
from flask_cors import CORS, cross_origin

import api

app = Flask(__name__)
cors = CORS(app)

app.secret_key = b'681783631680ab73cc5b0b82a96705a4'

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/products", methods = ['POST', 'GET', 'PUT', 'DELETE'])
@cross_origin()
def products():
	if request.method == 'GET':
		return jsonify(api.Products.retrieve(  ))

	return "The remaining methods are not yet available to the public"

@app.route( "/login", methods = ['GET', 'POST', 'DELETE'] )
@cross_origin()
def login():
	if request.method == 'GET':
		if not len( session ):
			return jsonify(None)
		return jsonify(dict(session))

	elif request.method == 'DELETE':
		keys = [i for i in session]
		for i in keys:
			session.pop( i )
		return jsonify( True )

	try:
		res = api.Auth.login( **request.get_json() )
		if res['status']:
			for key in res['data']:
				session[key] = res['data'][key]
		return jsonify( res )

	except TypeError as e:
		abort( Response( {"error": str(e), "data": None}, 400 ) )

	return "Weird"

@app.route( "/signup", methods = ['POST'] )
@cross_origin()
def signup():

	try:
		return jsonify( api.Auth.create( **request.get_json() ) )
	except TypeError as e:
		abort( Response( {"status": False,"error": str(e), "data": None}, 400 ) )

	return "Weird"

@app.route( "/purchases", methods = ['POST'] )
def purchases():
	if request.method == 'POST':
		data = dict( request.get_json() )
		ref = data['ref']
		uid = data['uid']
		logs = []

		for item in data['basket']:
			res = api.Purchases.log( ref, item['id'], uid, item['price'], item['quantity'] )
			res['product'] = item['title']
			if not res['status']:
				logs.append( res )

		return jsonify( { 'status': True, "logs": logs } )

	return "Whoopsy"


if __name__ == '__main__':
	app.run( debug = True, host = '0.0.0.0' )