#!/usr/bin/env python3
# Copyright (C) 2026 sn0wd0wn (gregel, Dantiox, Alexes)
# SPDX-License-Identifier: AGPL-3.0-only
"""Decode Blaze TDF payloads into readable fields.

Takes a hex string, or a server log line with `hex=...`:

    python tools/tdf_decode.py "9a ec e8 00 00 ..."
    grep "comp 0x001C, cmd 0x0002" server.log | head -1 | python tools/tdf_decode.py -
"""

import re
import sys

TYPE_NAMES = {0: "int", 1: "string", 2: "blob", 3: "struct", 4: "list", 5: "map",
              6: "union", 7: "int list", 8: "object type", 9: "object id", 10: "float"}


def read_varint(data, offset):
    byte = data[offset]
    negative = byte & 0x40
    value = byte & 0x3F
    offset += 1
    shift = 6
    while byte & 0x80:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        shift += 7
    return (-value if negative else value), offset


def read_tag(data, offset):
    packed = int.from_bytes(data[offset:offset + 3], "big")
    return "".join(chr(((packed >> (18 - 6 * i)) & 0x3F) + 0x20) for i in range(4)).strip()


def read_value(data, offset, kind):
    if kind == 0:
        return read_varint(data, offset)
    if kind == 1:
        length, offset = read_varint(data, offset)
        return data[offset:offset + length - 1].decode("latin1"), offset + length
    if kind == 2:
        length, offset = read_varint(data, offset)
        return f"<blob {length} bytes>", offset + length
    if kind == 3:
        if data[offset] == 2:
            offset += 1
        return read_struct(data, offset)
    if kind == 4:
        element = data[offset]
        count, offset = read_varint(data, offset + 1)
        items = []
        for _ in range(count):
            item, offset = read_value(data, offset, element)
            items.append(item)
        return items, offset
    if kind == 5:
        key_kind, value_kind = data[offset], data[offset + 1]
        count, offset = read_varint(data, offset + 2)
        items = []
        for _ in range(count):
            key, offset = read_value(data, offset, key_kind)
            value, offset = read_value(data, offset, value_kind)
            items.append((key, value))
        return dict(items), offset
    if kind == 6:
        member = data[offset]
        if member == 0x7F:
            return None, offset + 1
        tag = read_tag(data, offset + 1)
        value, offset = read_value(data, offset + 5, data[offset + 4])
        return {f"union[{member}].{tag}": value}, offset
    if kind == 7:
        count, offset = read_varint(data, offset)
        items = []
        for _ in range(count):
            item, offset = read_varint(data, offset)
            items.append(item)
        return items, offset
    if kind == 8:
        first, offset = read_varint(data, offset)
        second, offset = read_varint(data, offset)
        return (first, second), offset
    if kind == 9:
        first, offset = read_varint(data, offset)
        second, offset = read_varint(data, offset)
        third, offset = read_varint(data, offset)
        return (first, second, third), offset
    if kind == 10:
        return data[offset:offset + 4].hex(), offset + 4
    raise ValueError(f"unknown TDF type {kind} at offset {offset}")


def read_struct(data, offset=0):
    fields = {}
    while offset < len(data) and data[offset] != 0:
        tag = read_tag(data, offset)
        value, offset = read_value(data, offset + 4, data[offset + 3])
        fields[tag] = value
    return fields, offset + 1


def show(value, indent=0):
    pad = "  " * indent
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                print(f"{pad}{key}:")
                show(item, indent + 1)
            else:
                print(f"{pad}{key} = {item}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, (dict, list)):
                print(f"{pad}[{index}]")
                show(item, indent + 1)
            else:
                print(f"{pad}[{index}] = {item}")


def main():
    text = sys.stdin.read() if len(sys.argv) < 2 or sys.argv[1] == "-" else " ".join(sys.argv[1:])
    match = re.search(r"hex=([0-9a-f ]+?)(?: from|$)", text.strip())
    hex_text = match.group(1) if match else text
    data = bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", hex_text))
    fields, used = read_struct(data)
    show(fields)
    print(f"-- decoded {used} of {len(data)} bytes")


if __name__ == "__main__":
    main()
