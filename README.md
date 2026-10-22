# Cloudflare Tunnel for Home Assistant

A community Home Assistant add-on that runs `cloudflared` to connect to a remotely managed Cloudflare Tunnel. Supports **amd64** and **aarch64**, with no inbound port forwarding and Protection mode enabled.

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Faffeldt28%2Fha-addons-cloudflare)
[![Validate](https://github.com/affeldt28/ha-addons-cloudflare/actions/workflows/validate.yml/badge.svg)](https://github.com/affeldt28/ha-addons-cloudflare/actions/workflows/validate.yml)

Requires Home Assistant with Supervisor (such as Home Assistant OS), a Cloudflare account and a domain configured with Cloudflare for a public hostname. Home Assistant Container does not support add-ons.

1. Add `https://github.com/affeldt28/ha-addons-cloudflare` to your Home Assistant add-on repositories.
2. Install **Cloudflare Tunnel**.
3. Create a remotely managed Cloudflare Tunnel and paste its connector token into the add-on's `tunnel_token` option.
4. Follow the [setup documentation](cloudflared/DOCS.md) to configure your hostname and Home Assistant's trusted proxy settings.
5. Start the add-on and check the logs and tunnel status in Cloudflare. Enable Start on boot after confirming it works.

```yaml
tunnel_token: "your-tunnel-token"
log_level: info
protocol: auto
```

Hostname routing is managed in Cloudflare. This add-on does not create tunnels or DNS records and does not require a Cloudflare API key.

See [documentation and troubleshooting](cloudflared/DOCS.md), [changes](cloudflared/CHANGELOG.md) and [contributing](CONTRIBUTING.md). This is an independent community project, unaffiliated with Cloudflare or Home Assistant. Initial release is experimental pending validation on Home Assistant OS.
