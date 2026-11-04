# Server logs

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

## 4 November 2026: random speedlist

`session-2026-11-04.log` is the session shown in the
[gameplay video](https://www.youtube.com/watch?v=gprfBzVMjnw): Dantiox hosts,
ih8sn0w and Alex join, and the server hands out a random speedlist
(`GetNextPlaylist`, events such as 1463179 and 1552840). Same edits as above:
addresses and session tokens replaced, keep-alive lines left out.
