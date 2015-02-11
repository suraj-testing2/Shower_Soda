"""Mapping between slot / operator names.

This defines the internal constants CPython uses to map magic methods to slots
of PyTypeObject structures, and also other constants, like compare operator
mappings.
"""


import collections


TYPEOBJECT_PREFIX = "tp_"
NUMBER_PREFIX = "nb_"
SEQUENCE_PREFIX = "sq_"
MAPPING_PREFIX = "mp_"


class Slot(object):
  """A "slot" describes a Python operator.

  In particular, it describes how a magic method (E.g. "__add__") relates to the
  opcode ("BINARY_ADD") and the C function pointer ("nb_add").

  Args:
    python_name: The name of the Python method. E.g. "__add__".
    c_name: The name of the C function pointer. Only use the base name, e.g.
      for tp_as_number->nb_add, use nb_add.
    function_type: Type of the C function
    index: If multiple python methods share the same function pointer
      (e.g. __add__ and __radd__), this is 0 or 1.
    opcode: The name of the opcode that CPython uses to call this
      function. This is only filled in for operators (e.g. BINARY_SUBSCR),
      but not for operations (e.g. STORE_SUBSCR).
    python_version: "2", "3", or (default) "*"
  """

  def __init__(self, python_name, c_name, function_type, index=None,
               opcode=None, python_version="*"):
    self.python_name = python_name
    self.c_name = c_name
    self.function_type = function_type
    self.index = index
    self.opcode = opcode
    self.python_version = python_version


