# Setup

## Create and connect a tunnel

1. In the [Cloudflare dashboard](https://dash.cloudflare.com/), open Networking → Tunnels (or Cloudflare Zero Trust → Networks → Connectors).
2. Create a Cloudflared tunnel managed by Cloudflare. From the connector installation command, copy only the token following `--token`.
3. Paste it into `tunnel_token` in the add-on Configuration tab. Keep `log_level: info` and `protocol: auto` initially.
4. Start the add-on. Confirm Cloudflare reports the tunnel as healthy.
5. Add a published application route/public hostname, such as `ha.example.com`, pointing to **HTTP** service **`homeassistant:8123`**. The add-on uses the Supervisor container network; `localhost` refers to the add-on itself.

If Home Assistant uses HTTPS internally, choose HTTPS and configure origin certificate validation for your installation.

Cloudflare's [tunnel setup guide](https://developers.cloudflare.com/tunnel/get-started/) explains dashboard configuration. Treat the tunnel token as a secret: anyone holding it can run a connector. Rotate it in Cloudflare if disclosed, then update the add-on configuration and restart. Backups containing add-on options also contain the token.

## Allow the reverse proxy in Home Assistant

Home Assistant requires explicit proxy trust. Merge the following into its existing `configuration.yaml` `http:` section:

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.30.33.0/24
```

This is the standard Supervisor add-on subnet; verify it matches your installation. Trusting this subnet allows other add-ons on that subnet to supply forwarded headers. For narrower trust, use the connector's actual address, but verify it after container recreation. Never trust all addresses (`0.0.0.0/0`). Validate the configuration and restart Home Assistant before opening the public hostname. See the [Home Assistant HTTP documentation](https://www.home-assistant.io/integrations/http/#reverse-proxies).

Set your external Home Assistant URL to the public HTTPS hostname in Home Assistant's network settings if needed. Keep Home Assistant authentication enabled. Cloudflare Access policies are optional; test companion app and webhook compatibility when enabling them.

## Options

| Option | Default | Purpose |
| --- | --- | --- |
| `tunnel_token` | Empty (required) | Remotely managed tunnel connector token, not an API token. |
| `log_level` | `info` | `debug`, `info`, `warn`, `error`, or `fatal`. Debug may log sensitive request details. |
| `protocol` | `auto` | `auto`, `quic`, or `http2`. Use HTTP/2 if outbound UDP is blocked. |

Routes and origin settings are managed in Cloudflare. Local tunnel credentials files and quick tunnels are not supported. Updates to cloudflared are delivered through add-on updates; its self-updater is disabled.

## Troubleshooting

- **Missing token:** paste only the token, with no spaces or line breaks, save and restart.
- **Tunnel disconnected:** check the token, DNS and outbound connectivity. Cloudflare Tunnel requires outbound port 7844 (UDP for QUIC or TCP for HTTP/2). Try `protocol: http2` where UDP is blocked.
- **502 from Cloudflare:** verify the service is `http://homeassistant:8123`, Home Assistant is running, and the origin protocol matches its HTTP/TLS configuration.
- **400 / untrusted proxy:** inspect Home Assistant logs and trust the actual connecting proxy address or the correct Supervisor add-on subnet, then restart Home Assistant.
- **Login/app issues:** check external URL and any Cloudflare Access policies.

The add-on exposes no host ports and needs no host networking, Docker socket, Supervisor API access or additional privileges. Stop it to disconnect this connector; other replicas of the tunnel may remain active.

For issues, include add-on version, architecture and relevant logs with tokens and personal information removed. Live tunnel connectivity requires your own Cloudflare account and token.
