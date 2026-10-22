# Contributing

`cloudflared/` contains the Home Assistant manifest, Dockerfile, startup script, translations and user documentation. The image copies the official cloudflared binary into Alpine and uses Docker init with an exec-based entrypoint.

Run local checks:

```sh
sh -n cloudflared/rootfs/usr/local/bin/run-cloudflared
python3 -m unittest discover -s tools -p 'test_*.py'
docker build -t ha-cloudflared:test cloudflared
docker run --rm --entrypoint cloudflared ha-cloudflared:test --version
```

CI checks configuration/startup behavior and builds both supported architectures. Before releasing, test installation, tunnel connection, proxy configuration, restart and shutdown on Home Assistant OS. Never commit real tunnel tokens.

For releases, bump `cloudflared/config.json`, the Dockerfile's default `BUILD_VERSION`, and the changelog. Update the pinned upstream cloudflared image separately. Home Assistant detects updates from the manifest version when the repository refreshes.
