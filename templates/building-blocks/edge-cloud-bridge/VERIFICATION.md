# Verification log — edge-cloud-bridge

Original verification date: 2026-07-28  
Multi-notebook migration re-verification: 2026-08-05

Docs index: https://docs.coreflux.org/llms.txt  
Primary plugin page: `/latest/lot-language/routes/data-pipeline/mqtt-bridge`

## 2026-08-05 migration re-verification

The migration moved existing definitions into solution, simulator, and production
notebooks and normalized the site identifier to `site-plant`. No new LOT keyword or
plugin key was introduced.

- `DEFINE MODEL ... WITH TOPIC ...`, typed `ADD`, topic sources, static values, `AS TRIGGER`, and `TIMESTAMP "UTC"` — CONFIRMED — `/latest/lot-language/models/schema-definition` — 2026-08-05
- `DEFINE ACTION`, `ON TOPIC`, `TOPIC POSITION`, `GET JSON ... IN PAYLOAD AS DOUBLE`, conditionals, string concatenation, and `PUBLISH TOPIC` — CONFIRMED — `/latest/lot-language/actions/overview` and `/latest/lot-language/actions/operations` — 2026-08-05
- `ON EVERY <n> SECONDS`, typed `GET TOPIC`, `EMPTY` checks, arithmetic, `RANDOM DOUBLE BETWEEN`, `KEEP TOPIC`, and `PUBLISH TOPIC` used by all simulator Actions — CONFIRMED — `/latest/lot-language/actions/events` and `/latest/lot-language/actions/operations` — 2026-08-05
- `DEFINE ROUTE ... WITH TYPE MQTT_BRIDGE`, `BROKER SELF`, destination connection keys, mapping keys, and `RECONNECTION_RETRIES` — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-08-05
- Production TLS keys `USE_TLS`, `ALLOW_UNTRUSTED_CERTS`, `SERVER_CA_CERT_PATH`, `CLIENT_CERT_PATH`, and `CLIENT_CERT_PASS` — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-08-05
- `DEFINE RULE`, priority, Publish/Subscribe topic scopes, `USER IS`, `OR`, `ALLOW`, `DENY`, and optional `ELSE` — CONFIRMED — `/latest/lot-language/rules/syntax` — 2026-08-05
- MQTT_BRIDGE store-and-forward buffer, queue, QoS, and restart-persistence semantics — UNCONFIRMED — absent from `/latest/lot-language/routes/data-pipeline/mqtt-bridge`; only `RECONNECTION_RETRIES` is documented — 2026-08-05
- Effect of deploying a Rule on an already-connected MQTT session — UNCONFIRMED — `/latest/lot-language/rules/syntax` documents per-operation evaluation but not session transition behavior — 2026-08-05

## Constructs

