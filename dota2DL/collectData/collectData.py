import dota2api
import os
import MySQLdb

API_KEY = 'BE591D102BD4B3652CB310A39F7EA79C'
# MYSQL_PORT_3306_TCP_PORT
DB_HOST = os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1')
DB_PORT = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306))
DB_USER = 'root'
DB_PASS = '1122'
DB_NAME = 'dota2_data'

class CollectData():

    def __init__(self):
        self.api = dota2api.Initialise(API_KEY)
        self.db = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        self.c = self.db.cursor()


    def testMysqlConnection(self):
        try:
            self.c.execute('show databases;')
            print self.c.fetchall()
        except MySQLdb.Error, e:
            print 'mysql connection failed'
            raise e
            self.db.rollback()


    def getHeroMapping(self):
        getHero = self.api.get_heroes()
        l = []
        for hero in getHero["heroes"]:
            tup = (hero['id'], hero['localized_name'], hero['name'])
            l.append(tup)
        sqlstr = """
            INSERT INTO Hero (HERO_ID, LOCALIZED_NAME, NAME)
            VALUES (%s, %s, %s)
        """
        try:
            self.c.executemany(sqlstr, l)
            self.db.commit()
        except MySQLdb.Error, e:
            print 'mysql connection failed'
            raise e
            self.db.rollback()






if __name__ == '__main__':
    co = CollectData()
    co.getHeroMapping()
