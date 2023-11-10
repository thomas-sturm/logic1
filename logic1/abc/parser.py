from abc import ABC, abstractmethod
import ast
import sys

from ..firstorder import All, And, Equivalent, Ex, F, Implies, Not, Or, T

from ..support.tracing import trace  # noqa


class ParserError(Exception):
    pass


class L1Parser(ABC):

    def process(self, a: ast.expr):
        try:
            return self._process(a)
        except ParserError as exc:
            print(f'{exc.__str__()}', file=sys.stderr)
            raise

    def _process(self, a: ast.expr):
        match a:
            case ast.Call(func=func, args=args):
                assert isinstance(func, ast.Name)
                match func.id:
                    case 'Ex' | 'ex':
                        var = self._process_var(args[0])
                        return Ex(var, *(self._process(arg) for arg in args[1:]))
                    case 'All' | 'all':
                        assert isinstance(args[0], ast.Name)
                        var = self._process_var(args[0])
                        return All(var, *(self._process(arg) for arg in args[1:]))
                    case 'Or':
                        return Or(*(self._process(arg) for arg in args))
                    case 'And':
                        return And(*(self._process(arg) for arg in args))
                    case 'Implies':
                        return Implies(*(self._process(arg) for arg in args))
                    case 'Equivalent':
                        return Equivalent(*(self._process(arg) for arg in args))
                    case _:
                        raise ParserError(f'cannot parse {ast.unparse(a)}')
            case ast.BoolOp(op=op, values=args):
                match op:
                    case ast.Or():
                        return Or(*(self._process(arg) for arg in args))
                    case ast.And():
                        return And(*(self._process(arg) for arg in args))
                    case _:
                        raise ParserError(f'unknown operator {ast.dump(op)} in {ast.unparse(a)}')
            case ast.BinOp(op=op, left=left, right=right):
                match op:
                    case ast.BitOr():
                        return Or(self._process(left), self._process(right))
                    case ast.BitAnd():
                        return And(self._process(left), self._process(right))
                    case ast.RShift():
                        return Implies(self._process(left), self._process(right))
                    case _:
                        raise ParserError(f'unknown operator {ast.dump(op)} in {ast.unparse(a)}')
            case ast.UnaryOp(op=op, operand=operand):
                match op:
                    case ast.Invert() | ast.Not():
                        return Not(self._process(operand))
                    case _:
                        raise ParserError(f'unknown operator {ast.dump(op)} in {ast.unparse(a)}')
            case ast.Name(id=id):
                match id:
                    case 'T' | 'true':
                        return T
                    case 'F' | 'false':
                        return F
                    case _:
                        raise ParserError(f'cannot parse {ast.unparse(a)}')
            case _:
                return self._process_atom(a)

    @abstractmethod
    def _process_atom(self, a):
        ...

    @abstractmethod
    def _process_var(self, v):
        ...