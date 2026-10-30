<p align="center">
  <img src="cloudflared/logo.png" alt="Cloudflare" width="420">
</p>

# Cloudflare Tunnel Community Add-on for Home Assistant

Connect Home Assistant to a remotely managed **Cloudflare Tunnel**. Reach your instance through a public hostname, with an outbound connection, no inbound port forwarding and Protection mode enabled.

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Faffeldt28%2Fha-addons-cloudflare)

[![Validate Cloudflare Tunnel](https://github.com/affeldt28/ha-addons-cloudflare/actions/workflows/pipeline.yml/badge.svg?branch=main)](https://github.com/affeldt28/ha-addons-cloudflare/actions/workflows/pipeline.yml)
![Stage: experimental](https://img.shields.io/badge/stage-experimental-orange)
![Architectures: amd64 and aarch64](https://img.shields.io/badge/architectures-amd64%20%7C%20aarch64-blue)
[![GitHub stars](https://img.shields.io/github/stars/affeldt28/ha-addons-cloudflare?style=flat)](https://github.com/affeldt28/ha-addons-cloudflare/stargazers)

Independent community package for Cloudflare Tunnel. This add-on is experimental; report issues with your host architecture, add-on version and relevant logs.

## About the add-on

- **Official cloudflared binary:** connects using your tunnel's connector token.
- **Outbound connection:** no inbound router port forwarding or exposed host ports.
- **Cloudflare-managed routing:** configure hostnames and origin settings in Cloudflare.
- **Protection mode enabled:** no Docker socket, host networking or Supervisor API access required.

The add-on connects to an existing remotely managed tunnel. It does not create tunnels or DNS records and does not require a Cloudflare API key. See the [setup documentation](cloudflared/DOCS.md) and [changelog](cloudflared/CHANGELOG.md) for details.

## Installation

### Requirements

- Home Assistant with **Supervisor and an add-on/app store**, such as Home Assistant OS.
- An **amd64** or **aarch64** host.
- A **Cloudflare account** and a remotely managed tunnel.
- A domain configured with Cloudflare for your public hostname.

Home Assistant Container installations do not provide the add-on store.

### Add the repository

Click the **Add to Home Assistant** button above and confirm the repository URL in your Home Assistant instance.

To add it manually, open the add-on/app store's **⋮ → Repositories** menu and add:

```text
https://github.com/affeldt28/ha-addons-cloudflare
```

### Connect a tunnel

1. Install **Cloudflare Tunnel**.
2. In Cloudflare, create a remotely managed tunnel and copy its connector token.
3. In the add-on's **Configuration** tab, enter the token as `tunnel_token`. Keep `log_level: info` and `protocol: auto` initially.
4. Follow the [setup documentation](cloudflared/DOCS.md) to configure your public hostname and Home Assistant's trusted proxy settings.
5. Keep **Protection mode enabled**, start the add-on, and check its logs and the tunnel status in Cloudflare. Enable **Start on boot** after confirming the connection.

## Configuration example

Use the connector token generated for your own Cloudflare Tunnel:

```yaml
tunnel_token: "your-tunnel-token"
log_level: info
protocol: auto
```

Hostname routing is managed in Cloudflare. Available transports are `auto`, `quic` and `http2`. See the add-on's **Documentation** tab for options, reverse proxy configuration and troubleshooting. Keep Home Assistant authentication enabled and treat the connector token as a secret.

## Updates

Home Assistant checks the repository for newer add-on versions. Use the store's **Check for updates** action to refresh manually, then press **Update** on the add-on page. Enable **Auto update** there for automatic installation; **Start on boot** does not enable updates.

Renovate updates the pinned cloudflared and Alpine images. Package versions use `<cloudflared version>-<packaging revision>` (for example `2026.10.6-1`). Upstream updates reset the revision to `1`; Alpine updates and packaging changes increment only that suffix. Non-major updates and cloudflared calendar-year updates merge automatically after validation and both native architecture builds pass; other major upgrades require review. The pipeline then creates a tag and GitHub Release. Home Assistant builds the updated add-on on your device.

Use Home Assistant to update this add-on; cloudflared's self-updater is disabled. Maintainers can follow the [one-time automation setup](CONTRIBUTING.md#one-time-github-setup).

## Help and feedback

- **Setup and troubleshooting:** [Cloudflare Tunnel documentation](cloudflared/DOCS.md)
- **What's new:** [Add-on changelog](cloudflared/CHANGELOG.md) · [GitHub releases](https://github.com/affeldt28/ha-addons-cloudflare/releases)
- **Bug reports and feature requests:** [GitHub issues](https://github.com/affeldt28/ha-addons-cloudflare/issues)
- **Contributing and local checks:** [Contributing guide](CONTRIBUTING.md)
- **Upstream documentation:** [Cloudflare Tunnel setup](https://developers.cloudflare.com/tunnel/get-started/) · [Home Assistant reverse proxies](https://www.home-assistant.io/integrations/http/#reverse-proxies)

When reporting a problem, include the add-on version, architecture, Home Assistant version and relevant logs. Remove tunnel tokens, passwords and other secrets first.

## Credits

Built around the official [cloudflared](https://github.com/cloudflare/cloudflared) client.

This repository is not an official Home Assistant or Cloudflare project. Cloudflare artwork belongs to Cloudflare, Inc.; see [source and attribution](branding/README.md).