SLOTS = [
    # typeobject
    Slot("__new__", "tp_new", "new"),
    Slot("__init__", "tp_init", "init"),
    Slot("__str__", "tp_print", "print"),
    Slot("__repr__", "tp_repr", "repr"),

    Slot("__hash__", "tp_hash", "hash"),
    Slot("__call__", "tp_call", "call"),

    # Note: In CPython, if tp_getattro exists, tp_getattr is never called.
    Slot("__getattribute__", "tp_getattro", "getattro"),
    Slot("__getattr__", "tp_getattro", "getattro"),
    Slot("__setattr__", "tp_setattro", "setattro"),
    Slot("__delattr__", "tp_setattro", "setattro"),

    # for Py_TPFLAGS_HAVE_ITER:
    Slot("__iter__", "tp_iter", "unary"),
    Slot("next", "tp_iternext", "next", python_version="2"),
    Slot("__next__", "tp_iternext", "next", python_version="3"),

    # for Py_TPFLAGS_HAVE_CLASS:
    Slot("__get__", "tp_descr_get", "descr_get"),
    Slot("__set__", "tp_descr_set", "descr_set"),
    Slot("__delete__", "tp_descr_set", "descr_delete"),
    Slot("__del__", "tp_del", "destructor"),

    # all typically done by __richcompare__
    Slot("__cmp__", "tp_compare", "cmp",
         python_version="2"),  # "tp_reserved" in Python 3
    Slot("__lt__", "tp_richcompare", "richcmpfunc"),
    Slot("__le__", "tp_richcompare", "richcmpfunc"),
    Slot("__eq__", "tp_richcompare", "richcmpfunc"),
    Slot("__ne__", "tp_richcompare", "richcmpfunc"),
    Slot("__gt__", "tp_richcompare", "richcmpfunc"),
    Slot("__ge__", "tp_richcompare", "richcmpfunc"),

    Slot("__richcompare__", "tp_richcompare", "richcmpfunc"),

    # number methods:
    Slot("__add__", "nb_add", "binary_nb", index=0,
         opcode="BINARY_ADD"),
    Slot("__radd__", "nb_add", "binary_nb", index=1),
    Slot("__sub__", "nb_subtract", "binary_nb", index=0,
         opcode="BINARY_SUBTRACT"),
    Slot("__rsub__", "nb_subtract", "binary_nb", index=1),
    Slot("__mul__", "nb_multiply", "binary_nb", index=0),
    Slot("__rmul__", "nb_multiply", "binary_nb", index=1),
    Slot("__div__", "nb_divide", "binary_nb", index=0,
         opcode="BINARY_DIVIDE"),
    Slot("__rdiv__", "nb_divide", "binary_nb", index=1),
    Slot("__mod__", "nb_remainder", "binary_nb", index=0,
         opcode="BINARY_MODULO"),
    Slot("__rmod__", "nb_remainder", "binary_nb", index=1),
    Slot("__divmod__", "nb_divmod", "binary_nb", index=0),
    Slot("__rdivmod__", "nb_divmod", "binary_nb", index=1),
    Slot("__lshift__", "nb_lshift", "binary_nb", index=0,
         opcode="BINARY_LSHIFT"),
    Slot("__rlshift__", "nb_lshift", "binary_nb", index=1),
    Slot("__rshift__", "nb_rshift", "binary_nb", index=0,
         opcode="BINARY_RSHIFT"),
    Slot("__rrshift__", "nb_rshift", "binary_nb", index=1),
    Slot("__and__", "nb_and", "binary_nb", index=0,
         opcode="BINARY_AND"),
    Slot("__rand__", "nb_and", "binary_nb", index=1),
    Slot("__xor__", "nb_xor", "binary_nb", index=0,
         opcode="BINARY_XOR"),
    Slot("__rxor__", "nb_xor", "binary_nb", index=1),
    Slot("__or__", "nb_or", "binary_nb", index=0,
         opcode="BINARY_OR"),
    Slot("__ror__", "nb_or", "binary_nb", index=1),
    # needs Py_TPFLAGS_HAVE_CLASS:
    Slot("__floordiv__", "nb_floor_divide", "binary_nb", index=0,
         opcode="BINARY_FLOOR_DIVIDE"),
    Slot("__rfloordiv__", "nb_floor_divide", "binary_nb", index=1),
    Slot("__truediv__", "nb_true_divide", "binary_nb", index=0,
         opcode="BINARY_TRUE_DIVIDE"),
    Slot("__rtruediv__", "nb_true_divide", "binary_nb", index=1),

    Slot("__pow__", "nb_power", "ternary",
         opcode="BINARY_POWER"),
    Slot("__rpow__", "nb_power", "ternary"),  # needs wrap_tenary_nb

    Slot("__neg__", "nb_negative", "unary",
         opcode="UNARY_NEGATIVE"),
    Slot("__pos__", "nb_positive", "unary",
         opcode="UNARY_POSITIVE"),
    Slot("__abs__", "nb_absolute", "unary"),
    Slot("__nonzero__", "nb_nonzero", "inquiry"),
    Slot("__invert__", "nb_invert", "unary",
         opcode="UNARY_INVERT"),
    Slot("__coerce__", "nb_coerce", "coercion"),  # not needed
    Slot("__int__", "nb_int", "unary"),  # expects exact int as return
    Slot("__long__", "nb_long", "unary"),  # expects exact long as return
    Slot("__float__", "nb_float", "unary"),  # expects exact float as return
    Slot("__oct__", "nb_oct", "unary"),
    Slot("__hex__", "nb_hex", "unary"),

    # Added in 2.0.  These are probably largely useless.
    # (For list concatenation, use sl_inplace_concat)
    Slot("__iadd__", "nb_inplace_add", "binary",
         opcode="INPLACE_ADD"),
    Slot("__isub__", "nb_inplace_subtract", "binary",
         opcode="INPLACE_SUBTRACT"),
    Slot("__imul__", "nb_inplace_multiply", "binary",
         opcode="INPLACE_MUL"),
    Slot("__idiv__", "nb_inplace_divide", "binary",
         opcode="INPLACE_DIV"),
    Slot("__irem__", "nb_inplace_remainder", "binary",
         opcode="INPLACE_MODULO"),
    Slot("__ipow__", "nb_inplace_power", "ternary",
         opcode="INPLACE_POWER"),
    Slot("__ilshift__", "nb_inplace_lshift", "binary",
         opcode="INPLACE_LSHIFT"),
    Slot("__irshift__", "nb_inplace_rshift", "binary",
         opcode="INPLACE_RSHIFT"),
    Slot("__iand__", "nb_inplace_and", "binary",
         opcode="INPLACE_AND"),
    Slot("__ixor__", "nb_inplace_xor", "binary",
         opcode="INPLACE_XOR"),
    Slot("__ior__", "nb_inplace_or", "binary",
         opcode="INPLACE_OR"),
    Slot("__ifloordiv__", "nb_inplace_floor_divide", "binary",
         opcode="INPLACE_FLOOR_DIVIDE"),
    Slot("__itruediv__", "nb_inplace_true_divide", "binary",
         opcode="INPLACE_TRUE_DIVIDE"),

    # Added in 2.5. Used whenever i acts as a sequence index (a[i])
    Slot("__index__", "nb_index", "unary"),  # needs int/long return

    # mapping
    # __getitem__: Python first tries mp_subscript, then sq_item
    # __len__: Python first tries sq_length, then mp_length
    # __delitem__: Reuses __setitem__ slot.
    Slot("__getitem__", "mp_subscript", "binary",
         opcode="BINARY_SUBSCR"),
    Slot("__delitem__", "mp_ass_subscript", "objobjargproc", index=0),
    Slot("__setitem__", "mp_ass_subscript", "objobjargproc", index=1),
    Slot("__len__", "mp_length", "len"),

    # sequence
    Slot("__contains__", "sq_contains", "objobjproc"),

    # These sequence methods are duplicates of number or mapping methods.
    # For example, in the C API, "add" can be implemented either by sq_concat,
    # or by np_add.  Python will try both. The opcode mapping is identical
    # between the two. So e.g. the implementation of the BINARY_SUBSCR opcode in
    # Python/ceval.c will try both sq_item and mp_subscript, which is why this
    # opcode appears twice in our list.
    Slot("__add__", "sq_concat", "binary",
         opcode="BINARY_ADD"),
    Slot("__mul__", "sq_repeat", "indexargfunc",
         opcode="BINARY_MULTIPLY"),
    Slot("__iadd__", "sq_inplace_concat", "binary",
         opcode="INPLACE_ADD"),
    Slot("__imul__", "sq_inplace_repeat", "indexargfunc",
         opcode="INPLACE_MUL"),
    Slot("__getitem__", "sq_item", "sq_item",
         opcode="BINARY_SUBSCR"),
    Slot("__setitem__", "sq_ass_slice", "sq_ass_item"),
    Slot("__delitem__", "sq_ass_item", "sq_delitem"),

    # slices are passed as explicit slice objects to mp_subscript.
    Slot("__getslice__", "sq_slice", "sq_slice"),
    Slot("__setslice__", "sq_ass_slice", "ssizessizeobjarg"),
    Slot("__delslice__", "sq_ass_slice", "delslice"),
]


