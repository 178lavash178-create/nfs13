#!/usr/bin/env python3
# Copyright (C) 2026 sn0wd0wn (gregel, Dantiox, Alexes)
# SPDX-License-Identifier: AGPL-3.0-only
"""Make a server log safe to share: replace IP addresses and session tokens.

Every distinct private or public IPv4 address gets a stable 10.13.x.y stand-in,
in the order it first appears (the server's own NFS13_HOST becomes 10.13.0.1
if given). Raw big-endian copies of those addresses inside hex dumps are
replaced too.

    python tools/sanitize_log.py server.log --server-ip 192.168.1.50 > shared.log
"""

import argparse
import ipaddress
import re
import sys

IP_RE = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
KEEP = {"127.0.0.1", "0.0.0.0"}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("log", type=argparse.FileType("r", errors="replace"))
    parser.add_argument("--server-ip", help="the server's NFS13_HOST address")
    args = parser.parse_args()

    mapping = {}
    if args.server_ip:
        mapping[args.server_ip] = "10.13.0.1"

    def stand_in(match):
        address = match.group(0)
        if address in KEEP:
            return address
        try:
            ipaddress.IPv4Address(address)
        except ValueError:
            return address
        if address not in mapping:
            index = len(mapping) + (1 if args.server_ip else 2)
            mapping[address] = f"10.13.{index // 250}.{index % 250}"
        return mapping[address]

    text = IP_RE.sub(stand_in, args.log.read())
    text = re.sub(r"session=[^&\s]+", "session=REDACTED", text)
    text = re.sub(r"\b(SKEY|PCTK|session_key)([=: ]+)[0-9A-Za-z-]{16,}", r"\1\2REDACTED", text)
    for original, replacement in mapping.items():
        old = " ".join(f"{part:02x}" for part in ipaddress.IPv4Address(original).packed)
        new = " ".join(f"{part:02x}" for part in ipaddress.IPv4Address(replacement).packed)
        text = text.replace(old, new)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
