from fractions import Fraction

def gen_cantor(iters, interval=[Fraction(0), Fraction(1)]):
    a = interval[0]
    b = interval[1]
    if iters == 0:
        return interval

    third = (b-a)/3
    il = [a, a + third]
    ir = [a + 2*third, b]

    return gen_cantor(iters-1, il) + gen_cantor(iters-1, ir)

def find_cantor_pair(q):
    if not isinstance(q, Fraction):
        raise(ValueError("q must be a Fraction object"))
    elif not (q >= 0) and (q <= 2):
        raise(ValueError("q must be in the interval [0, 2]"))
    
    return "Work in progress! :)"


