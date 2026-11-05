# Tools

| Script | What it does |
| --- | --- |
| `tdf_decode.py` | Decodes a Blaze TDF payload (hex, or a server log line with `hex=`) into readable fields |
| `session_summary.py` | Turns a server log into a Markdown table of every session |
| `sanitize_log.py` | Replaces IP addresses and session tokens so a log can be shared |

```bash
python tools/sanitize_log.py server.log --server-ip 192.168.1.50 > shared.log
python tools/session_summary.py shared.log
grep "comp 0x001C, cmd 0x0002" shared.log | head -1 | python tools/tdf_decode.py -
```
