# -*- coding: utf-8 -*-
import binascii
import os
import shutil
import struct
import json
from pathlib import Path

src_path = Path(os.path.dirname(os.path.realpath(__file__)))
root_path = src_path.parent.absolute()
input_path = os.path.join(root_path, "inputs")
output_path = os.path.join(root_path, "outputs")
output_json_path = os.path.join(output_path, "output.json")


def find_cur_dir() -> str:
    return os.getcwd()


def make_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def enumerate_files(path: str) -> tuple[list, list]:
    output_filepaths = []
    output_filenames = []
    for root, folder, filenames in os.walk(path):
        for filename in filenames:
            output_filepaths.append(os.path.join(root, filename))
            output_filenames.append(filename)
    return output_filepaths, output_filenames


def remove_dir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def init() -> None:
    remove_dir(output_path)
    for path in [input_path, output_path]:
        make_dir(path)


def copy_file(src: str, dst: str) -> None:
    if os.path.exists(dst):
        os.remove(dst)
    if not os.path.exists(src):
        return
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copy(src, dst)


def open_as_hex(filepath: str) -> str:
    with open(filepath, "rb") as f:
        hex_data = binascii.hexlify(f.read()).decode("ascii")
    return hex_data


def save_hex(filepath: str, hex_data: str) -> None:
    with open(filepath, "wb") as f:
        f.write(binascii.unhexlify(hex_data))


def str2hex(input_str: str) -> str:
    output = ""
    for char in input_str:
        output += struct.pack('<s', bytes(char, "utf-8")).hex()
    return output


def int2hex(input_int: int, hex_len: int) -> str:
    if hex_len == 1:
        hex_data = struct.pack('<b', input_int).hex()
    elif hex_len == 2:
        hex_data = struct.pack('<h', input_int).hex()
    elif hex_len == 4:
        hex_data = struct.pack('<i', input_int).hex()
    elif hex_len == 8:
        hex_data = struct.pack('<q', input_int).hex()
    else:
        hex_data = ""
    return hex_data


def float2hex(input_float: float) -> str:
    hex_data = struct.pack('<f', input_float).hex()
    return hex_data


def hex2int(input_hex: str) -> int:
    hex_data = bytearray.fromhex(input_hex)
    if len(hex_data) == 4:
        output = struct.unpack('<l', hex_data)[0]
    elif len(hex_data) == 2:
        output = struct.unpack('<h', hex_data)[0]
    else:
        output = 0
    return output


def hex2float(input_hex: str) -> float:
    hex_data = bytearray.fromhex(input_hex)
    output = struct.unpack('<f', hex_data)[0]
    return output

def write_json(fumen_data_list):
    with open(output_json_path, "wb") as f:
        f.write(json.dumps({"items": fumen_data_list}, sort_keys=False, indent="\t", ensure_ascii=False).encode("utf-8"))