# Sumset Computations

The purpose of this project is to provide a set of tools that can be used for computations with
subsets of the natural numbers in additive combinatorics. The project is entirely Python-based, 
and no additional dependencies are required.

## Features
* Represent a finite set of non-negative integers with a `Sumset` object
* Form sumsets: `A + B = {a + b; a in A, b in B}`
* Repeated addition with self: `n*A = A + A + ... + A`
* Scalar dilation: `A*n = {n*a : a in A}`
* Compute invariants of a set
  * Doubling constant: `Sumset.doubling_constant`
  * Is AP (True/False): `Sumset.is_arithmetic_progression`
  * Ordered additive energy: `Sumset.additive_energy`

## Repository layout
* `sumset.py`: Sumset class implementation
* `dc_example`: Computes examples of doubling constants for simple sets
* `set_info.py`: Provides relevant information on a user-defined set in a readable format.
* `gen_random_sums.py`: Allows the easy generation of random sets and their sumsets.
* `cantor_set.py`: Allows work with the Cantor set in [0, 1]. Work in progress.
  
## Usage examples

Usage of `Sumset` class
```python
from sumset import Sumset

A = Sumset([1, 2, 3])
2*A                                # Sumset([2, 3, 4, 5, 6])
A*2                                # Sumset([2, 4, 6])

B = Sumset([1, 5])
A + B                              # Sumset([2, 3, 4, 6, 7, 8])

A.doubling_constant                # Fraction(5, 3)
A.is_arithmetic_progression        # True
A.additive_energy                  # 19
```
Output of `set_info.py` program
```bash
[algebraity@T460 sumset-computations]$ python3 set_info.py -s "1 2 3 4 5" -n 5
S = [1, 2, 3, 4, 5]
Cardinality of S: 5
Doubling constant of S: 9/5
Is arithmetic progression: True
Additive energy: 85
iS for 2 <= i <= 5: 
  2*S = Sumset([2, 3, 4, 5, 6, 7, 8, 9, 10])
  3*S = Sumset([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
  4*S = Sumset([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
  5*S = Sumset([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
```

## License and attribution

The contents of this repository are licensed under the GNU General Public License v3.0 (GPL-3.0).
