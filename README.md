# P-stable-LSH

The package is one implementation of paper Locality-Sensitive Hashing Scheme Based on p-Stable Distributions in SCG’2014. P-stable-lsh a novel Locality-Sensitive Hashing scheme for the Approximate Nearest Neighbor Problem under $L_p$ norm, based on p-stable distributions.

Note: This code is used as the practice of the paper, and there are few optimizations. Sharing is for communication and learning. If it is a high-performance scenario, please optimize as appropriate.

## Install

```
pip install p-stable-lsh-python
```

## Usage

### Example

The following example shows all features of the package, If you want to know the details, please refer to the source code and comments.

```
import numpy as np
import p_stable_lsh.pstable as psl

dim = 100 # vector dimension
data = [np.random.random(dim) for _ in range(2)] # generate two vectors

r = 50.0 # the parameter $r$ in paper

m1 = psl.pstable(r, dim, metric_dim=1)
m1.lsh(data[0])
m2 = psl.pstable(r, dim, metric_dim=1)
m2.lsh(data[1])
print(m1.md(m2)) # estimate value
print(m1.p(np.average(sum(np.abs(data[0]-data[1]))))) # theoretical(true) value

m1 = psl.pstable(r, dim, metric_dim=2)
m1.lsh(data[0])
m2 = psl.pstable(r, dim, metric_dim=2)
m2.lsh(data[1])
print(m1.md(m2)) # estimate value
print(m1.p(np.sqrt(sum([i**2 for i in data[0]-data[1]])))) # theoretical(true) value
```
