# Cloudflare Tunnel

Reach your Home Assistant instance through your own Cloudflare hostname. Connect to a remotely managed tunnel using the official cloudflared client, with no inbound port forwarding and Protection mode enabled.

## What it provides

- **Tunnel connection:** authenticate with your Cloudflare connector token.
- **Cloudflare-managed routing:** configure public hostnames and origin settings in Cloudflare.
- **Transport options:** use automatic selection, QUIC or HTTP/2.
- **Home Assistant updates:** receive cloudflared updates through the add-on's update flow.

## How it connects

The connector opens an **outbound connection to Cloudflare**. No inbound host port, Docker socket access or disabled Protection mode is needed. Manage your tunnel and routes in Cloudflare; this add-on does not provide a separate dashboard inside Home Assistant.

## Get started

1. In Cloudflare, create a remotely managed tunnel and copy its connector token.
2. In this add-on's **Configuration** tab, enter `tunnel_token`. Leave `log_level` on **info** and `protocol` on **auto** initially.
3. Follow the **Documentation** tab to configure your hostname and Home Assistant's trusted proxy settings.
4. Keep **Protection mode enabled**, start the add-on, and confirm that Cloudflare reports a healthy tunnel.

You need Home Assistant with Supervisor, a supported 64-bit host (amd64 or aarch64), a Cloudflare account and a domain configured with Cloudflare for your public hostname.

## Configuration and access

Routes and origin settings are managed in Cloudflare. The add-on does not create tunnels or DNS records, and does not require a Cloudflare API key. Local tunnel credentials files and quick tunnels are not supported.

Keep Home Assistant authentication enabled. Treat the connector token as a secret; backups containing add-on options also contain it. Use Home Assistant for updates, since cloudflared's self-updater is disabled.

[Setup, options and troubleshooting](https://github.com/affeldt28/ha-addons-cloudflare/blob/main/cloudflared/DOCS.md) · [Cloudflare documentation](https://developers.cloudflare.com/tunnel/get-started/) · [Report an issue](https://github.com/affeldt28/ha-addons-cloudflare/issues)

Independent community add-on, unaffiliated with Cloudflare or Home Assistant.
