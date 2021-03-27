import pymysql as DBAdapter
import sys, os

class Connection:
    def __init__(self, 
        host = 'vkh7buea61avxg07.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', 
        usr = 'n0r8dtq32n99jcwm', pwd = 'snapxx84ci4o4824', db = "ftakoaax9gh5voz8"):
        self.db = DBAdapter.connect( host, usr, pwd, db )
        # self.db = DBAdapter.connect( "localhost", "root", "", "silcon" )

    def set( self, sql ):
        with self.db.cursor() as c:
            try:
                c.execute( sql )
                self.db.commit()
                return True
            except DBAdapter.err.IntegrityError:
                return -2
            except Exception as e:
                self.db.rollback()
                raise e
        return False
    
    def get( self, sql ):
        with self.db.cursor()as c:
            try:
                c.execute( sql )
                res = c.fetchall()
                return res
            except Exception as e:
                raise e
        return ()
    def getone(self, sql):
        with self.db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchone()
                return res
            except Exception as e:
                raise e
        return ()
    def check( self, sql ):
        with self.db.cursor()as c:
            try:
                c.execute( sql )
                res = c.fetchall()
                return True if len(res) > 0 else False
            except Exception as e:
                raise e
        return False