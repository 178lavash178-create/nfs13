# Server log: three-player speedlist

`speedlist-session-2026-11-03.log` is the unedited server log of a session with
three players (ih8sn0w, Dantiox, Alex) on 3 November 2026, from the start of
the speedlist to its end: the playlist request, the attribute changes for each
of the five events and every game report. Only the IP addresses (replaced with
`10.13.0.x`) and Autolog session tokens were changed. Routine keep-alive lines
were left out.

Useful searches:

```bash
grep -E "getComponent=playlist|setGameAttributes|Generic reply for comp 0x001C" speedlist-session-2026-11-03.log
```