- `DEFINE ROUTE ... WITH TYPE MQTT_BRIDGE` — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-07-28
- `ADD SOURCE_CONFIG` / `WITH BROKER SELF` — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-07-28
- `ADD DESTINATION_CONFIG` with `BROKER_ADDRESS`, `BROKER_PORT`, `CLIENT_ID`, `USERNAME`, `PASSWORD`, `USE_TLS`, `ALLOW_UNTRUSTED_CERTS`, `SERVER_CA_CERT_PATH`, `CLIENT_CERT_PATH`, `CLIENT_CERT_PASS`, `RECONNECTION_RETRIES` — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-07-28
- `ADD MAPPING <name>` with `SOURCE_TOPIC`, `DESTINATION_TOPIC`, `DIRECTION` (`out` | `in` | `both`) — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-07-28
- Topic remap/prefix via different `SOURCE_TOPIC` / `DESTINATION_TOPIC` (incl. `+` / `#` wildcards in examples) — CONFIRMED — `/latest/lot-language/routes/data-pipeline/mqtt-bridge` — 2026-07-28
- MQTT_BRIDGE dedicated `QOS` configuration key — UNCONFIRMED — not listed on mqtt-bridge page — 2026-07-28
- MQTT_BRIDGE store-and-forward / offline message buffer / queue size / persistence across restart — UNCONFIRMED — docs only document `RECONNECTION_RETRIES` (default 5) for offline resilience — 2026-07-28
- `DEFINE MODEL ... WITH TOPIC ...` / `ADD <TYPE> ... WITH TOPIC ... AS TRIGGER` / `WITH TIMESTAMP "UTC"` / static `WITH "..."` — CONFIRMED — `/latest/lot-language/models` and `/latest/lot-language/models/schema-definition` — 2026-07-28
- Wildcard Models (`sensors/+/...`) — CONFIRMED — `/latest/lot-language/models/examples` (multi-instance) — 2026-07-28; this template uses explicit per-machine Models to keep raw→clean path prefixes unambiguous
- `DEFINE ACTION` / `ON EVERY n SECONDS` / `ON TOPIC` / `SET` / `PUBLISH TOPIC` / `KEEP TOPIC` / `GET TOPIC ... AS DOUBLE|INT` / `IF`/`ELSE IF`/`ELSE` — CONFIRMED — `/latest/lot-language/actions/syntax`, `/latest/lot-language/actions/operations`, `/latest/lot-language/actions/overview` — 2026-07-28
- `RANDOM DOUBLE BETWEEN a AND b` / `RANDOM INT BETWEEN a AND b` — CONFIRMED — `/latest/lot-language/actions/operations` — 2026-07-28
- `GET JSON "field" IN PAYLOAD AS DOUBLE` — CONFIRMED — `/latest/lot-language/actions/overview` — 2026-07-28
- `TOPIC POSITION n` — CONFIRMED — `/latest/lot-language/actions/events` — 2026-07-28
- `IF GET TOPIC "..." == EMPTY` — CONFIRMED — `/latest/lot-language/actions/events` — 2026-07-28
- `KEEP TOPIC` retained vs `PUBLISH TOPIC` non-retained — CONFIRMED — `/latest/lot-language/actions/operations` — 2026-07-28
- `DEFINE RULE ... WITH PRIORITY n FOR Publish|Subscribe TO TOPIC "..."` / `USER IS` / `ALLOW`/`DENY` / `OR` — CONFIRMED — `/latest/lot-language/rules/syntax` — 2026-07-28
- Rule priority: lower number = higher priority; first matching rule wins — CONFIRMED — `/latest/lot-language/rules/syntax` — 2026-07-28
- Redeploy same-named Rule replaces previous definition — CONFIRMED — `/latest/lot-language/rules` — 2026-07-28
- Effect of deploying a Rule on an already-connected MQTT session — UNCONFIRMED — docs describe per-operation evaluation but do not state mid-session behavior explicitly — 2026-07-28
- `-addUser <username> <password>` — CONFIRMED — `/latest/mqtt-broker/commands` — 2026-07-28
- Docker image `coreflux/coreflux-mqtt-broker` with ports 1883/5000/8080/8443 and named volume `/etc/project` — CONFIRMED — `/latest/quick-start/installation` (and `/v2.0/quick-start/installation`) — 2026-07-28
- Dual-broker / two-container licensing limits — UNCONFIRMED — installation docs describe Docker and cloud trial for a single broker; no published statement that two local containers are forbidden or allowed under trial — document honestly and advise confirming license terms with Coreflux for production multi-broker use — 2026-07-28

## Spec verification flags (resolved)

| Flag | Resolution |
|---|---|
| Documented store-and-forward semantics and limits | **UNCONFIRMED.** README must not claim store-and-forward. Documented offline behavior is reconnection retries only (`RECONNECTION_RETRIES`). Compose "pause cloud" test demonstrates reconnect, not buffered catch-up. |
| Topic remap/prefix syntax in the bridge Route | **CONFIRMED** via `ADD MAPPING` `SOURCE_TOPIC` / `DESTINATION_TOPIC`. |

## Unconfirmed / follow-ups

1. MQTT_BRIDGE store-and-forward, buffer size, QoS knobs, persistence across broker restart.
2. Mid-session Rule activation effect on already-connected clients (assumed to apply to subsequent operations; not spelled out).
3. Licensing for two concurrent local broker containers on trial/community terms.
4. Whether `#` multi-level remap in `DESTINATION_TOPIC` preserves the full matched suffix the same way `+` does (examples use both; treat as confirmed-by-pattern, re-check if remap misbehaves).
