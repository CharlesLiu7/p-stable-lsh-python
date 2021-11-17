# -*- coding: UTF-8 -*-
from scipy import integrate
import numpy as np


class pstable:
    """P stable LSH is a probabilistic data structure for computing
    $L_p$ distance between vectors.

    Note:
        This code is used as the practice of the paper, and there are
        few optimizations. If it is a high-performance scenario, please
        optimize as appropriate.
    """

    def __init__(self, r, dim, metric_dim=2, seed=1, num_perm=1024, hashvalues=None):
        """
        Args:
            r (int): The size of equi-width segments $r$ in paper.
            dim (int): Number of dimension of vectors.
            metric_dim (int): The metric $p$ for $L_p$ distance.
            seed (int, optional): The random seed controls the set of random permutation functions generated.
            num_perm (int, optional): Number of random permutation functions.
            hashvalues (`numpy.array` or `list`, optional): The hash values is the internal state of the `pstable.hashvalues`.
            It can be specified for faster initialization using the existing state from another pstable.
        """
        self.r = r
        self.seed = seed
        self.metric_dim = metric_dim
        self.num_perm = num_perm
        self.dim = dim
        if hashvalues is not None:
            self.hashvalues = hashvalues
        self.__init_permutations()

    def __init_permutations(self):
        """Create parameters from a random generation function. Numpy random generator makes the hash values consistent across different Python versions.
        """
        self.gen = np.random.RandomState(self.seed)
        if self.metric_dim == 1:
            self.param_gen = self.__param_cauchy_gen
            self.f = self.f_cauchy
        elif self.metric_dim == 2:
            self.param_gen = self.__param_normal_gen
            self.f = self.f_gaussian
        else:
            raise ValueError("Only support L_1 and L_2 distance metric.")
        self.ab = [self.param_gen(self.dim) for _ in range(self.num_perm)]

    def __len__(self):
        """
        :returns: int -- The number of hash values.
        """
        return len(self.hashvalues)

    def __param_normal_gen(self, dim):
        """Generate $a, b$ for $h_{a,b}(v)$ in paper from normal distribution.
        """
        mu, sigma = 0, 1
        b = self.gen.uniform(0, self.r)
        a = self.gen.normal(mu, sigma, dim)
        return a, b

    def __param_cauchy_gen(self, dim):
        """Generate $a, b$ for $h_{a,b}(v)$ in paper from cauchy distribution.
        """
        b = self.gen.uniform(0, self.r)
        a = self.gen.standard_cauchy(dim)
        return a, b

    def lsh(self, x):
        """Hash the vector x into hash values.

        Args:
            x: The vector to be hashed with (dim, ) shape.
        """
        dim = len(x)
        if dim != self.dim:
            raise ValueError("Vector dimension mismatch")
        self.hashvalues = np.array(
            [np.floor((np.dot(a, x)+b)/self.r) for a, b in self.ab])

    def md(self, other):
        """Estimate metric distance with another pstable object.

        Args:
            other (pstable): The other pstable object.
        """
        if other.seed != self.seed:
            raise ValueError("Cannot compute given PSLSH with different seeds")
        if other.dim != self.dim:
            raise ValueError(
                "Cannot compute given PSLSH with different vector dimension")
        if other.num_perm != self.num_perm:
            raise ValueError(
                "Cannot compute given PSLSH with different numbers of permutation functions")
        if other.metric_dim != self.metric_dim:
            raise ValueError(
                "Cannot compute given PSLSH with different metric dimension")
        return float(np.count_nonzero(self.hashvalues == other.hashvalues)) / float(len(self))

    def f_cauchy(self, x):
        """Standard Cauchy distribution with parameter x.
        """
        return 1/(np.pi*(1+x**2))

    def f_gaussian(self, x):
        """Standard Gaussian distribution with parameter x.
        """
        return np.e**(-x**2/2)/np.sqrt(2*np.pi)

    def pstableProb(self, x, c):
        return self.f(x/c)*(1-x/self.r)/c

    def p(self, c):
        """p(c) function in paper.

        Args:
            c (float): metric distance of two vectors.
        """
        v, err = integrate.quad(lambda t: self.pstableProb(t, c), 0, self.r)
        return 2*v  # maybe typo in paper
