.. _api-atomlib:

**********************
Atomic Formula Library
**********************


.. automodule:: logic1.atomlib.sympy

.. autoclass:: TermMixin
  :members:
  :undoc-members:

.. autoclass:: AtomicFormula
  :members:

.. autoclass:: BinaryAtomicFormula
  :members: lhs, rhs

  .. property:: dual_func
    :classmethod:

    A class property yielding the dual class of this class or of the
    derived subclass.

    There is an implicit assumption that there are abstract class properties
    `complement_func` and `converse_func` specified, which is technically not
    possible at the moment.


.. autoclass:: Eq
  :members: latex_symbol, text_symbol, simplify

  .. .. attribute: : func
  ..   :type: type[Eq]

  ..   A type annotation for the class property `func` inherited from
  ..   :class:`.firstorder.AtomicFormula.func`.

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`Ne` of
    :class:`Eq`.

  .. property:: converse_func
    :classmethod:

    A class property yielding the converse class :class:`Eq` of
    :class:`Eq`.


.. autoclass:: Ne
  :members: latex_symbol, text_symbol, simplify

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`Eq` of
    :class:`Ne`.

  .. property:: converse_func
    :classmethod:

    A class property yielding the converse class :class:`Ne` of
    :class:`Ne`.


.. autoclass:: Ge
  :members: latex_symbol, text_symbol

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`Lt` of
    :class:`Ge`.

  .. property:: converse_func
    :classmethod:

    A class property yielding the converse class :class:`Le` of
    :class:`Ge`.


.. autoclass:: Le
  :members: latex_symbol, text_symbol

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`Gt` of
    :class:`Le`.

  .. property:: converse_func
    :classmethod:

    A class property yielding the converse class :class:`Ge` of
    :class:`Le`.


.. autoclass:: Gt
  :members: latex_symbol, text_symbol

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`Le` of
    :class:`Gt`.

  .. property:: converse_func
    :classmethod:

    A class property yielding the converse class :class:`Lt` of
    :class:`Gt`.


.. autoclass:: Lt
  :members: latex_symbol, text_symbol

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`Ge` of
    :class:`Lt`.

  .. property:: converse_func
    :classmethod:

    A class property yielding the converse class :class:`Gt` of
    :class:`Lt`.


.. autoclass:: IndexedConstantAtomicFormula
  :members:


.. autoclass:: C
  :members:

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`C_` of :class:`C`.


.. autoclass:: C_
  :members:

  .. property:: complement_func
    :classmethod:

    A class property yielding the complement class :class:`C` of :class:`C_`.
