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
- Timeouts, retries, backoff for client.
- Connection handling improvements (keepalive, connection limits).
- Improved diagnostics and log context.

## Phase 3: Protocol Enhancements
- TLS/mTLS support.
- Better HL7 parsing (optional).
- Support for batch messages (if required).
- Optional validation with AE/AR responses.

## Phase 4: Ecosystem & Integrations
- Docker image and Helm chart.
- Prometheus metrics.
- Integration examples (Mirth, Iguana, etc.).
