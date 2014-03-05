import random
from random import randint

def lhs(mu, sigma, iteration):
    segSize = 1/float(iteration)
    lhs_values = []
    for i in range(iteration):
        segMin = float(i) * segSize
        point = segMin + (random.normalvariate(mu,sigma) * segSize)
        lhs_values.append(point)
    return lhs_values
