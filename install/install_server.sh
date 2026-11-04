#!/usr/bin/env bash
# Install the nfs13 server for the current user on a Linux host.
#
#   ./install/install_server.sh 192.168.1.50
#
# The argument is the address the game clients use to reach this machine
# (its LAN or VPN IP). Requires python3 >= 3.10, openssl and either docker
# (to build the SSLv3 stunnel) or a prebuilt binary in $STUNNEL_SSL3.
set -euo pipefail

HOST_IP="${1:?usage: install_server.sh <server-ip>}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${NFS13_DIR:-$HOME/nfs13-server}"
UNITS="$HOME/.config/systemd/user"

mkdir -p "$DEST/certs" "$DEST/frontend" "$UNITS"
install -m 644 "$REPO/server/server.py" "$DEST/server.py"

if [ -n "${STUNNEL_SSL3:-}" ]; then
    install -m 755 "$STUNNEL_SSL3" "$DEST/frontend/stunnel-ssl3"
elif [ ! -x "$DEST/frontend/stunnel-ssl3" ]; then
    # The game speaks SSLv3 only, which current distributions no longer ship.
    docker build -t nfs13-stunnel-ssl3 "$REPO/server/frontend"
    container="$(docker create nfs13-stunnel-ssl3)"
    docker cp "$container:/out/stunnel-ssl3" "$DEST/frontend/stunnel-ssl3"
    docker rm "$container" >/dev/null
fi

if [ ! -f "$DEST/certs/cert.pem" ]; then
    # Same shape as the certificate used in testing: self-signed, SHA-1, RSA 2048.
    openssl req -x509 -newkey rsa:2048 -sha1 -nodes -days 3650 \
        -subj "/CN=*.ea.com" \
        -keyout "$DEST/certs/key.pem" -out "$DEST/certs/cert.pem"
fi

sed "s#@DEST@#$DEST#g" "$REPO/server/frontend/stunnel.conf.in" > "$DEST/frontend/stunnel.conf"

cat > "$UNITS/nfs13-server.service" <<EOF
[Unit]
Description=NFS Most Wanted 2012 private server
After=network-online.target

[Service]
WorkingDirectory=$DEST
Environment=NFS13_HOST=$HOST_IP
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/env python3 $DEST/server.py
Restart=on-failure

[Install]
WantedBy=default.target
EOF

cat > "$UNITS/nfs13-frontend.service" <<EOF
[Unit]
Description=SSLv3 frontend for the NFS13 server
After=nfs13-server.service

[Service]
WorkingDirectory=$DEST
ExecStart=$DEST/frontend/stunnel-ssl3 $DEST/frontend/stunnel.conf
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now nfs13-server.service nfs13-frontend.service
loginctl enable-linger "$USER" 2>/dev/null || true

cat <<EOF

Server installed in $DEST and started.
Open TCP 42127, 44125, 8080, 17500 and UDP 17500 on this machine.
Players point these names at $HOST_IP (hosts file or local DNS):
$(sed 's/^/  /' "$REPO/client/hosts.txt")

Live log:  journalctl --user -u nfs13-server.service -f -o cat
EOF
