"""We introduce formulas with Boolean toplevel operators as subclasses of
:class:`.Formula`.
"""
from __future__ import annotations

from typing import final, Optional

from .formula import Formula

from ..support.tracing import trace  # noqa


class BooleanFormula(Formula):
    r"""A class whose instances are Boolean formulas in the sense that their
    toplevel operator is one of the Boolean operators :math:`\top`,
    :math:`\bot`, :math:`\lnot`, :math:`\wedge`, :math:`\vee`,
    :math:`\longrightarrow`, :math:`\longleftrightarrow`.
    """
    pass


@final
class Equivalent(BooleanFormula):
    r"""A class whose instances are equivalences in the sense that their
    toplevel operator represents the Boolean operator
    :math:`\longleftrightarrow`.

    >>> from logic1.theories.RCF import *
    >>> x, = VV.get('x')
    >>> Equivalent(x >= 0, Or(x > 0, x == 0))
    Equivalent(x >= 0, Or(x > 0, x == 0))
    """
    @property
    def lhs(self) -> Formula:
        """The left-hand side of the equivalence.

        .. seealso::
            * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
            * :attr:`op <.formula.Formula.op>` -- operator
        """
        return self.args[0]

    @property
    def rhs(self) -> Formula:
        """The right-hand side of the equivalence.

        .. seealso::
            * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
            * :attr:`op <.formula.Formula.op>` -- operator
        """
        return self.args[1]

    def __init__(self, lhs: Formula, rhs: Formula) -> None:
        # discuss: To what extent does this check for 2 args?
        self.args = (lhs, rhs)


@final
class Implies(BooleanFormula):
    """A class whose instances are equivalences in the sense that their
    toplevel operator represents the Boolean operator :math:`\\longrightarrow`.

    >>> from logic1.theories.RCF import *
    >>> x, = VV.get('x')
    >>> Implies(x == 0, x >= 0)
    Implies(x == 0, x >= 0)

    .. seealso::
        * :meth:`>>, __rshift__() <.formula.Formula.__rshift__>` -- \
            infix notation of :class:`Implies`
        * :meth:`\<\<, __lshift__() <.formula.Formula.__lshift__>` -- \
            infix notation of converse :class:`Implies`
    """  # noqa
    @property
    def lhs(self) -> Formula:
        """The left-hand side of the implication.

        .. seealso::
            * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
            * :attr:`op <.formula.Formula.op>` -- operator
        """
        return self.args[0]

    @property
    def rhs(self) -> Formula:
        """The right-hand side of the implication.

        .. seealso::
            * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
            * :attr:`op <.formula.Formula.op>` -- operator
        """
        return self.args[1]

    def __init__(self, lhs: Formula, rhs: Formula) -> None:
        self.args = (lhs, rhs)


@final
class And(BooleanFormula):
    """A class whose instances are conjunctions in the sense that their
    toplevel operator represents the Boolean operator
    :math:`\\wedge`.

    >>> from logic1.theories.RCF import *
    >>> x, y, z = VV.get('x', 'y', 'z')
    >>> And()
    T
    >>> And(x == 0)
    x == 0
    >>> And(x == 1, x == y, y == z)
    And(x - 1 == 0, x - y == 0, y - z == 0)

    .. seealso::
        * :meth:`&, __and__() <.formula.Formula.__and__>` -- \
            infix notation of :class:`And`
        * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
        * :attr:`op <.formula.Formula.op>` -- operator
    """
    @classmethod
    def dual(cls) -> type[Or]:
        r"""A class method yielding the class :class:`Or`, which implements
        the dual operator :math:`\vee` of :math:`\wedge`.
        """
        return Or

    @classmethod
    def definite(cls) -> type[_F]:
        r"""A class method yielding the class :class:`_F`, which is the
        operator of the constant Formula :data:`F`. The definite is the dual of
        the neutral.
        """
        return _F

    @classmethod
    def definite_element(cls) -> _F:
        r"""A class method yielding the unique instance :data:`F` of the
        :class:`_F`.
        """
        return F

    @classmethod
    def neutral(cls) -> type[_T]:
        r"""A class method yielding the class :class:`_T`, which is the
        operator of the constant Formula :data:`T`. The neutral is the dual of
        the definite.
        """
        return _T

    @classmethod
    def neutral_element(cls) -> _T:
        r"""A class method yielding the unique instance :data:`T` of the
        :class:`_T`.
        """
        return T

    def __new__(cls, *args: Formula):
        if not args:
            return T
        if len(args) == 1:
            return args[0]
        return super().__new__(cls)

    def __init__(self, *args: Formula) -> None:
        """
        >>> from logic1.theories.RCF import *
        >>> a, = VV.get('a')
        >>> And(a >= 0, a != 0)
        And(a >= 0, a != 0)
        """
        args_flat = []
        for arg in args:
            if isinstance(arg, And):
                args_flat.extend(list(arg.args))
            else:
                args_flat.append(arg)
        self.args = tuple(args_flat)


