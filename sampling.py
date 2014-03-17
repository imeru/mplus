import random
from scipy.stats.distributions import norm, triang
import pyDOE

class Lhs(object):
    """
    Generate a latin-hypercube design

    Parameters
    ----------
    sampling_dist: string
        Models of distributions: uniform, normal, triang

    Example
    -------
    A 1-factor design with uniform distribution

        >>> sampling = Lhs(sampling_dist='uniform', n=1, samples=10).generate()

    Reference
    ---------
    pyDOE, lhs: http://pythonhosted.org/pyDOE/randomized.html#latin-hypercube
    Models of dist: http://docs.scipy.org/doc/scipy/reference/stats.html
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.sampling_dist = kwargs['sampling_dist']

    def generate(self):
        if self.sampling_dist == 'uniform':
            lhd = self._uniform_generate()
        elif self.sampling_dist == 'normal':
            lhd = self._normal_generate()
        elif self.sampling_dist == 'triang':
            lhd = self._triang_generate()
        else:
            raise NotImplementedError("It does not be supported")
        # flatten ndarray and make it to list
        return lhd.flatten().tolist()

    def _uniform_generate(self):
        n = self.kwargs['n']
        samples = self.kwargs['samples']
        lhd = pyDOE.lhs(n, samples)
        return lhd

    def _normal_generate(self):
        loc = self.kwargs['loc']
        scales = self.kwargs['scales']
        lhd = self._uniform_generate(n, samples)
        lhd = norm(loc, scales=1).ppf(lhd)
        return lhd

    def _triang_generate(self):
        min = self.kwargs['min']
        max = self.kwargs['max']
        mod = self.kwargs['mod']
        loc = min
        scale = max - min
        c = (mod - min) / (max - min)
        lhd = self._uniform_generate(n, samples)
        lhd = triang(c, loc, scale).ppf(lhd)
        return lhd
