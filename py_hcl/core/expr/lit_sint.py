from py_hcl.core.expr import HclExpr, ConnDir
from py_hcl.core.type.sint import SIntT
from py_hcl.utils import signed_num_bin_len


class SLiteral(HclExpr):
    def __init__(self, value: int):
        self.value = value

        w = signed_num_bin_len(value)
        self.hcl_type = SIntT(w)
        self.conn_dir = ConnDir.RT
