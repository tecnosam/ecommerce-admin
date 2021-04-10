from db.mysql import Connection as con

from hashlib import md5, sha1
import time
from requests import post
import buddy

database = buddy.Instance("mysql://n0r8dtq32n99jcwm:snapxx84ci4o4824@vkh7buea61avxg07.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ftakoaax9gh5voz8")

def upload(fn):
	url = "https://api.cloudinary.com/v1_1/tecnosam/image/upload"
	timestamp = int(time.time())
	signature = sha1(f"timestamp={timestamp}UNe-2W-y7BTECHqyetINaBO2btw".encode()).hexdigest()
	file = open(fn, "rb")
	api_key = "758317386493753"
	data = {"api_key": api_key, "timestamp": timestamp, "signature": signature }
	files = {"file": file}
	res = post( url, data = data, files = files )
	return res.json()['secure_url']

class Auth:

	@staticmethod
	def login( email, pwd ):
		_pwd = md5( pwd.encode() ).hexdigest()
		cols = 'uid,name,email,pwd,address'

		sql = f"SELECT {cols} FROM users WHERE email='{email}' AND pwd='{_pwd}'"
		db = database.db
		cols = cols.split(",")

		res = db.getone( sql )
		if res is None:
			return {
				"status": False,
				"error": "Invalid Authentication details", 
				"data": None
			}
		return {
			"status": True,
			'data':{ cols[i]: res[i] for i in range( len( cols ) ) },
			'error': None
		}

	@staticmethod
	def create( uid, name, email, pwd, address ):

		pwd = md5( pwd.encode() ).hexdigest()

		sql = f"""INSERT INTO users (uid, name, email, pwd, address)
			 VALUES ('{uid}', '{name}', '{email}', '{pwd}', '{address}')"""
		db = database.db

		return {'status': db.set( sql )}

	@staticmethod
	def edit_cred( _id, node, val ):

		if node not in [ 'name', 'email', 'pwd', 'address' ]:
			return {'status': False, 'code': 405}

		if node == 'pwd':
			val = md5( pwd.encode() ).hexdigest()

		sql = f"UPDATE users SET `{node}`='{val}' WHERE id={_id}"
		db = database.db

		return {'status': db.set( sql )}


class Products:

	@staticmethod
	def create( title, price, image, category, vid, delivered_in=3 ):
		# Vid means vendor ID
		sql = """INSERT INTO products ( title, price, image, category, vid, `delivered-in` ) 
					VALUES ('%s', %s, '%s', '%s', '%s', %s)""" % (
				title, price, image, category, vid, delivered_in
			)
		db = database.db

		return {'status': db.set( sql )}

	@staticmethod
	def retrieve( fil = None ):
		cols = ['id', 'title', 'price', 'image', 'category', '`delivered-in`']
		sql = f"SELECT {','.join(cols)} FROM products ORDER BY `date-posted` DESC"
		db = database.db

		res = db.get(sql)
		ret = []

		for row in res:

			ret.append( { cols[i].replace("`", ""): row[i] for i in range( len(cols) ) } )

		return ret

	@staticmethod
	def update( _id, node, val ):

		if node not in [ 'title', 'price', 'category', 'delivered-in' ]:
			return {'status': False, 'code': 405}

		sql = f"UPDATE products SET `{node}`='{val}' WHERE id={_id}"
		db = database.db

		return db.set( sql )

	@staticmethod
	def delete( _id ):
		sql = f"DELETE FROM products WHERE id={_id}"
		db = database.db

		return {'status': db.set( sql )}


class Vendors:

	@staticmethod
	def create( name, whatsapp ):
		sql = "INSERT INTO vendors ( name, whatsapp ) VALUES ('%s', '%s')" % (
				name, whatsapp
			)

		db = database.db

		return {'status': db.set( sql )}

	@staticmethod
	def retrieve( fil = None ):
		cols = ['vid', 'name', 'whatsapp']
		sql = "SELECT vid,name,whatsapp FROM vendors ORDER BY `date-created` DESC"
		db = database.db

		res = db.get(sql)
		ret = []

		for row in res:

			ret.append( { cols[i]: row[i] for i in range(3) } )

		return ret

	@staticmethod
	def update( vid, node, val ):

		if node not in [ 'name', 'whatsapp' ]:
			return {'status': False, 'code': 405}

		sql = f"UPDATE vendors SET `{node}`='{val}' WHERE vid={vid}"
		db = database.db

		return {'status': db.set( sql )}

	@staticmethod
	def delete( vid ):
		sql = f"DELETE FROM vendors WHERE vid={vid}"
		db = database.db

		return {'status': db.set( sql )}

class Purchases:
	@staticmethod
	def log( ref, _id, user, price,  quantity = 1, db= None ):
		# Vid means vendor ID
		# _id means id of the product purchased
		# ref is the transaction reference
		# price is the purchase price at that moment
		# quantity is the number of units purchased
		sql = "INSERT INTO purchases (ref,id,user,price,quantity) VALUES ('%s',%s,'%s',%s,%s)" % (
				ref, _id, user, price, quantity
			)
		if db is None:
			db = database.db

		return {
			'status': db.set( sql )
			}

	@staticmethod
	def calc_revenue( vid ):
		# calc revenue for a vendor
		sql = "SELECT purchases.price, FROM "