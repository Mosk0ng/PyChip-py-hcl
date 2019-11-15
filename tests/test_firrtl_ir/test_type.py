from py_hcl.firrtl_ir.field import Field
from py_hcl.firrtl_ir.tpe import UnknownType, ClockType, \
    UIntType, SIntType, VectorType, BundleType
from py_hcl.firrtl_ir.width import IntWidth, UnknownWidth
from .utils import serialize_equal


def test_unknown_type():
    serialize_equal(UnknownType(), "?")


def test_clock_type():
    serialize_equal(ClockType(), "Clock")


def test_uint_type():
    serialize_equal(UIntType(UnknownWidth()), "UInt")
    serialize_equal(UIntType(IntWidth(8)), "UInt<8>")
    serialize_equal(UIntType(IntWidth(32)), "UInt<32>")


def test_sint_type():
    serialize_equal(SIntType(UnknownWidth()), "SInt")
    serialize_equal(SIntType(IntWidth(8)), "SInt<8>")
    serialize_equal(SIntType(IntWidth(32)), "SInt<32>")


def test_vector_type():
    vt = VectorType(UIntType(UnknownWidth()), 16)
    serialize_equal(vt, "UInt[16]")

    vt = VectorType(SIntType(IntWidth(8)), 16)
    serialize_equal(vt, "SInt<8>[16]")

    vt = VectorType(UIntType(IntWidth(8)), 16)
    serialize_equal(vt, "UInt<8>[16]")

    vt = VectorType(vt, 32)
    serialize_equal(vt, "UInt<8>[16][32]")

    vt = VectorType(VectorType(VectorType(vt, 42), 7), 9)
    serialize_equal(vt, "UInt<8>[16][32][42][7][9]")


def test_bundle_type():
    bd = BundleType([
        Field("a", UIntType(IntWidth(8))),
        Field("b", UIntType(IntWidth(8))),
        Field("c", UIntType(IntWidth(8)), True),
    ])
    serialize_equal(bd, "{a : UInt<8>, b : UInt<8>, flip c : UInt<8>}")

    vt = VectorType(UIntType(IntWidth(8)), 16)
    bd = BundleType([
        Field("a", vt),
        Field("b", UIntType(IntWidth(8)), True),
        Field("c", VectorType(vt, 32)),
    ])
    serialize_equal(
        bd, "{a : UInt<8>[16], flip b : UInt<8>, c : UInt<8>[16][32]}"
    )

    # TODO: Is it valid?
    bd = BundleType([
        Field("l1", BundleType([
            Field("l2", BundleType([
                Field("l3", UIntType(IntWidth(8)), True)
            ])),
            Field("vt", vt),
        ]))
    ])
    serialize_equal(bd, "{l1 : {l2 : {flip l3 : UInt<8>}, vt : UInt<8>[16]}}")
