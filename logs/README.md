# Logs

Real logs from our server and the host PC, 1–5 November 2026. Unedited except
for IP addresses (replaced with `10.13.x.x`, numbered separately in each file)
and Autolog session tokens. Routine keep-alive lines were left out of the
full session logs.

| File | What it is |
| --- | --- |
| `server-events-2026-11-01_05.log` | Every session event of five days: games, joins, host changes, speedlist requests, attribute changes, game reports. Source of [docs/SESSIONS.md](../docs/SESSIONS.md) |
| `first-three-player-session-2026-11-02.log` | The first session with three players (2 November, 21:02–21:33 UTC), full log |
| `speedlist-session-2026-11-03.log` | A full five-event speedlist with three players (ih8sn0w, Dantiox, Alex) |
| `session-2026-11-04.log` | The session in the [gameplay video](https://www.youtube.com/watch?v=gprfBzVMjnw): random speedlist, events 1463179 and 1552840 |
| `client/` | Excerpts of the host PC's `nfs13_trace.log` from [client/trace_hook](../client/trace_hook): mesh setup, the speedlist rejected and then accepted, the game's event table |

Useful searches:

```bash
grep -E "Created game|Joined game|Migrated" server-events-2026-11-01_05.log
grep -E "getComponent=playlist|setGameAttributes" speedlist-session-2026-11-03.log
```
