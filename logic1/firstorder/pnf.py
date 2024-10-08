"""Convert to Prenex Normal Form.

A Prenex Normal Form (PNF) is a Negation Normal Form (NNF) in which all
quantifiers :class:`Ex` and :class:`All` stand at the beginning of the
formula. The method used here minimizes the number of quantifier
alternations in the prenex block [Burhenne-1990]_.

.. [Burhenne-1990]
       Klaus-Dieter Burhenne. Implementierung eines Algorithmus zur
       Quantorenelimination für lineare reelle Probleme.
       Diploma Thesis, University of Passau, Germany, 1990
"""

from typing import Generic

from . import (
    All, And, AtomicFormula, BooleanFormula, Ex, _F, Formula, Or,
    QuantifiedFormula, _T)
from .formula import α, τ, χ, σ


class PrenexNormalForm(Generic[α, τ, χ, σ]):

    def __call__(self,
                 f: Formula[α, τ, χ, σ],
                 prefer_universal: bool = False,
                 is_nnf: bool = False) -> Formula[α, τ, χ, σ]:
        return self.pnf(f, prefer_universal=prefer_universal, is_nnf=is_nnf)

    def pnf(self,
            f: Formula[α, τ, χ, σ],
            prefer_universal: bool,
            is_nnf: bool) -> Formula[α, τ, χ, σ]:
        """If the minimal number of alternations in the result can be achieved
        with both :class:`Ex` and :class:`All` as the first quantifier in the
        result, then the former is preferred. This preference can be changed
        with a keyword argument `prefer_universal=True`.

        An keyword argument `is_nnf=True` indicates that `self` is already in
        NNF. :meth:`pnf` then skips the initial NNF computation, which can
        be useful in time-critical situations.
        """
        if not is_nnf:
            f = f.to_nnf()
        f = self.with_distinct_vars(f, set(f.fvars()))
        return self._pnf(f)[All if prefer_universal else Ex]

    def _pnf(self, f: Formula[α, τ, χ, σ]) -> dict[type[All | Ex], Formula[α, τ, χ, σ]]:
        """Private Prenex Normal Form.

        f must be in NNF. Both keys of the result dict are guaranteed to be
        exist. The values are prenex equivalents of f with the same minimized
        number of quantifier alternations. Either d[Ex] starts with an
        existential quantifier and d[All] starts with a universal quantifier,
        or d[Ex] is d[All], i.e., identity is guaranteed.
        """
        # All and Ex are not annotated in the return type, because they are not
        # used as quantifiers but as dictionary keys.
        match f:
            case AtomicFormula() | _F() | _T():
                return {Ex: f, All: f}
            case And() | Or():
                L1 = []
                L2 = []
                for arg in f.args:
                    d = self._pnf(arg)
                    L1.append(d[Ex])
                    L2.append(d[All])
                f1 = self.interchange(f.op(*L1), Ex)
                f2 = self.interchange(f.op(*L2), All)
                if f1.op is not Ex and f2.op is not All:
                    # f is quantifier-free
                    return {Ex: f, All: f}
                f1_alternations = f1.count_alternations()
                f2_alternations = f2.count_alternations()
                d = {}
                if f1_alternations == f2_alternations:
                    d[Ex] = f1 if f1.op is Ex else f2
                    d[All] = f2 if f2.op is All else f1
                    return d
                if f1_alternations < f2_alternations:
                    d[Ex] = d[All] = f1
                    return d
                d[Ex] = d[All] = f2
                return d
            case All() | Ex():
                new_f = f.op(f.var, self._pnf(f.arg)[f.op])
                return {Ex: new_f, All: new_f}
            case _:
                assert False

    def interchange(self, f: And[α, τ, χ, σ] | Or[α, τ, χ, σ], q: type[Ex | All]) -> Formula[α, τ, χ, σ]:
        # All and Ex are not annotated in the return type, because they are not
        # used as quantifiers but as dictionary keys.
        quantifiers = []
        quantifier_positions = set()
        args = list(f.args)
        while True:
            found_quantifier = False
            for i, arg_i in enumerate(args):
                while isinstance(arg_i, q):
                    # I think it follows from the type hints that arg_i is
                    # an instance of Ex or All, but mypy 1.0.1 cannot see
                    # that.
                    quantifiers += [(q, arg_i.var)]  # type: ignore
                    arg_i = arg_i.arg  # type: ignore
                    quantifier_positions.update({i})
                    found_quantifier = True
                args[i] = arg_i
            if not found_quantifier:
                break
            q = q.dual()
        # The lifting of quantifiers above can introduce direct nested
        # ocurrences of self.op, which is one of And, Or. We
        # flatten those now, but not any other nestings.
        args_pnf: list[Formula] = []
        for i, arg in enumerate(args):
            if i in quantifier_positions and arg.op is f.op:
                args_pnf += arg.args
            else:
                args_pnf += [arg]
        pnf: Formula = f.op(*args_pnf)
        for q, v in reversed(quantifiers):
            pnf = q(v, pnf)
        return pnf

    def with_distinct_vars(self, f: Formula[α, τ, χ, σ], badlist: set[χ]) -> Formula[α, τ, χ, σ]:
        """Convert to equivalent formula with distinct variables.

        Bound variables are renamed such that that set of all bound variables
        is disjoint from the set of all free variables. Furthermore, each bound
        variable in the result occurs with one and only one quantifier.

        Recursively traverse self. If a badlisted variable is encountered as a
        quantified variable, it will be replaced with a fresh name in the
        respective QuantifiedFormula, and the fresh name will be badlisted for
        the future. Note that this can includes variables that do not *occur*
        in a mathematical sense.
        """
        match f:
            case QuantifiedFormula(op=Q, var=var, arg=arg):
                new_arg = self.with_distinct_vars(arg, badlist)
                if var in badlist:
                    new_var = var.fresh()
                    new_arg = new_arg.subs({var: new_var})
                    badlist.update({new_var})  # mutable
                    return Q(new_var, new_arg)
                badlist.update({var})
                return Q(var, new_arg)
            case BooleanFormula(op=op, args=args):
                return op(*(self.with_distinct_vars(arg, badlist) for arg in args))
            case AtomicFormula():
                return f
            case _:
                assert False
