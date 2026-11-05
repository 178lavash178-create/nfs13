# Contributing

Thanks for helping. A few rules keep this project clean and safe for everyone.

## Never submit

* Game files: executables (patched or not), assets, data, audio, video.
* EA source code, SDK code, or code decompiled from the game.
* Memory dumps, packet captures or logs that contain other people's data,
  real IP addresses, tokens or passwords. Use `tools/sanitize_log.py` first.
* Cracks, keys, or anything that helps run the game without a licence.

Pull requests or issues containing any of this will be closed and the content
removed.

## Do submit

* Your own code and documentation.
* Protocol findings described in your own words (field names, message layout,
  addresses where the game reads something).
* Sanitized logs from your own sessions.

## Licence and sign-off

All contributions are accepted under the
[GNU Affero General Public License v3.0](LICENSE). By submitting a contribution
you confirm that you wrote it yourself (or have the right to submit it) and
agree to license it under the AGPL-3.0. Please add a sign-off line to your
commits (`git commit -s`), as in the
[Developer Certificate of Origin](https://developercertificate.org/).

## Before a pull request

```bash
cd server && python3 -m unittest -v test_server
```

Please read [DISCLAIMER.md](DISCLAIMER.md) before contributing.
