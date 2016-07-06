import os
import MySQLdb
import numpy as np
from collections import defaultdict
import six.moves.cPickle as pickle


DB_HOST = os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1')
DB_PORT = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306))
DB_USER = 'root'
DB_PASS = os.getenv('MYSQL_ENV_MYSQL_ROOT_PASSWORD')
DB_NAME = 'dota2_data'
HERO_COUNT = 113
FEATURE_COUNT = HERO_COUNT*2
NUMBER_OF_PLAYER_PER_TEAM = 10

class BundleData():

    def __init__(self):
        # db connection
        self.db = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        self.c = self.db.cursor()
        # datasets
        self.train_set = None
        self.test_set = None

    def getNumberOfMatchStored(self):
        '''get number of match stored in db'''
        sqlstr = """
            SELECT DISTINCT COUNT(*) FROM GameMatch;
        """
        try:
            self.c.execute(sqlstr)
            return self.c.fetchall()[0][0]
        except MySQLdb.Error, e:
            print 'get number of match failed'
            raise e
            self.db.rollback()

    def getFirstNMatch(self, n):
        '''get n number of training set from database'''
        sqlstr = """
            SELECT DISTINCT MATCH_ID, RADIANT_WIN, HERO_ID, TEAM_ID
            FROM GameMatch JOIN MatchPlayer USING (MATCH_ID)
            LIMIT %s
        """
        try:
            self.c.execute(sqlstr, (n * NUMBER_OF_PLAYER_PER_TEAM,))
            print 'training set:'
            res = self.c.fetchall()
            self.train_set = self.organizeData(list(res))
            return self.organizeData(list(res))
        except MySQLdb.Error, e:
            print 'get TRAINING datasets failed'
            raise e
            self.db.rollback()

    def getLastNMatch(self, n):
        '''get n number of testing set from database'''
        sqlstr = """
            SELECT DISTINCT MATCH_ID, RADIANT_WIN, HERO_ID, TEAM_ID
            FROM GameMatch JOIN MatchPlayer USING (MATCH_ID)
            ORDER BY MATCH_ID DESC
            LIMIT %s
        """
        try:
            self.c.execute(sqlstr, (n * NUMBER_OF_PLAYER_PER_TEAM,))
            print('test set:')
            res = self.c.fetchall()
            self.test_set = self.organizeData(list(res))
            return self.organizeData(list(res))
        except MySQLdb.Error, e:
            print 'get TEST datasets failed'
            raise e
            self.db.rollback()

    def getAllDataSets(self):
        '''get all data from database'''
        sqlstr = """
            SELECT DISTINCT MATCH_ID, RADIANT_WIN, HERO_ID, TEAM_ID
            FROM GameMatch JOIN MatchPlayer USING (MATCH_ID)
            ORDER BY MATCH_ID DESC
        """
        try:
            self.c.execute(sqlstr)
            print('total data set:')
            res = self.c.fetchall()
            return self.organizeData(list(res))
        except MySQLdb.Error, e:
            print 'get TOTAL datasets failed'
            raise e
            self.db.rollback()

    def organizeData(self, data):
        ''' reorganize data to groups based on match_id'''

        groups = defaultdict( list )
        [groups[item[0]].append(item[1:]) for item in data]

        x, y = [], []
        for k in dict(groups):
            blanks = [0] * FEATURE_COUNT
            match = groups[k]
            for player in match:
                hero_id = int(player[1]) - 1    # hero list start from 1, need to decr
                if player[2] == 1:              # team_id = dire
                    hero_id = hero_id + HERO_COUNT
                blanks[hero_id] = 1
            x.append(blanks)
            y.append(match[0][0])       # radiant win == 1
        x = np.array(x, dtype=np.float32)
        y = np.array(y, dtype=np.float32)

        if len(x) != len(y):
            print 'error generating dataset: inconsistent dimension with x and y'
        print 'x dimension is {}, y dimension is {}'.format(x.shape, y.shape)
        return (x, y)

if __name__ == '__main__':
    cut = 0.8
    out = {}

    bundle = BundleData()
    matchNum = bundle.getNumberOfMatchStored()

    out['total_set'] = bundle.getAllDataSets()
    out['train_set'] = bundle.getFirstNMatch(matchNum // (1/cut))
    out['test_set'] = bundle.getLastNMatch(matchNum // (1/(1-cut)))

    with open('dota2_data.pkl', 'wb') as f:
        pickle.dump(out, f)
