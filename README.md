# P-stable-LSH

The package is one implementation of paper Locality-Sensitive Hashing Scheme Based on p-Stable Distributions in SCG’2014.

## test case

```
import numpy as np
import p_stable_lsh.pstable as psl

data = [np.random.random(100) for _ in range(2)]

m1 = psl.pstable(50, metric_dim=1, num_perm=200000)
m1.lsh(data[0])
m2 = psl.pstable(50, metric_dim=1, num_perm=200000)
m2.lsh(data[1])
print(m1.jaccard(m2)) # estimate value
print(m1.p(np.average(sum(np.abs(data[0]-data[1]))))) # theoretical(true) value

m1 = psl.pstable(50, metric_dim=2, num_perm=200000)
m1.lsh(data[0])
m2 = psl.pstable(50, metric_dim=2, num_perm=200000)
m2.lsh(data[1])
print(m1.jaccard(m2)) # estimate value
print(m1.p(np.sqrt(sum([i**2 for i in data[0]-data[1]])))) # theoretical(true) value
```
