import os
import MySQLdb
import numpy as np
from collections import defaultdict
import theano
import theano.tensor as T

DB_HOST = os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1')
DB_PORT = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306))
DB_USER = 'root'
DB_PASS = os.getenv('MYSQL_ENV_MYSQL_ROOT_PASSWORD')
DB_NAME = 'dota2_data'
HERO_COUNT = 113
FEATURE_COUNT = HERO_COUNT*2

class LogisticRegression():

    def __init__(self):
        # db connection
        self.db = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        self.c = self.db.cursor()
        # datasets
        self.D = ()
        self.testD = ()
        # symbolic variables
        self.x = T.dmatrix("x")
        self.y = T.dvector("y")
        self.w = theano.shared(np.random.randn(FEATURE_COUNT), name="w")
        self.b = theano.shared(0., name="b")
        # expression
        self.prediction = None
        self.xent = None
        self.cost = None
        self.gw = None
        self.gb = None
        # function
        self.train = None
        self.predict = None

    def constructGraph(self):
        p_1 = 1 / (1 + T.exp(-T.dot(self.x, self.w) - self.b))   # activation function
        self.prediction = p_1 > 0.5                          # The prediction thresholded
        self.xent = -self.y * T.log(p_1) - (1-self.y) * T.log(1-p_1)   # Cross-entropy loss function
        self.cost = self.xent.mean() + 0.01 * (self.w ** 2).sum()      # The cost to minimize
        self.gw, self.gb = T.grad(self.cost, [self.w, self.b])                   # Compute the gradient of the cost


    def buildFunction(self):
        self.train = theano.function(
          inputs=[self.x, self.y],
          outputs=[self.prediction, self.xent],
          updates=((self.w, self.w - 0.1 * self.gw), (self.b, self.b - 0.1 * self.gb)))
        self.predict = theano.function(inputs=[self.x], outputs=self.prediction)

    def getTrainingDataSets(self):
        sqlstr = """
            SELECT DISTINCT MATCH_ID, RADIANT_WIN, HERO_ID, TEAM_ID
            FROM GameMatch JOIN MatchPlayer USING (MATCH_ID)
            LIMIT 33600
        """
        try:
            self.c.execute(sqlstr)
            res = self.c.fetchall()
            self.D = self.extractData(list(res))
        except MySQLdb.Error, e:
            print 'get TRAINING datasets'
            raise e
            self.db.rollback()

    def getTestingDataSets(self):
        sqlstr = """
            SELECT DISTINCT MATCH_ID, RADIANT_WIN, HERO_ID, TEAM_ID
            FROM GameMatch JOIN MatchPlayer USING (MATCH_ID)
            ORDER BY MATCH_ID DESC
            LIMIT 8400
        """
        try:
            self.c.execute(sqlstr)
            res = self.c.fetchall()
            self.testD = self.extractData(list(res))
        except MySQLdb.Error, e:
            print 'get TEST datasets'
            raise e
            self.db.rollback()

    def extractData(self, data):
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
        x = np.array(x)
        y = np.array(y)

        if len(x) != len(y):
            print 'error generating dataset: inconsistent dimension with x and y'
        print 'x dimension is {}, y dimension is {}'.format(x.shape, y.shape)
        return (x, y)

if __name__ == '__main__':
    lr = LogisticRegression()
    lr.getTrainingDataSets()
    lr.getTestingDataSets()
    lr.constructGraph()
    lr.buildFunction()

    for i in range(1):
        pred, err = lr.train(lr.D[0], lr.D[1])
        # print pred, err

    print("Final model:")
    print(lr.w.get_value())
    print(lr.b.get_value())
    print("target values for D:")
    print(lr.testD[1])
    print("prediction on D:")
    print(lr.predict(lr.testD[0]))

    print("Final model: w: \n {}, \n b: \n {}".format(lr.w.get_value(), lr.b.get_value()))
    #
    pred = lr.predict(lr.testD[0])
    print pred
    #
    zipped = zip(pred, lr.D[1])
    tf = [1 if i[0] == i[1] else 0 for i in zipped]
    print 'precent prediction correct: {} %'.format(sum(tf)*100/200)
