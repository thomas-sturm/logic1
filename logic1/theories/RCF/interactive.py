from .bnf import cnf as _cnf
from .bnf import dnf as _dnf
from .parser import l1
from .qe import VirtualSubstitution as _VirtualSubstitution
from .rcf import AtomicFormula, Polynomial, Variable, ring, VV  # noqa
from .simplify import simplify as _simplify


def cnf(x, *args, **kwargs):
    if isinstance(x, str):
        x = l1(x)
    return _cnf(x, *args, **kwargs)


def dnf(x, *args, **kwargs):
    if isinstance(x, str):
        x = l1(x)
    return _dnf(x, *args, **kwargs)


class VirtualSubstitution(_VirtualSubstitution):

    def __call__(self, x, *args, **kwargs):
        if isinstance(x, str):
            x = l1(x)
        return super().__call__(x, *args, **kwargs)


qe = virtual_substitution = VirtualSubstitution()


def simplify(x, *args, **kwargs):
    if isinstance(x, str):
        x = l1(x)
    return _simplify(x, *args, **kwargs)
