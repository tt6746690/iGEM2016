import dota2api
import os
import MySQLdb
from time import sleep

ti = 0

API_KEY = 'BE591D102BD4B3652CB310A39F7EA79C'
# MYSQL_PORT_3306_TCP_PORT
DB_HOST = os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1')
DB_PORT = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306))
DB_USER = 'root'
DB_PASS = os.getenv('MYSQL_ENV_MYSQL_ROOT_PASSWORD')
DB_NAME = 'dota2_data'

class CollectData():

    def __init__(self):
        self.api = dota2api.Initialise(API_KEY)
        self.db = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        self.c = self.db.cursor()


    def testMysqlConnection(self):
        ''' testing connection to mysql in another container'''
        try:
            self.c.execute('show databases;')
            print self.c.fetchall()
        except MySQLdb.Error, e:
            print 'mysql connection failed'
            raise e
            self.db.rollback()


    def getHeroMapping(self):
        ''' store hero name:id mapping to db '''
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

    def checkValidMatch(self, match):
        ''' check if match is valid '''
        for player in match['players']:
            if player['leaver_status'] is not 0:
                return False
        return True

    def handleMatch(self, matchID):
        ''' process match detail in detail '''
        m = self.api.get_match_details(match_id=matchID)
        if not self.checkValidMatch(m):
            print 'skipping match {}'.format(m['match_id'])
            return None

        self.populateGameMatchTable(m)

    def populateGameMatchTable(self, m):
        ''' populate Match table '''
        sqlstr = """
            INSERT IGNORE INTO GameMatch (MATCH_ID, RADIANT_WIN)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE MATCH_ID=%s
        """
        inserts = (m['match_id'], m['radiant_win'], m['match_id'])
        try:
            self.c.execute(sqlstr, inserts)
            self.db.commit()
            print 'SUCCESS: insert to GameMatch table {}'.format(m['match_id'])
            self.populateMatchPlayerTable(m)
        except MySQLdb.Error, e:
            print 'ERROR: populate match table failed at {}'.format(m['match_id'])
            raise e
            self.db.rollback()

    def populateMatchPlayerTable(self, m):
        ''' populate MatchPlayer table '''
        sqlstr = """
            INSERT INTO MatchPlayer (MATCHPLAYER_ID, ACCOUNT_ID, HERO_ID,
            HERO_NAME, MATCH_ID)
            VALUES (0, %s, %s, %s, %s)
        """
        inserts = [(p['account_id'], p['hero_id'], p['hero_name'], m['match_id'])
            for p in m['players']]
        try:
            self.c.executemany(sqlstr, inserts)
            self.db.commit()
            print 'SUCCESS: insert to MatchPlayer table {}'.format(m['match_id'])
        except MySQLdb.Error, e:
            print 'ERROR: populate matchplayer table failed at {}'.format(m['match_id'])
            raise e
            self.db.rollback()

    def getMatches(self):
        ''' handles logic for getting history and loading data to db '''
        iterr = 5
        startMatchID = None
        while True:
            his = self.api.get_match_history(start_at_match_id=startMatchID,
                                             skill=3,
                                             min_players=10,
                                             game_mode=2,
                                             matches_requested=500)
            matches = his['matches']

            if len(matches) is 0:
                print('Finished processing all 500 most recent matches.')
                break

            print 'start from {} to {}'.format(matches[0]['match_id'],matches[-1]['match_id'] - 1)

            for match in matches:
                self.handleMatch(match['match_id'])
                sleep(ti)

            startMatchID = matches[-1]['match_id'] - 1
            sleep(5)



if __name__ == '__main__':
    iterr = 50
    while iterr >= 0:
        try:
            co = CollectData()
            co.getMatches()
            sleep(5)
        except dota2api.src.exceptions.APITimeoutError:
            sleep(10)
            print '==== re-run script due to APITimeoutError ===='
            continue
        else:
            break
