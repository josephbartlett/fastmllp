# fastmllp Design

## Purpose
`fastmllp` is a small, reliable Python tool and library for HL7 v2 messaging over MLLP. It must be simple to operate, easy to embed, and safe for production usage.

Phase 1 focus: always ACK complete frames regardless of content.

## Goals
- Provide a TCP server that accepts MLLP-framed HL7 messages and returns ACKs.
- Provide a TCP client that sends MLLP-framed HL7 messages and waits for ACKs.
- Offer both a CLI and a Python library API.
- Keep dependencies minimal and avoid heavy HL7 parsing in phase 1.

## Non-goals (Phase 1)
- HL7 validation or schema enforcement.
- Advanced routing, transformations, or persistence.
- TLS, proxy, or authentication support (planned later).
- Async or event-driven server model (threaded blocking only in phase 1).

## Core Concepts
- MLLP framing:
  - Start block: 0x0b (VT)
  - End block: 0x1c (FS)
  - Segment terminator: 0x0d (CR)
- HL7 message parsing in phase 1 is best-effort:
  - If an MSH segment is present and parseable, ACK mirrors separators.
  - If not, use default separators and generate a safe ACK.

## Protocol and Framing Rules
- A frame starts with VT (0x0b) and ends with FS (0x1c) optionally followed by CR (0x0d).
- Any bytes before the first VT are discarded to resynchronize framing.
- A single socket read can contain multiple complete frames; all are processed.
- If FS is found without a trailing CR, treat FS as the terminator and continue.
- If a frame grows beyond `max_size` before its terminator, it is treated as malformed:
  - Log a warning with connection ID.
  - Drop the connection to prevent unbounded memory growth (no ACK because no complete frame was received).
- VT bytes inside a frame are treated as payload, not as a new frame start.
- `max_size` applies to the payload bytes between VT and FS (framing bytes are excluded).

## Connection and Concurrency Model
- Blocking TCP sockets with one thread per client connection.
- The main thread accepts connections; per-connection threads handle reads/writes.
- Connections remain open for multiple messages until the client closes or a timeout occurs.
- Server `timeout` is treated as idle timeout (no data read within `timeout` closes the connection).

## Message Normalization
- No HL7 normalization in phase 1.
- The client sends message bytes exactly as provided.
- The server decodes bytes with `errors="replace"` only for ACK construction.
- If a client message is provided as `str`, it is encoded using `errors="replace"`.

## Architecture
The project is split into a small set of modules with clear responsibilities.

```
fastmllp/
  __init__.py
  cli.py
  client.py
  server.py
  mllp.py
  hl7.py
  ack.py
  config.py
  logging.py
```

### Module Responsibilities
- `mllp.py`: frame/unframe bytes, handle stream buffering.
- `hl7.py`: minimal MSH parsing and separator detection; no deep validation.
- `ack.py`: build ACK messages based on inbound best-effort parsing.
- `server.py`: TCP listener, accept connections, read frames, send ACK.
- `client.py`: connect, send frame, read ACK.
- `cli.py`: entrypoint, maps flags to server/client operations.
- `config.py`: load CLI args and optional config file.
- `logging.py`: structured logging helpers with sane defaults.

## Message Flow
### Server (Receive)
1. Accept TCP connection.
2. Read bytes from socket.
3. Discard any bytes before the first VT.
4. Extract full MLLP frame(s) using `mllp.unframe_stream`.
5. For each frame:
   - Convert bytes to string with configured encoding (default: UTF-8, `errors="replace"`).
   - Build ACK with `ack.build_ack`.
   - Encode ACK with configured encoding (`errors="replace"`) and send as MLLP-framed bytes.
   - ACKs are sent in the same order frames are received.
6. Close connection on client close, timeout, or fatal errors.

### Client (Send)
1. Connect to TCP host/port.
2. Wrap outgoing HL7 message in MLLP frame.
3. Send framed bytes.
4. Read response and unframe to get ACK.
5. Return the first complete ACK frame; ignore any extra frames.
6. Return ACK to caller / print to stdout.

## ACK Strategy (Phase 1)
Goal: always ACK complete MLLP frames, regardless of inbound content.

