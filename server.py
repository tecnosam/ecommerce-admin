from flask import Flask, request, jsonify, session, abort, Response, flash, render_template, redirect, url_for
# from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import copy
import buddy
import api
import os

# database = buddy.Instance("mysql://n0r8dtq32n99jcwm:snapxx84ci4o4824@vkh7buea61avxg07.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ftakoaax9gh5voz8")

app = Flask(__name__)
# cors = CORS(app)
ADMIN = '0000'

app.secret_key = b'681783631680ab73cc5b0b82a96705a4'

# app.config['CORS_HEADERS'] = 'Content-Type'

prop_map = {
	'products': {
		"cols": ['id', 'vid', 'title', 'price', 'image', 'category', 'delivered-in'],
		"spawnable": True,
		'deletable': "id",
		"editable": {
			'title':'text', 
			'price':'number', 
			'image': 'file', 
			'category':'text',
			'vid': "number",
			'delivered-in':'number'
		},
		"vid": None
	},
	'vendors': {
		"cols": ['vid', 'name', 'whatsapp'],
		"spawnable":True,
		'deletable': "vid",
		"editable": {"name": "text", "whatsapp": "text"},
		"vid": None
	},
	'purchases': {
		"cols": ['ref','id','user', 'price'],
		"spawnable": False,
		"deletable": False,
		"editable": None,
		"vid": None
	},
	'users': {
		"cols": ['uid', 'name', 'email', 'address'],
		"spawnable": False,
		"deletable": False,
		"editable": None,
		"vid": None
	}
}

@app.route("/")
def home():
	try:
		vid = request.args['key']
	except KeyError:
		abort(Response("Access denied. invalid key. key should be your vid", 400))

	return redirect( url_for( "fetch", title = "products", key = vid ) )

@app.route("/products", methods = ['POST', 'DELETE'])
def products():
	try:
		vid = request.args['key']
	except KeyError:
		abort(Response("Access denied. invalid key. key should be your vid", 400))

	if request.method == 'POST':

		try:
			# title, price, image, category, vid, delivered_in=3
			data = dict(request.form)
			fn = secure_filename( request.files['image'].filename )

			request.files['image'].save( fn )

			data['image'] = api.upload( fn )
			data['delivered_in'] = data.pop('delivered-in')
			os.remove(fn)

			res = api.Products.create( **data )

			if res:
				flash( f"Sucessfully created product", "success" )
			else:
				flash( f"Could not create product", "danger" )
		except TypeError as e:
			raise e
			abort(400)


	elif request.method == 'DELETE':
		try:
			# _id
			return jsonify(api.Products.delete( request.args['id'] ))
		except TypeError as e:
			return Response( { 'status': False, 'error': str(e) }, 400 )

	return redirect( url_for( "fetch", title = "products" ) + f"?key={vid}" )

@app.route("/products-edit", methods = ['POST'])
def products_edit():

	try:
		vid = request.args['key']
	except KeyError:
		abort(Response("Access denied. invalid key. key should be your vid", 400))

	try:
		# _id, node, val
		data = dict(request.form)
		_id = data.pop("id")
		for key in data:
			if key == 'image':
				fn = secure_filename( request.files['image'].filename )

				request.files['image'].save( fn )

				data[key] = api.upload( fn )

				os.remove( fn )
			api.Products.update( _id = _id, node = key, val = data[key] )

			# if res:
			# 	flash( f"Sucessfully edited {key} in product {_id}", "success" )
			# else:
			# 	flash( f"Could not edit product {_id}", "danger" )

		flash( f"Sucessfully edited product {_id}", "success" )

	except TypeError as e:
		raise e
		abort(400)

	return redirect( url_for( "fetch", title = "products" ) + f"?key={vid}" )

@app.route("/vendors", methods = ['POST', 'PUT', 'DELETE'])
def vendors():

	if request.method == 'POST':
		try:
			# vid, name, whatsapp
			res = api.Vendors.create( **request.form )
			if res:
				flash( f"Sucessfully created vendor", "success" )
			else:
				flash( f"Could not create vendor", "danger" )

		except TypeError as e:
			abort(400)

	elif request.method == 'DELETE':
		try:
			# vid
			return jsonify(api.Vendors.delete( request.args['vid'] ))
		except TypeError as e:
			return Response( { 'status': False, 'error': str(e) }, 400 )

	return redirect( url_for( "fetch", title = "vendors" ) )

@app.route("/vendors-edit", methods = ['POST'])
def vendors_edit():
	try:
		# vid, node, val
		data = dict(request.form)
		_id = data.pop("vid")
		for key in data:
			api.Vendors.update( _id = _id, node = key, val = data[key] )

			# if res:
			# 	flash( f"Sucessfully edited {key} in product {_id}", "success" )
			# else:
			# 	flash( f"Could not edit product {_id}", "danger" )

		flash( f"Sucessfully edited vendor {vid}", "success" )

	except TypeError as e:
		abort(400)

	return redirect( url_for( "fetch", title = "vendors" ) )

@app.route("/fetch/<title>")
def fetch( title ):
	try:
		vid = request.args['key']
	except KeyError:
		if title != 'products':
			vid = ADMIN
		else:
			abort(Response("Access denied. invalid key. key should be your vid", 400))
	try:
		# print( prop_map[title] )
		props = copy.deepcopy(prop_map[title])
		if (vid == ADMIN):
			data = api.database.fetch( title, props['cols'] )[::-1]
		else:
			if (title == 'products'):
				props['vid'] = vid
				props['editable'].pop('vid')
				data = api.database.fetch( title, props['cols'], {'vid': vid} )[::-1]
			else:
				data = []
	except KeyError as e:
		raise e
		print(str(e))
		flash( "table not found", "danger" )
		data = []

	return render_template( "data-renderer.html", data = data,
			title = title, props = props )

if __name__ == '__main__':
	app.run( debug = True, host = '0.0.0.0' )