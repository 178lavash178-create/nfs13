# Security

## Know the risks before you run it

* **SSLv3.** The game only speaks SSLv3, which is broken. Traffic between the
  game and the server must be treated as unencrypted.
* **No certificate check.** The client patch turns off the game's server
  certificate check. A patched game will talk to whatever server its DNS or
  hosts file points to.
* **No authentication.** The server identifies players by IP address only.
  There are no passwords and no accounts. Anyone who can reach the server can
  join and rename themselves.
* **Old protocol code.** The server parses binary messages from the game. It
  has tests, but it has not been audited.

## Recommendations

* Run the server only on a private LAN or a VPN (for example WireGuard) with
  people you trust. Do not expose its ports to the internet.
* Run it as an unprivileged user (the installer uses systemd user services).
* Never enter a real EA, Origin or any other password anywhere related to this
  project. Nothing here needs one.
* Keep the patched game executable separate from your original one.

## Reporting a vulnerability

Please do not post exploit details publicly. Open a GitHub security advisory
in this repository ("Security" tab → "Report a vulnerability"), or an issue
that only says you have a security report, and we will get in touch.

This project comes without any warranty; see [DISCLAIMER.md](DISCLAIMER.md).
