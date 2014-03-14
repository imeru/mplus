import random
from random import randint

class Sampling(object):
    def __init__(self, sampling_dist, sampling_method):
        self.sample_values = None
        self.range = None
        self.iteration = None
        self.sampling_dist_type = sampling_dist
        self.sampling_method_type = sampling_method
        if self.sampling_method_type == "lhs":
            self.sampling_method = Lhs(self.sampling_dist_type)
        else:
            raise NotImplementedError("It does not be supported")

    def generate(self, iteration, params):
        self.sample_values = self.sampling_method.generate(iteration, params)
        return self.sample_values

class Lhs(object):
    def __init__(self, sampling_dist):
        self.sampling_dist = sampling_dist

    def generate(self, iteration, params):
        mu = params[0]
        sigma = params[1]
        segSize = 1/float(iteration)
        lhs_values = []
        for i in range(iteration):
            segMin = float(i) * segSize
            point = segMin + (random.normalvariate(mu,sigma) * segSize)
            lhs_values.append(point)
        return lhs_values
