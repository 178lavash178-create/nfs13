#!/usr/bin/env python3
# Copyright (C) 2026 sn0wd0wn (gregel, Dantiox, Alexes)
# SPDX-License-Identifier: AGPL-3.0-only
"""Summarise the sessions in a server log as a Markdown table.

    python tools/session_summary.py logs/server-events-2026-11-01_05.log

For each game: when it started and ended, host, everyone who joined, the
largest number of players at once, speedlist requests, speedlist events played
(from the host's `current_event` attribute) and game reports by type.
"""

import collections
import re
import sys
from datetime import datetime

STAMP = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)")
EVENT_ATTR = re.compile(
    r"63 75 72 72 65 6e 74 5f 65 76 65 6e 74 00 [0-9a-f]{2} ((?:3[0-9] )+)00")
FREEROAM_EVENT = "1113775"


def report_type(line):
    match = re.search(r"hex=([0-9a-f ]+?) from", line)
    if not match:
        return None
    data = bytes.fromhex(match.group(1).replace(" ", ""))
    index = data.find(bytes.fromhex("9f4e70"))  # GTYP string
    if index < 0:
        return None
    return data[index + 5:index + 4 + data[index + 4]].decode("latin1")


def main():
    sessions = []
    open_games = {}
    current = None
    for line in open(sys.argv[1], errors="replace"):
        stamp = STAMP.match(line)
        if not stamp:
            continue
        when = datetime.strptime(stamp.group(1), "%Y-%m-%d %H:%M:%S")
        if "listening on" in line and "Blaze server" in line:
            for game in open_games.values():
                game["end"] = game["end"] or when
            open_games.clear()
            continue
        created = re.search(r"Created game gid=(\d+) host=([^/]+)/", line)
        if created:
            game = {"gid": created.group(1), "start": when, "end": None,
                    "host": created.group(2), "players": [created.group(2)], "max": 1,
                    "playlists": 0, "events": [], "reports": collections.Counter(),
                    "migrations": 0}
            sessions.append(game)
            open_games[game["gid"]] = game
            current = game
            continue
        joined = re.search(r"Joined game gid=(\d+) player=([^/]+)/\d+ slot=\d+ count=(\d+)", line)
        if joined and joined.group(1) in open_games:
            game = open_games[joined.group(1)]
            if joined.group(2) not in game["players"]:
                game["players"].append(joined.group(2))
            game["max"] = max(game["max"], int(joined.group(3)))
            continue
        removed = re.search(r"Removed empty game gid=(\d+)", line)
        if removed and removed.group(1) in open_games:
            open_games.pop(removed.group(1))["end"] = when
            continue
        if current is None or current["end"] is not None:
            continue
        if "Migrated game" in line:
            current["migrations"] += 1
        elif "getComponent=playlist" in line:
            current["playlists"] += 1
        elif "setGameAttributes cmd" in line:
            value = EVENT_ATTR.search(line)
            if value:
                event = bytes.fromhex(value.group(1).replace(" ", "")).decode()
                if event not in ("0", FREEROAM_EVENT) and event not in current["events"]:
                    current["events"].append(event)
        elif "comp 0x001C, cmd 0x0002" in line:
            kind = report_type(line)
            if kind:
                current["reports"][kind] += 1

    print("| Start (UTC) | Length | Host | Players | Max at once | Speedlist requests | Speedlist events played | Game reports |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for game in sessions:
        length = ""
        if game["end"]:
            minutes = int((game["end"] - game["start"]).total_seconds() // 60)
            length = f"{minutes} min"
        reports = ", ".join(f"{kind} {count}" for kind, count in game["reports"].most_common())
        print(f"| {game['start']:%Y-%m-%d %H:%M} | {length} | {game['host']} | "
              f"{', '.join(game['players'])} | {game['max']} | {game['playlists'] or ''} | "
              f"{len(game['events']) or ''} | {reports} |")

    played = [game for game in sessions if game["max"] >= 2]
    minutes = sum(int((g["end"] - g["start"]).total_seconds() // 60) for g in played if g["end"])
    print()
    print(f"Sessions: {len(sessions)}, with two or more players: {len(played)}, "
          f"with three: {sum(1 for g in sessions if g['max'] >= 3)}, "
          f"multiplayer time: {minutes // 60} h {minutes % 60} min, "
          f"speedlist events played: {sum(len(g['events']) for g in sessions)}, "
          f"game reports: {sum(sum(g['reports'].values()) for g in sessions)}.")


if __name__ == "__main__":
    main()
