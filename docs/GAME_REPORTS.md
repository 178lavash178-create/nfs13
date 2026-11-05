# Game reports, decoded

After every event, and from time to time in free roam, each game sends a
game report (`submitGameReport`, Blaze component `0x1C`, command `2`).
These are real reports from our sessions, taken from
[logs/server-events-2026-11-01_05.log](../logs/server-events-2026-11-01_05.log)
and decoded with:

```bash
grep "comp 0x001C, cmd 0x0002" logs/server-events-2026-11-01_05.log | head -1 | python tools/tdf_decode.py -
```

`EVID` is the event, `NUMP` the number of players, `SCOR` the score, `XP` the
player's online XP, `TKDS`/`WRCK` takedowns and wrecks, `DDRV` distance driven
and `PLYT` play time. The server stores license plates from `license_plate`
reports; the rest is accepted but not processed yet (see `ResultNotification`
in [HOW_IT_WORKS.md](HOW_IT_WORKS.md)).

## OnlineEventChallenge

Sent by the game at 2026-11-03 20:31:29,189 UTC from 10.13.0.3.

```
FNSH = 0
PRVT = []
RPRT:
  GAME:
    LICN:
      1000001 = {}
    RSLT:
      1000001:
        EVID = 1430729
        NUMP = 3
        SCOR = 125516
        VALD = 1
    STAT:
      1000001:
        ASST = 0
        DDRV = 3172
        PLYT = 136
        SCOR = 3000
        SUCD = 1
        TKDS = 0
        TKDW = 0
        WRCK = 3
        WRKS = 3
        XP = 29215
GRID = 0
GTYP = OnlineEventChallenge
-- decoded 175 of 175 bytes
```

## OnlineEventFreedrive

Sent by the game at 2026-11-02 21:06:10,593 UTC from 10.13.0.4.

```
FNSH = 0
PRVT = []
RPRT:
  GAME:
    LICN:
      1 = {}
    RSLT:
      1:
        EVID = 1113775
        NUMP = 2
        SCOR = 0
        VALD = 1
    STAT:
      1:
        ASST = 0
        DDRV = 1953
        PLYT = 185
        SCOR = 0
        SUCD = 0
        TKDS = 0
        TKDW = 0
        WRCK = 0
        WRKS = 0
        XP = 26715
GRID = 0
GTYP = OnlineEventFreedrive
-- decoded 166 of 166 bytes
```

## license_plate

Sent by the game at 2026-11-01 19:57:42,568 UTC from 10.13.0.3.

```
FNSH = 0
PRVT = []
RPRT:
  GAME:
    PLAT:
      1000001:
        ID = 2284727
        TAG = NEED4SPD
GRID = 0
GTYP = license_plate
-- decoded 88 of 88 bytes
```

## onlinemilestone

Sent by the game at 2026-11-02 21:06:10,585 UTC from 10.13.0.4.

```
FNSH = 0
PRVT = []
RPRT:
  GAME:
    MILE:
      1:
        REPS:
          1512596:
            CNT = 1670
          1512640:
            CNT = 1670
          1518653:
            CNT = 260
          1518697:
            CNT = 260
          1610985:
            CNT = 260
          2242712:
            CNT = 10
          2242733:
            CNT = 10
          2268082:
            CNT = 130
          2268292:
            CNT = 390
GRID = 0
GTYP = onlinemilestone
-- decoded 170 of 170 bytes
```