CompareOp = collections.namedtuple("CompareOp", ["op", "index", "magic"])


CMP_LT = 0
CMP_LE = 1
CMP_EQ = 2
CMP_NE = 3
CMP_GT = 4
CMP_GE = 5
CMP_IN = 6
CMP_NOT_IN = 7
CMP_IS = 8
CMP_IS_NOT = 9
CMP_EXC_MATCH = 9


COMPARE_OPS = [
    CompareOp("LT", CMP_LT, "__lt__"),
    CompareOp("LE", CMP_LE, "__le__"),
    CompareOp("EQ", CMP_EQ, "__eq__"),
    CompareOp("NE", CMP_NE, "__ne__"),
    CompareOp("GT", CMP_GT, "__gt__"),
    CompareOp("GE", CMP_GE, "__ge__"),
    CompareOp("IN", CMP_IN, None),  # reversed __contains__
    # these don't have a magic function:
    CompareOp("NOT_IN", CMP_NOT_IN, None),
    CompareOp("IS", CMP_IS, None),
    CompareOp("IS_NOT", CMP_IS_NOT, None),
    CompareOp("EXC_MATCH", CMP_EXC_MATCH, None),
]


# Used by abstractvm.py:
def GetBinaryOperatorMapping():
  return {slot.opcode[len("BINARY_"):]: slot.python_name
          for slot in SLOTS
          if slot.opcode}


def GetCompareFunctionMapping():
  return {index: magic
          for op, index, magic in COMPARE_OPS
          if magic
         }