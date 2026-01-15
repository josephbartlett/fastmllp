# fastmllp Roadmap

## Phase 0: Project Setup
- Repo scaffolding, packaging layout, CI hooks.
- DESIGN and REQUIREMENTS finalized.
- CLI interface spec locked.

## Phase 1: Minimal MLLP + Always-ACK
Deliverables:
- MLLP framing/unframing utilities.
- TCP server that receives and ACKs any message.
- TCP client that sends and waits for ACK.
- Basic CLI: `fastmllp server` and `fastmllp send`.
- Config file support (TOML via `--config`).
- Structured logging with opt-in message logging.
- Max message size enforcement.
- Unit tests for framing and ACK.

Exit criteria:
- Server ACKs all inbound complete frames (even malformed).
- Client can send to local server and receive ACK.
- Basic docs and examples.

## Phase 2: Reliability and Observability
- Client reliability: retries with backoff, configurable retry count.
- Server robustness: connection limits, graceful shutdown, idle connection metrics.
- Better diagnostics: structured log fields for peer address and message IDs.
- Config validation warnings (unknown keys, type mismatches).
- Optional metrics hooks (Prometheus exporter or stats callback).
- Integration tests for failure scenarios (timeouts, oversized frames).

## Phase 3: Protocol Enhancements
- TLS and mTLS for server and client.
- Optional HL7 validation plugin interface.
- AE/AR responses when validation is enabled.
- Batch message support (if required by integrations).
- Improved MSH parsing and configurable ACK templates.

## Phase 4: Ecosystem & Integrations
- Published Docker image and optional Helm chart.
- Integration examples (Mirth, Iguana, Rhapsody, etc.).
- Operational guidance and deployment samples (systemd, docker-compose).
- Performance benchmarks and tuning guide.
