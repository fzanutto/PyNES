

from instructions.base_instructions import Transfer


class Txs(Transfer):
    identifier_byte = bytes([0x9A])
    fromRegister = "X"
    toRegister = "S"
