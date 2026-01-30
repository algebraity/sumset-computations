import random as rand
from fractions import Fraction

#############################################################################################################################
#                                                                                                                           #
# OOKAMI v1.0.0 --- Licensed under GPL 3.0                                                                                  #
#                                                                                                                           #
# An implementation of methods and properties applicable to a diffset of the integers Z, along with methods of              #
# constructing them. Suitable for research in additive and multiplicative combinatorics on subsets of Z.                    #
#                                                                                                                           #
# ATTIBUTES                                                                                                                 #
# self._set (list): the mathematical set represented by the CombSet object                                                  #
# self.add_cache (dict): a cache storing computed values of i*A                                                             #
# self.diff_cache (dict): a cache storing computed values of A - A - ...                                                    #
# self.mult_cache (dict): a cache storing computed values of A**i                                                           #
# self.rep_add_cache (dict): a cache storing computed values of r_{A+A}(x) for x in A+A                                     #
# self.rep_diff_cache (dict): a cache storing computed values of r_{A-A}(x) for x in A-A                                    #
# self.rep_mult_cache (dict): a cache storing computed values of r_{A*A}(x) for x in A*A                                    #
# self.energies (dict): stores the additive and multiplicative energies once computed                                       #
#                                                                                                                           #
# METHODS                                                                                                                   #
# self.add(x): append an integer x to self._set safely                                                                      #
# self.remove(x): remove an integer x from self._set safely                                                                 #
# self.construct(nums=None): constructs a set, either by taking a list as input to the method, or by taking user input.     #
# self.translate(n): translates the set A by n, returning A + {n} = {a + n : a in A}                                        #
# self.rep_add(x): returns the representation function r_{A+A}(x) for a given x in Z                                        #
# self.rep_diff(x): returns the representation function r_{A-A}(x) for a given x in Z                                       #
# self.rep_mult(x): returns the representation function r_{A*A}(x) for a given x in Z                                       #
#                                                                                                                           #
# self.rand_set(length=0, min_element=0, max_element=0): generates a random CombSet with the paramaters given.              #
# self.info(n): returns a dictionary containing all computable information about the set available in the CombSet class,    #
#               including the list [2*A, 3*A, ..., n*A]                                                                     #
#                                                                                                                           #
# PROPERTIES                                                                                                                #
# self.cardinality: property representing |A|                                                                               #
# self.diameter: property giving the diameter of A                                                                          #
# self.density: property giving |A|/(maxA - minA + 1)                                                                       #
# self.ads: property returning A+A, caching it if not yet computed and reading from self.add_cache otherwise                #
# self.dds: property returning A-A, caching it if not yet computed and reading from self.diff_cache otherwise               #
# self.mds: property returning A*A, caching it if not yet computed and reading from self.mult_cache otherwise               #
# self.ads_cardinality: property giving |A+A|                                                                               #
# self.dds_cardinality: property giving |A-A|                                                                               #
# self.mds_cardinality: property giving |A*A|                                                                               #
# self.doubling_constant: property giving |A + A|/|A| as a Fraction object.                                                 #
# self.is_arithmetic_progression: property returning True if the CombSet object is an arithmetic progression, False o/w.    #
# self.is_geometric_progression: property returning True if the CombSet object is a geometric progression, False o/w.       #
# self.energy_add: property returning the additive energy E(A) of a CombSet object                                          #
# self.energy_mult: property returning the multiplicative energy of a CombSet object                                        #
#                                                                                                                           #
# INTERNAL METHODS                                                                                                          #
# self._clear_cache(): clears self.add_cache and self.mult_cache                                                            #
# self._normalize(): sets self._set = sorted(set(self._set))                                                                #
#                                                                                                                           #
# MAGIC METHODS                                                                                                             #
# self.__add__(): add two CombSet objects as CombSet. A + B = {a + b : a in A, b in B}                                      #
# self.__rmul__(): 3 * A = A + A + A                                                                                        #
# self.__mul__(): A * 3 = {3a : a in A}                                                                                     #
#                 A * B = {a * b : a in A, b in B}                                                                          #
# self.__pow__(): A ** n = A * A * ... * A (negative powers unsupported)                                                    #
# self.__eq__(): A == B if and only if A._set == B._set                                                                     #
# self.__neg__(): -A = {-a : a in A}                                                                                        #
#                                                                                                                           #
#############################################################################################################################
class CombSet():
    def __init__(self, base_set=None):
        if base_set is not None:
            if base_set == []:
                raise ValueError("base_set cannot be empty!")
            self._set = base_set
            self._normalize()
        
        self.add_cache = {}
        self.diff_cache = {}
        self.mult_cache = {}
        self.rep_add_cache = {}
        self.rep_diff_cache = {}
        self.rep_mult_cache = {}
        self.energies = {}

        if base_set is None:
            self.construct()

    def add(self, x):
        self._set.append(x)
        self._normalize()
        self._clear_cache()

    def remove(self, x):
        if x in self._set:
            for i in range(0, self.cardinality):
                if self._set[i] == x:
                    self._set = self._set[:i] + self._set[i+1:]
                    break
        
        self._normalize()
        self._clear_cache()

    def construct(self, nums=None):
        if nums == []:
            raise ValueError("nums cannot be empty.")        
        
        if nums is not None:
            self._set = nums
        else:
            self._set = []
            choice = int(input("Please enter a number to select one of the following options: \n 0: First n elements of kN (enter n, k later) \n 1: Custom set (enter each element later)\nYour choice: "))
            print("\n")
            if choice == 0:
                k = int(input("Enter k as an integer: "))
                n = int(input("Enter n as an integer: "))
                self._set = [k * i for i in range(1, n+1)]
            elif choice == 1:
                current_input = ""
                while True:
                    current_input = input("\nEnter the next element of the set (or \"stop\"): ")
                    if current_input == "stop":
                        break
                    else:
                        i = int(current_input)
                        self._set.append(i)
            else:
                raise ValueError("Invalid input. Selected option must be 0 or 1.")

            print("Set created.")

        if self._set == []:
            raise ValueError("self._set cannot be empty!")
        self._clear_cache()
        self._normalize()

    def translate(self, n):
        translated_set = []
        for i in range(0, len(self._set)):
            translated_set.append(self._set[i] + n)

        return CombSet(translated_set)

    def rep_add(self, x):
        if x in self.rep_add_cache:
            return self.rep_add_cache[x]
        
        rep = 0
        for a in self._set:
            for b in self._set:
                if a + b == x:
                    rep += 1
        
        self.rep_add_cache[x] = rep
        return self.rep_add_cache[x]

    def rep_diff(self, x):
        if x in self.rep_diff_cache:
            return self.rep_diff_cache[x]
        
        rep = 0
        for a in self._set:
            for b in self._set:
                if a - b == x:
                    rep += 1
        
        self.rep_diff_cache[x] = rep
        return self.rep_diff_cache[x]

    def rep_mult(self, x):
        if x in self.rep_mult_cache:
            return self.rep_mult_cache[x]
        
        rep = 0
        for a in self._set:
            for b in self._set:
                if a * b == x:
                    rep += 1
        
        self.rep_mult_cache[x] = rep
        return self.rep_mult_cache[x]

    def rand_set(self, length=0, min_element=0, max_element=0):
        if length == 0:
            raise ValueError("length must be greater than 0.")
        gen_set = []
        if max_element - min_element + 1 < length:
            raise(ValueError("Length higher than range of possible values."))
        while len(gen_set) < length:
            r = rand.randint(min_element, max_element)
            if not r in gen_set:
                gen_set.append(r)

        self._set = gen_set
        self._normalize()
        self._clear_cache()        

    def info(self, n=-1):
        self_sum = self.ads
        self_diff = self.dds
        self_prod = self.mds
        card = self.cardinality
        diam = self.diameter
        densty = self.density
        dc = self.doubling_constant
        is_ap = self.is_arithmetic_progression
        is_gp = self.is_geometric_progression
        add_energy = self.energy_add
        mult_energy = self.energy_mult
        if n > 1:
            sum_list = []
            for i in range(2, n+1):
                sum_list.append(i*self)
            return {"add_ds": self_sum, "diff_ds": self_diff, "mult_ds": self_prod, "cardinality": card, "diameter": diam, "density": densty, "dc": dc, "is_ap": is_ap, "is_gp": is_gp, "add_energy": add_energy, "mult_energy": mult_energy, "i*A_list": sum_list}

        return {"add_ds": self_sum, "diff_ds": self_diff, "mult_ds": self_prod, "cardinality": card, "diameter": diam, "density": densty, "dc": dc, "is_ap": is_ap, "is_gp": is_gp, "add_energy": add_energy, "mult_energy": mult_energy}

    @property
    def cardinality(self):
        return len(self._set)
        
    @property
    def diameter(self):
        return (self._set[-1] - self._set[0])

    @property
    def density(self):
        return self.cardinality / (self._set[-1] - self._set[0] + 1)

    @property
    def ads(self):
        if not 2 in self.add_cache:
            self.add_cache[2] = 2*self
        return self.add_cache[2]
    
    @property
    def dds(self):
        if not 2 in self.diff_cache:
            self.diff_cache[2] = self - self
        return self.diff_cache[2]

    @property
    def mds(self):
        if not 2 in self.mult_cache:
            self.mult_cache[2] = self**2
        return self.mult_cache[2]

    @property
    def ads_cardinality(self):
        return len((self.ads)._set)

    @property
    def dds_cardinality(self):
        return len((self.dds)._set)

    @property
    def mds_cardinality(self):
        return len((self.mds)._set)

    @property
    def doubling_constant(self):
        num = len((self.ads)._set)
        denom = len(self._set)
        return Fraction(num, denom)

    @property
    def is_arithmetic_progression(self):
        if len(self._set) == 1:
            return True
        else:
            d = self._set[1] - self._set[0]
            for i in range(2, len(self._set)):
                if self._set[i] - self._set[i-1] != d:
                    return False
            return True

    @property
    def is_geometric_progression(self):
        if len(self._set) == 1:
            return True
        elif 0 in self._set:
            return False
        else:
            r = Fraction(self._set[1], self._set[0])
            for i in range(2, len(self._set)):
                if Fraction(self._set[i], self._set[i-1]) != r:
                    return False
            return True

    @property
    def energy_add(self):
        if "add" in self.energies:
            return self.energies["add"]
        self.rep_add_cache = {}
        for a in self:
            for b in self:
                if a + b in self.rep_add_cache:
                    self.rep_add_cache[a + b] += 1
                else:
                    self.rep_add_cache[a + b] = 1
        energy = 0
        for r in self.rep_add_cache:
            energy += self.rep_add_cache[r]**2

        self.energies["add"] = energy
        return self.energies["add"]

    @property
    def energy_mult(self):
        if "mult" in self.energies:
            return self.energies["mult"]
        self.rep_mult_cache = {}
        for a in self:
            for b in self:
                if a * b in self.rep_mult_cache:
                    self.rep_mult_cache[a * b] += 1
                else:
                    self.rep_mult_cache[a * b] = 1
        energy = 0
        for r in self.rep_mult_cache:
            energy += self.rep_mult_cache[r]**2

        self.energies["mult"] = energy
        return self.energies["mult"]

    def _clear_cache(self):
        self.add_cache = {}
        self.diff_cache = {}
        self.mult_cache = {}
        self.rep_add_cache = {}
        self.rep_diff_cache = {}
        self.rep_mult_cache = {}
        self.energies = {}

    def _normalize(self):
        for x in self._set:
            if not isinstance(x, int):
                raise TypeError("Set elements must all be integers.")
        self._set = sorted(set(self._set))

    def __add__(self, other):
        if not isinstance(other, CombSet):
            if isinstance(other, int):
                return self.translate(other)
            raise(TypeError)
        if self is other:
            if 2 in self.add_cache:
                return self.add_cache[2]
        new_set = []
        for a in self._set:
            for b in other._set:
                c = a+b
                new_set.append(c)
        if self is other:
            self.add_cache[2] = CombSet(new_set)
            return self.add_cache[2]
        return CombSet(new_set)

    def __sub__(self, other):
        if not isinstance(other, CombSet):
            if isinstance(other, int):
                return self.translate(-other)
            raise(TypeError)
        if self is other:
            if 2 in self.diff_cache:
                return self.diff_cache[2]
        new_set = []
        for a in self._set:
            for b in other._set:
                c = a-b
                new_set.append(c)
        if self is other:
            self.diff_cache[2] = CombSet(new_set)
            return self.diff_cache[2]
        return CombSet(new_set)

    def __rmul__(self, other):
        if isinstance(other, int):
            if other == 0:
                return CombSet([0])
            if other in self.add_cache:
                return self.add_cache[other]
            if other < 0:
                result = -(abs(other) * self)
                self.add_cache[other] = result
                return result
            result = CombSet(self._set)
            times = other-1
            while times > 0:
                result += self
                times -= 1
            self.add_cache[other] = result
            return result
        raise TypeError("Multiplication is only supported for CombSet * CombSet, int * CombSet, and CombSet * int.")

    def __mul__(self, other):
        if isinstance(other, int):
            if other == 0:
                return CombSet([0])
            new_set = (self._set).copy()
            for i in range(0, len(new_set)):
                new_set[i] *= other
            return CombSet(new_set)
        if isinstance(other, CombSet):
            prod_set = []
            if self is other:
                if 2 in self.mult_cache:
                    return self.mult_cache[2]
            for i in self:
                for j in other:
                    prod_set.append(i*j)

            if self is other:
                self.mult_cache[2] = CombSet(prod_set)
                return self.mult_cache[2]
            return CombSet(prod_set)
        
        raise TypeError("Multiplication is only supported for CombSet * CombSet, int * CombSet, and CombSet * int.")

    def __pow__(self, other):
        if isinstance(other, int):
            if other == 0:
                return CombSet([1])
            if other < 0:
                raise TypeError("Negative exponentiation is not supported.")
            if other in self.mult_cache:
                return self.mult_cache[other]
            current = CombSet(self._set)
            n = other
            while n > 1:
                current *= self
                n -= 1

            self.mult_cache[other] = current
            return self.mult_cache[other]
        raise TypeError("Exponentiation is only supported for CombSet ** int.")

    def __str__(self):
        return "CombSet(" + str(self._set) + ")"

    def __iter__(self):
        return iter(self._set)

    def __eq__(self, other):
        if isinstance(other, CombSet):
            return self._set == other._set
        else:
            return False
        
    def __neg__(self):
        return CombSet([-i for i in self._set])

    __repr__ = __str__