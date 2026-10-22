ARG BUILD_FROM=alpine:3.23
FROM cloudflare/cloudflared:2026.10.3 AS cloudflared
FROM ${BUILD_FROM}
RUN apk add --no-cache ca-certificates jq
COPY --from=cloudflared /usr/local/bin/cloudflared /usr/local/bin/cloudflared
COPY rootfs /
RUN chmod 0755 /usr/local/bin/run-cloudflared
ARG BUILD_ARCH
ARG BUILD_VERSION=1.0.0
LABEL io.hass.type="addon" \
	io.hass.name="Cloudflare Tunnel" \
	io.hass.arch="${BUILD_ARCH}" \
	io.hass.version="${BUILD_VERSION}"
ENTRYPOINT ["/usr/local/bin/run-cloudflared"]
