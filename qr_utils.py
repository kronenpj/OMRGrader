#!/usr/bin/env python3
import inspect
import logging
from random import choice

logging.basicConfig()
global_log = logging.getLogger(__package__)
log = global_log.getChild(__name__.replace(f"{__package__}.", ""))
log.setLevel(global_log.getEffectiveLevel())

"""
Routine to pack and unpack the answers 

Author: Paul Kronenwetter <n2kiq0@gmail.com>
Supports QR code generation and decoding answers for randomly generated exams. 
"""


def pack_string(answers: str) -> bytearray:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    temp = 0
    bits = 0
    b_array = bytearray()
    for character in list(answers):
        # Shift in the bits here so unpacking is done in order.
        if character == "A":
            temp = temp + (0 << bits)
        if character == "B":
            temp = temp + (1 << bits)
        if character == "C":
            temp = temp + (2 << bits)
        if character == "D":
            temp = temp + (3 << bits)
        bits = bits + 2
        if bits >= 8:
            b_array.append(temp)
            bits = 0
            temp = 0
    return b_array


def unpack_bytearray(byte_array: bytearray) -> str:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    ret_str = ""
    for byte in byte_array:
        shift = byte
        for _ in [0, 1, 2, 3]:
            temp = shift & 0x03
            if temp == 0:
                ret_str = ret_str + "A"
            if temp == 1:
                ret_str = ret_str + "B"
            if temp == 2:
                ret_str = ret_str + "C"
            if temp == 3:
                ret_str = ret_str + "D"
            shift = shift >> 2
    return ret_str


def main():
    from_str = "ABCD"
    source_string = ""
    for _ in range(0, 60):
        source_string = source_string + choice(from_str)
    b_array = pack_string(source_string)
    unpacked_string = unpack_bytearray(b_array)

    print("Compare:")
    print(f"{source_string}")
    print(f"{unpacked_string}")
    assert source_string == unpacked_string


# Main
if __name__ == "__main__":
    main()