@final
class Or(BooleanFormula):
    """A class whose instances are disjunctions in the sense that their
    toplevel operator represents the Boolean operator
    :math:`\\vee`.

    >>> from logic1.theories.RCF import *
    >>> x, = VV.get('x')
    >>> Or()
    F
    >>> Or(x == 0)
    x == 0
    >>> Or(x == 1, x == 2, x == 3)
    Or(x - 1 == 0, x - 2 == 0, x - 3 == 0)

    .. seealso::
        * :meth:`|, __or__() <.formula.Formula.__or__>` -- \
            infix notation of :class:`Or`
        * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
        * :attr:`op <.formula.Formula.op>` -- operator
    """
    @classmethod
    def dual(cls) -> type[And]:
        r"""A class method yielding the class :class:`And`, which implements
        the dual operator :math:`\wedge` of :math:`\vee`.
        """
        return And

    @classmethod
    def definite(cls) -> type[_T]:
        r"""A class method yielding the class :class:`_T`, which is the
        operator of the constant Formula :data:`T`. The definite is the dual of
        the neutral.
        """
        return _T

    @classmethod
    def definite_element(cls) -> _T:
        r"""A class method yielding the unique instance :data:`T` of the
        :class:`_T`.
        """
        return T

    @classmethod
    def neutral(cls) -> type[_F]:
        r"""A class method yielding the class :class:`_F`, which is the
        operator of the constant Formula :data:`F`. The neutral is the dual of
        the definite.
        """
        return _F

    @classmethod
    def neutral_element(cls) -> _F:
        r"""A class method yielding the unique instance :data:`F` of the
        :class:`_F`.
        """
        return F

    def __new__(cls, *args):
        if not args:
            return F
        if len(args) == 1:
            return args[0]
        return super().__new__(cls)

    def __init__(self, *args) -> None:
        """
        >>> from logic1.theories.RCF import *
        >>> a, = VV.get('a')
        >>> Or(a > 0, a == 0)
        Or(a > 0, a == 0)
        """
        args_flat = []
        for arg in args:
            if isinstance(arg, Or):
                args_flat.extend(list(arg.args))
            else:
                args_flat.append(arg)
        self.args = tuple(args_flat)


@final
class Not(BooleanFormula):
    """A class whose instances are negated formulas in the sense that their
    toplevel operator is the Boolean operator
    :math:`\\neg`.

    >>> from logic1.theories.RCF import *
    >>> a, = VV.get('a')
    >>> Not(a == 0)
    Not(a == 0)

    .. seealso::
        * :meth:`~, __invert__() <.formula.Formula.__invert__>` -- \
            short notation of :class:`Not`
    """
    @property
    def arg(self) -> Formula:
        """The one argument of the operator :math:`\\neg`.

        .. seealso::
            * :attr:`args <.formula.Formula.op>` -- all arguments as a tuple
            * :attr:`op <.formula.Formula.op>` -- operator
        """
        return self.args[0]

    def __init__(self, arg: Formula) -> None:
        """
        >>> from logic1.theories.RCF import *
        >>> a, = VV.get('a')
        >>> Not(a == 0)
        Not(a == 0)
        """
        self.args = (arg, )


def involutive_not(arg: Formula) -> Formula:
    """Construct a formula equivalent Not(arg) using the involutive law if
    applicable.

    >>> from logic1.theories.RCF import *
    >>> x, = VV.get('x')
    >>> involutive_not(x == 0)
    Not(x == 0)
    >>> involutive_not(Not(x == 0))
    x == 0
    >>> involutive_not(T)
    Not(T)
    """
    if isinstance(arg, Not):
        return arg.arg
    return Not(arg)


@final
class _T(BooleanFormula):
    """A singleton class whose sole instance represents the constant Formula
    that is always true.

    >>> _T()
    T
    >>> _T() is _T()
    True
    """

    # This is a quite basic implementation of a singleton class. It does not
    # support subclassing. We do not use a module because we need _T to be a
    # subclass itself.

    @classmethod
    def dual(cls) -> type[_F]:
        r"""A class method yielding the class :class:`_F`, which implements
        the dual operator :math:`\bot` of :math:`\top`.
        """
        return _F

    _instance: Optional[_T] = None

    def __init__(self) -> None:
        self.args = ()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return 'T'


T = _T()
"""Support use as a constant without parentheses.

    >>> T is _T()
    True
"""


@final
class _F(BooleanFormula):
    """A singleton class whose sole instance represents the constant Formula
    that is always false.

    >>> _F()
    F
    >>> _F() is _F()
    True
    """

    # This is a quite basic implementation of a singleton class. It does not
    # support subclassing. We do not use a module because we need _F to be a
    # subclass itself.

    @classmethod
    def dual(cls) -> type[_T]:
        r"""A class method yielding the class :class:`_T`, which implements
        the dual operator :math:`\top` of :math:`\bot`.
        """
        return _T

    _instance: Optional[_F] = None

    def __init__(self) -> None:
        self.args = ()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return 'F'


F = _F()
"""Support use as a constant without parentheses.

    >>> F is _F()
    True
"""
