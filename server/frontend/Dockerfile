# Copyright (C) 2026 sn0wd0wn (gregel, Dantiox, Alexes)
# SPDX-License-Identifier: AGPL-3.0-only
FROM alpine:3.20
RUN apk add --no-cache build-base perl linux-headers curl
WORKDIR /src
RUN curl -fsSL -o openssl.tgz https://github.com/openssl/openssl/releases/download/OpenSSL_1_1_1w/openssl-1.1.1w.tar.gz \
 && echo "cf3098950cb4d853ad95c0841f1f9c6d3dc102dccfcacd521d93925208b76ac8  openssl.tgz" | sha256sum -c - \
 && tar xzf openssl.tgz && cd openssl-1.1.1w \
 && ./Configure linux-x86_64 --prefix=/opt/ossl --openssldir=/opt/ossl enable-ssl3 enable-ssl3-method enable-weak-ssl-ciphers no-shared no-tests no-async \
 && make -j3 >/dev/null && make install_sw >/dev/null
RUN curl -fsSL -o stunnel.tgz https://deb.debian.org/debian/pool/main/s/stunnel4/stunnel4_5.74.orig.tar.gz \
 && tar xzf stunnel.tgz && cd stunnel-5.74 \
 && ./configure --with-ssl=/opt/ossl --disable-shared --enable-static --disable-systemd --disable-libwrap --disable-fips LDFLAGS="-static" >/dev/null \
 && make -j3 LDFLAGS="-all-static" >/dev/null && make install >/dev/null
RUN mkdir /out && cp /opt/ossl/bin/openssl /out/openssl-ssl3 && find /usr/local/bin -name "stunnel" -exec cp {} /out/stunnel-ssl3 \; && strip /out/*
