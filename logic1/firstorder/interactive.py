from collections.abc import Sequence
from typing import Any, TypeAlias

from . import boolean
from . import quantified
from .formula import Formula
from .boolean import F, T  # noqa
from .atomic import Variable

Quantifier: TypeAlias = type[quantified.All | quantified.Ex]


def All(variables: object, arg: Formula) -> Formula:
    """Build an All-quantified Formula, checking arguments.
    """
    return _Q(quantified.All, variables, arg)


def And(*args: Formula) -> Formula:
    _check_formulas(*args)
    return boolean.And(*args)


def _check_formulas(*args: object) -> None:
    for arg in args:
        if not isinstance(arg, Formula):
            raise ValueError(f'{arg!r} is not a Formula')


def Equivalent(lhs: Formula, rhs: Formula) -> boolean.Equivalent:
    _check_formulas(lhs, rhs)
    return boolean.Equivalent(lhs, rhs)


def Ex(variables: object, arg: Formula) -> Formula:
    """Build an Ex-quantified Formula, checking arguments.

    >>> from logic1.theories.Sets import Eq, VV
    >>> x, = VV.set_vars('x')
    >>> Ex(x, x == x)
    Ex(x, x == x)

    >>> Ex('x', 'y')
    Traceback (most recent call last):
    ...
    ValueError: 'y' is not a Formula

    >>> Ex('x', Eq(x, x))
    Traceback (most recent call last):
    ...
    ValueError: type of variable 'x' must be <class 'logic1.firstorder.atomic.Term'>
    """
    return _Q(quantified.Ex, variables, arg)


def Implies(lhs: Formula, rhs: Formula) -> boolean.Implies:
    _check_formulas(lhs, rhs)
    return boolean.Implies(lhs, rhs)


def Or(*args: Formula) -> Formula:
    _check_formulas(*args)
    return boolean.Or(*args)


def _Q(q: Quantifier, variables: Any, arg: Formula) -> Formula:
    """Build a q-quantified Formula, checking arguments.
    """
    def check_variables(*args: object) -> None:
        for v in args:
            if not isinstance(v, Variable):
                raise ValueError(f'type of variable {v!r} must be {Variable}')

    _check_formulas(arg)
    match variables:
        case Sequence():
            check_variables(*variables)
            f = arg
            for v in reversed(variables):
                f = q(v, f)
        case _:
            check_variables(variables)
            f = q(variables, arg)
    return f
