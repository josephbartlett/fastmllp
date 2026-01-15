# fastmllp Requirements

## Functional Requirements
- Provide an MLLP server that:
  - Listens on a configurable host/port.
  - Reads MLLP-framed HL7 v2 messages.
  - Sends an ACK for every complete frame received (phase 1: always accept).
  - Handles multiple messages per connection.
  - Handles multiple concurrent connections (thread-per-connection).
  - Survives malformed or partial input without crashing.
  - Discards any bytes before the first VT to resynchronize framing.
  - Closes the connection if a single frame payload exceeds `max_size` (framing excluded).

- Provide an MLLP client that:
  - Sends a single HL7 message to a host/port.
  - Waits for an ACK and returns it to the caller.
  - Uses configurable timeouts and exits non-zero on failure.
  - Does not normalize or transform the message body.

- Provide a CLI that:
  - Runs in `server` or `send` mode.
  - Accepts input from file, stdin, or inline string.
  - Prints ACK to stdout in `send` mode.
  - Preserves message bytes as provided by the input source.

- Provide a Python library API:
  - `send(message, host, port, timeout=...) -> ack`
  - `serve(host, port, timeout=..., encoding=..., max_size=...)`

## Non-Functional Requirements
- Python 3.10+.
- Minimal dependencies (stdlib preferred in phase 1).
- Cross-platform (Linux/Windows/macOS).
- Safe logging defaults (no PHI in logs unless opted in).
- Simple packaging with `pyproject.toml`.
- Deterministic ACK defaults when MSH is missing or malformed.

## Constraints
- Phase 1 must ACK every complete frame regardless of message content.
- No network access is required at build time.
- No HL7 validation in phase 1.

## Assumptions
- Messages are HL7 v2 over MLLP.
- Segment terminator is CR (0x0d).
- Message encoding is UTF-8 unless specified.
- Config file is only loaded when `--config` is provided.

## Out of Scope (Phase 1)
- TLS, authentication, or authorization.
- Message storage or queueing.
- GUI or web interface.
