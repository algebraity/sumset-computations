# OOKAMI v1.1.0

*Licensed under GPL 3.0*

An implementation of methods and properties applicable to a diffset of the integers ( \mathbb{Z} ), along with methods for constructing them. Suitable for research in additive and multiplicative combinatorics on subsets of ( \mathbb{Z} ).

---

## combset.py

### Dependencies

The 'combset' module depends on the following standard-library modules:

- 'random'
- 'fractions'
- 'numpy'

---

### Attributes

* `self._set: np.ndarray`
  The mathematical set represented by the `CombSet` object.

* `self.add_cache: dict[int, "CombSet"]`
  Cache storing computed values of ( iA ).

* `self.diff_cache: dict[int, "CombSet"]`
  Cache storing computed values of ( A - A - \dots ).

* `self.mult_cache: dict[int, "CombSet"]`
  Cache storing computed values of ( A^i ).

* `self.rep_add_cache: dict[int, int]`
  Cache storing computed values of the representation function ( r_{A+A}(x) ) for ( x \in A+A ).

* `self.rep_diff_cache: dict[int, int]`
  Cache storing computed values of the representation function ( r_{A-A}(x) ) for ( x \in A-A ).

* `self.rep_mult_cache: dict[int, int]`
  Cache storing computed values of the representation function ( r_{A\cdot A}(x) ) for ( x \in A\cdot A ).

* `self.energies: dict[str, int]`
  Stores additive and multiplicative energies once computed.

---

### Methods

* `add(self, x: int) -> None`
  Append an integer `x` to `self._set` safely.

* `remove(self, x: int) -> None`
  Remove an integer `x` from `self._set` safely.

* `construct(self, nums: list[int] | None = None) -> None`
  Construct a set, either from a provided list or via user input.

* `translate(self, n: int) -> "CombSet"`
  Translate the set ( A ) by `n`, returning
  ( A + {n} = {a + n : a \in A} ).

* `rep_add(self, x: int) -> int`
  Return the representation function ( r_{A+A}(x) ) for a given integer `x`.

* `rep_diff(self, x: int) -> int`
  Return the representation function ( r_{A-A}(x) ) for a given integer `x`.

* `rep_mult(self, x: int) -> int`
  Return the representation function ( r_{A\cdot A}(x) ) for a given integer `x`.

* `rand_set(self, length: int = 0, min_element: int = 0, max_element: int = 0) -> "CombSet"`
  Generate a random `CombSet` with the given parameters.

* `info(self, n: int) -> dict[str, object]`
  Return a dictionary containing all computable information about the set available in the `CombSet` class, including the list
  ([2A, 3A, \dots, nA]).

---

### Properties

* `cardinality: int`
  The cardinality ( |A| ).

* `diameter: int`
  The diameter of ( A ).

* `density: float`
  The density ( |A| / (\max A - \min A + 1) ).

* `ads: "CombSet"`
  The sumset ( A + A ); cached after first computation.

* `dds: "CombSet"`
  The difference set ( A - A ); cached after first computation.

* `mds: "CombSet"`
  The product set ( A \cdot A ); cached after first computation.

* `ads_cardinality: int`
  The cardinality ( |A + A| ).

* `dds_cardinality: int`
  The cardinality ( |A - A| ).

* `mds_cardinality: int`
  The cardinality ( |A \cdot A| ).

* `doubling_constant: Fraction`
  The doubling constant ( |A + A| / |A| ).

* `is_arithmetic_progression: bool`
  `True` if the set is an arithmetic progression, `False` otherwise.

* `is_geometric_progression: bool`
  `True` if the set is a geometric progression, `False` otherwise.

* `energy_add: int`
  The additive energy ( E(A) ).

* `energy_mult: int`
  The multiplicative energy of the set.

---

### Internal Methods

* `_clear_cache(self) -> None`
  Clear `self.add_cache` and `self.mult_cache`.

* `_normalize(self) -> None`
  Normalize the set by assigning
  `self._set = np.asarray(self._set, dtype=np.int64)`
  if not already an array, and then
  `self._set = np.unique(self._set)`

---

### Magic Methods

* `__add__(self, other: "CombSet") -> "CombSet"`
  Add two `CombSet` objects:
  ( A + B = {a + b : a \in A, b \in B} ).

* `__rmul__(self, n: int) -> "CombSet"`
  Scalar addition:
  ( n \cdot A = A + A + \dots + A ).

* `__mul__(self, other: int | "CombSet") -> "CombSet"`

  * ( A \cdot n = {na : a \in A} )
  * ( A \cdot B = {ab : a \in A, b \in B} )

* `__pow__(self, n: int) -> "CombSet"`
  Repeated product:
  ( A^n = A \cdot A \cdot \dots \cdot A )
  (negative powers unsupported).

* `__eq__(self, other: object) -> bool`
  Equality holds if and only if `self._set == other._set`.

* `__neg__(self) -> "CombSet"`
  Negation:
  ( -A = {-a : a \in A} ).

