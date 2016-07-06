import os
import numpy as np
from collections import defaultdict
import theano
import theano.tensor as T

HERO_COUNT = 113
FEATURE_COUNT = HERO_COUNT*2

class LogisticRegression():

    def __init__(self):
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