Rules:
- If an MSH segment exists with a valid field separator, use it; else default to `|`.
- If encoding chars exist in MSH-2 (exactly 4 chars), use them; else default to `^~\&`.
- ACK message type is `ACK` with optional trigger event if inbound MSH-9 is parseable.
- MSA-1 is always `AA` (application accept).
- MSA-2 uses inbound MSH-10 (control ID) if present; otherwise generate a new ID.
- MSH-3/4 (sending app/fac) are taken from inbound MSH-5/6 (receiving app/fac).
- MSH-5/6 (receiving app/fac) are taken from inbound MSH-3/4 (sending app/fac).
- MSH-7 is current UTC timestamp in `YYYYMMDDHHMMSS`.
- MSH-10 is a newly generated control ID for the ACK.
- MSH-11 (processing ID) uses inbound MSH-11 if present, else `P`.
- MSH-12 (version) uses inbound MSH-12 if present, else `2.3`.

Field mapping details (best-effort):
- If inbound MSH-9 is `TYPE^TRIGGER^STRUCT`, ACK MSH-9 becomes `ACK^TRIGGER` (or `ACK` if missing).
- If inbound MSH-5/6 are missing, ACK MSH-3/4 default to `FASTMLLP`.
- If inbound MSH-3/4 are missing, ACK MSH-5/6 default to `UNKNOWN`.
- If inbound MSH-10 is missing, generate a UUID4 hex string and reuse it for both MSH-10 and MSA-2.
- ACK segments are separated with CR, and the ACK ends with a trailing CR.

Example ACK shape (fields are placeholders):
```
MSH|^~\&|RECEIVER|RECEIVER_FAC|SENDER|SENDER_FAC|20240101120000||ACK|12345|P|2.3
MSA|AA|12345
```

## Configuration
Configuration sources, from highest priority to lowest:
1. CLI flags
2. Environment variables
3. Optional config file (TOML)
4. Defaults

Key settings:
- `host`, `port`
- `timeout`: server idle read timeout, client connect/read timeout
- `encoding`: message encoding
- `log_level`
- `log_message`: opt-in raw message logging
- `max_size`: maximum payload size in bytes (framing excluded)

Config file format (TOML, loaded only when `--config` is provided):
```
[server]
host = "0.0.0.0"
port = 2575
timeout = 10
encoding = "utf-8"
max_size = 1048576

[client]
host = "127.0.0.1"
port = 2575
timeout = 10
encoding = "utf-8"

[logging]
log_level = "info"
log_message = false
```
Config sections map directly to CLI options and environment variables.

Defaults:
- `host`: `0.0.0.0` (server), `127.0.0.1` (client)
- `port`: `2575`
- `timeout`: `10` seconds
- `encoding`: `utf-8`
- `log_level`: `info`
- `log_message`: `false`
- `max_size`: `1048576`

## Error Handling
- Server must never crash on malformed input; log and ACK complete frames.
- Client errors (connect timeout, no ACK) should return non-zero exit code.
- Partial frames are buffered until complete.
- Frames exceeding `max_size` payload bytes are treated as malformed; server closes the connection.

## Logging
- Structured logs with timestamp, level, event, and connection ID.
- Log events: connect, disconnect, message received (length only), ACK sent, errors.
- Avoid logging full PHI by default; allow `--log-message` to log raw payloads.
- When `--log-message` is enabled, log raw content as received (no redaction).
- Connection IDs are monotonically increasing integers assigned on accept.

## Testing Strategy
- Unit tests for MLLP framing and stream parsing.
- Unit tests for ACK construction with and without MSH.
- Integration test: server receives, client sends, ACK returned.
- Regression tests for edge cases: missing MSH, weird separators, multiple frames in one read.
- Tests for framing errors: garbage before VT, FS without CR, oversized frames.

## Security & Safety
- Do not echo raw messages by default.
- Limit max message size (configurable).
- Close connections on invalid framing after `max_size` payload bytes.

## Future Enhancements (Not in Phase 1)
- TLS/mTLS support.
- HL7 validation and schema support.
- Advanced routing rules.
- Metrics and tracing hooks.
