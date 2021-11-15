# -*- coding: UTF-8 -*-
from scipy import integrate
import numpy as np


class pstable:
    def __init__(self, r, metric_dim=2, seed=1, num_perm=1024):
        self.r = r
        self.seed = seed
        self.gen = np.random.RandomState(self.seed)
        self.metric_dim = metric_dim
        if metric_dim == 1:
            self.param_gen = self.param_cauchy_gen
            self.f = self.f_cauchy
        elif metric_dim == 2:
            self.param_gen = self.param_normal_gen
            self.f = self.f_gaussian
        else:
            raise ValueError("Only support L_1 and L_2 distance metric.")
        self.num_perm = num_perm

    def param_normal_gen(self, dim):
        mu, sigma = 0, 1
        b = self.gen.uniform(0, self.r)
        w = self.gen.normal(mu, sigma, dim)
        return w, b

    def param_cauchy_gen(self, dim):
        b = self.gen.uniform(0, self.r)
        w = self.gen.standard_cauchy(dim)
        return w, b

    def lsh(self, x):
        dim = len(x)
        wb = [self.param_gen(dim) for _ in range(self.num_perm)]
        self.hashvalues = np.array(
            [np.floor((np.dot(w, x)+b)/self.r) for w, b in wb])

    def jaccard(self, other):
        if other.seed != self.seed:
            raise ValueError("Cannot compute given PSLSH with different seeds")
        if other.num_perm != self.num_perm:
            raise ValueError(
                "Cannot compute given PSLSH with different numbers of permutation functions")
        if other.metric_dim != self.metric_dim:
            raise ValueError(
                "Cannot compute given PSLSH with different metric dimension")
        return float(np.count_nonzero(self.hashvalues == other.hashvalues)) / float(len(self.hashvalues))

    def f_cauchy(self, x):
        return 1/(np.pi*(1+x**2))

    def f_gaussian(self, x):
        return np.e**(-x**2/2)/np.sqrt(2*np.pi)

    def pstableProb(self, x, c):
        return self.f(x/c)*(1-x/self.r)/c

    def p(self, c):
        v, err = integrate.quad(lambda t: self.pstableProb(t, c), 0, self.r)
        return 2*v