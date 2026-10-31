# Setup

## Create and connect a tunnel

1. In the [Cloudflare dashboard](https://dash.cloudflare.com/), open Networking → Tunnels (or Cloudflare Zero Trust → Networks → Connectors).
2. Create a Cloudflared tunnel managed by Cloudflare. From the connector installation command, copy only the token following `--token`.
3. Paste it into `tunnel_token` in the add-on Configuration tab. Keep `log_level: info` and `protocol: auto` initially.
4. Start the add-on. Confirm Cloudflare reports the tunnel as healthy.
5. Add a published application route/public hostname, such as `ha.example.com`, pointing to **HTTP** service **`homeassistant:80`**. New HAOS installations since Home Assistant 2026.8 default to port 80; older installations usually retain port 8123. Use the port configured for your installation (for example, `homeassistant:8123` or `homeassistant:8080`). The add-on uses the Supervisor container network; `localhost` refers to the add-on itself.

See Home Assistant's [current port defaults](https://www.home-assistant.io/docs/configuration/remote/). The origin port is configured in Cloudflare, independently of the public HTTPS port.

If Home Assistant uses HTTPS internally, choose HTTPS and configure origin certificate validation for your installation.

Cloudflare's [tunnel setup guide](https://developers.cloudflare.com/tunnel/get-started/) explains dashboard configuration. Treat the tunnel token as a secret: anyone holding it can run a connector. Rotate it in Cloudflare if disclosed, then update the add-on configuration and restart. Backups containing add-on options also contain the token.

## Allow the reverse proxy in Home Assistant

Home Assistant requires explicit proxy trust. On Home Assistant 2026.8 or later, open **Settings → System → Network → HTTP server**, enable **Trust X-Forwarded-For**, and add the connector's IP address to **Trusted proxies**. If requests return `400: Bad Request`, inspect Home Assistant's logs for the reverse proxy warning to find the connecting address.

Alternatively, add `172.30.32.0/23`, the standard Hass.io bridge network, to **Trusted proxies**; verify it matches your installation before trusting it. Trusting this network allows other containers on the bridge to supply forwarded headers. For narrower trust, use the connector's actual address, but verify it after container recreation. Never trust all addresses (`0.0.0.0/0`). Save the HTTP settings, allow Home Assistant to restart, and confirm the settings from your local connection when prompted. See the [Home Assistant HTTP documentation](https://www.home-assistant.io/integrations/http/#reverse-proxies).

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
- **502 from Cloudflare:** verify the origin uses Home Assistant's configured port (`http://homeassistant:80` for a new HAOS installation, often `http://homeassistant:8123` for an older one), Home Assistant is running, and the origin protocol matches its HTTP/TLS configuration. An HTTP origin entered as just `homeassistant` uses port 80. Inspect the add-on log: `no such host` indicates a DNS problem, `connection refused` indicates the destination is not accepting connections at that address and port, and certificate errors indicate an HTTPS validation problem. To check whether the internal hostname is the problem, try the HAOS host's LAN IP with the same port and protocol in the Cloudflare origin URL.
- **400 / untrusted proxy:** enable **Trust X-Forwarded-For** and add the actual connecting proxy address or the Hass.io bridge network (`172.30.32.0/23` on a standard installation) to **Trusted proxies**, then save and confirm the HTTP settings.
- **Login/app issues:** check external URL and any Cloudflare Access policies.

The add-on exposes no host ports and needs no host networking, Docker socket, Supervisor API access or additional privileges. Stop it to disconnect this connector; other replicas of the tunnel may remain active.

For issues, include add-on version, architecture and relevant logs with tokens and personal information removed. Live tunnel connectivity requires your own Cloudflare account and token.
