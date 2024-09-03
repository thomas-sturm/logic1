import itertools
from logic1.firstorder import *
from logic1.theories.Sets import *

V = list(VV.get(*(f'c{i}' for i in range(1, 28))))
for v in V:
    VV.imp(str(v))

gamma = [
    # Dummy
    [T],
    # Austria
    [c1 != c11, c1 != c6, c1 != c24, c1 != c13, c1 != c25, c1 != c15],
    # Belgium
    [c2 != c20, c2 != c11, c2 != c18, c2 != c10],
    # Bulgaria
    [c3 != c23, c3 != c12],
    # Croatia
    [c4 != c25, c4 != c13],
    # Cyprus
    [T],
    # Czechia
    [c6 != c11, c6 != c21, c6 != c24, c6 != c1],
    # Denmark
    [c7 != c11],
    # Estonia
    [c8 != c16],
    # Finland
    [c9 != c27],
    # France
    [c10 != c2, c10 != c18, c10 != c11, c10 != c15, c10 != c26],
    # Germany
    [c11 != c7, c11 != c21, c11 != c6, c11 != c1, c11 != c10,
     c11 != c18, c11 != c2, c11 != c20],
    # Greece
    [c12 != c3],
    # Hungary
    [c13 != c24, c13 != c23, c13 != c4, c13 != c25, c13 != c1],
    # Ireland
    [T],
    # Italy
    [c15 != c10, c15 != c1, c15 != c25],
    # Latvia
    [c16 != c8, c16 != c17],
    # Lithuania
    [c17 != c16, c17 != c21],
    # Luxembourg
    [c18 != c2, c18 != c11, c18 != c10],
    # Malta
    [T],
    # Netherlands
    [c20 != c11, c20 != c2],
    # Poland
    [c21 != c17, c21 != c25, c21 != c6, c21 != c11],
    # Portugal
    [c22 != c26],
    # Romania
    [c23 != c3, c23 != c13],
    # Slovakia
    [c24 != c21, c24 != c13, c24 != c1, c24 != c6],
    # Slovenia
    [c25 != c1, c25 != c13, c25 != c4, c25 != c15],
    # Spain
    [c26 != c10, c26 != c22],
    # Sweden
    [c27 != c9]]

psi = And(*(itertools.chain.from_iterable(gamma[1:])))
result = qe(Ex(V, psi))
assert result == C(4), result

# Test espresso
expected = Or(And(c1 == c3, c1 == c5),
              And(c1 == c4, c1 == c5),
              And(c2 == c3, c2 == c5),
              And(c2 == c4, c2 == c5))
actual = dnf(And(Or(c1 == c5, c2 == c5), Or(c3 == c5, c4 == c5)))
assert expected == actual, actual
