from db.mysql import Connection as con

from hashlib import md5

class Auth:

	@staticmethod
	def login( email, pwd ):
		_pwd = md5( pwd.encode() ).hexdigest()
		cols = 'uid,name,email,pwd,address'

		sql = f"SELECT {cols} FROM users WHERE email='{email}' AND pwd='{_pwd}'"
		db = con()
		cols = cols.split(",")

		res = db.getone( sql )
		print(res)
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
		db = con()

		return {'status': db.set( sql )}

	@staticmethod
	def edit_cred( _id, node, val ):

		if node not in [ 'name', 'email', 'pwd', 'address' ]:
			return {'status': False, 'code': 405}

		if node == 'pwd':
			val = md5( pwd.encode() ).hexdigest()

		sql = f"UPDATE users SET `{node}`='{val}' WHERE id={_id}"
		db = con()

		return {'status': db.set( sql )}


class Products:

	@staticmethod
	def create( title, price, image, category, vid ):
		# Vid means vendor ID
		sql = """INSERT INTO products ( title, price, image, category, vid ) 
					VALUES ('%s', %s, '%s', '%s', '%s')""" % (
				title, price, image, category, vid
			)
		db = con()

		return {'status': db.set( sql )}

	@staticmethod
	def retrieve( fil = None ):
		cols = ['id', 'title', 'price', 'image', 'category']
		sql = f"SELECT {','.join(cols)} FROM products ORDER BY `date-posted` DESC"
		db = con()

		res = db.get(sql)
		ret = []

		for row in res:

			ret.append( { cols[i]: row[i] for i in range( len(cols) ) } )

		return ret

	@staticmethod
	def update( _id, node, val ):

		if node not in [ 'title', 'price', 'category' ]:
			return {'status': False, 'code': 405}

		sql = f"UPDATE products SET `{node}`='{val}' WHERE id={_id}"
		db = con()

		return {'status': db.set( sql )}

	@staticmethod
	def delete( _id ):
		sql = f"DELETE FROM products WHERE id={_id}"
		db = con()

		return {'status': db.set( sql )}


class Vendors:

	@staticmethod
	def create( vid, name, whatsapp ):
		# Vid means vendor ID
		sql = "INSERT INTO vendors ( vid, name, whatsapp ) VALUES ('%s', '%s', '%s')" % (
				vid, name, whatsapp
			)
		db = con()

		return {'status': db.set( sql )}

	@staticmethod
	def retrieve( fil = None ):
		cols = ['vid', 'name', 'whatsapp']
		sql = "SELECT vid,name,whatsapp FROM vendors ORDER BY `date-created` DESC"
		db = con()

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
		db = con()

		return {'status': db.set( sql )}

	@staticmethod
	def delete( vid ):
		sql = f"DELETE FROM vendors WHERE vid={vid}"
		db = con()

		return {'status': db.set( sql )}

class Purchases:
	@staticmethod
	def log( ref, _id, user, price, quantity = 1 ):
		# Vid means vendor ID
		sql = "INSERT INTO purchases (ref,_id,user,price,quantity) VALUES ('%s',%s,'%s',%s,%s)" % (
				ref, _id, user, price, quantity
			)
		db = con()

		return {'status': db.set( sql )}

	@staticmethod
	def calc_revenue( vid ):
		# calc revenue for a vendor
		sql = "SELECT purchases.price, FROM "