# fastmllp API Spec

## Public API (Phase 1)

### `frame(message: bytes) -> bytes`
Wraps a payload in MLLP framing bytes.

### `unframe_stream(buffer: bytes) -> tuple[list[bytes], bytes]`
Extracts complete MLLP frames from a byte buffer.
Returns `(frames, remainder)`.
Behavior:
- Discards any bytes before the first VT.
- Treats FS as a frame terminator, consuming a trailing CR if present.
- Returns all complete frames found in the buffer.
- `remainder` contains any bytes after the last complete frame (including partial frames).

### `parse_msh(message: str) -> dict`
Best-effort parsing of the MSH segment.
Returns a dict with keys like `field_sep`, `encoding_chars`, `sending_app`, etc.
If MSH is missing or malformed, returns defaults.
Parsing rules:
- MSH is only recognized if the message starts with `MSH` and length >= 4.
- `field_sep` is the 4th character of the message.
- `encoding_chars` are the next 4 characters (positions 5-8); otherwise default.
Expected keys:
- `field_sep`
- `encoding_chars`
- `sending_app`, `sending_fac`
- `receiving_app`, `receiving_fac`
- `message_type`, `trigger_event`, `message_structure`
- `control_id`
- `processing_id`
- `version`

### `build_ack(message: str, *, ack_code: str = "AA") -> str`
Returns an HL7 ACK message string.
Uses best-effort MSH parsing and defaults if needed.
Behavior:
- Uses UTC `YYYYMMDDHHMMSS` for MSH-7.
- Uses inbound MSH-10 for MSA-2 if present; otherwise generates UUID4 hex.
- Uses the same generated UUID4 hex for ACK MSH-10 when inbound MSH-10 is missing.
- Defaults MSH-12 to `2.3` when missing.

### `send(message: str | bytes, host: str, port: int, *, timeout: float = 10.0, encoding: str = "utf-8") -> str`
Sends a message and returns the ACK string.
Behavior:
- `bytes` are used as-is.
- `str` is encoded using `encoding` with `errors="replace"`.
- No normalization or validation is applied.
- `timeout` applies to both connect and read operations.
- Returns the first complete ACK frame received; extra frames are ignored.

### `serve(host: str, port: int, *, timeout: float = 10.0, encoding: str = "utf-8", max_size: int = 1048576, log_message: bool = False) -> None`
Runs a blocking MLLP server that ACKs all messages.
Behavior:
- One thread per client connection.
- ACKs every complete frame regardless of content.
- Closes a connection if a single frame exceeds `max_size`.
- Encodes ACKs using the configured `encoding` with `errors="replace"`.
- Uses `timeout` as idle read timeout per connection.
- `max_size` applies to payload bytes excluding MLLP framing.
- When `log_message` is true, raw message payloads are logged.

## Error Model
- `send` raises `ConnectionError` or `TimeoutError` on connection issues.
- `send` raises `ValueError` on invalid input types.
- `serve` logs and continues on malformed input.

## Encoding Rules
- Input `bytes` are used as-is for framing.
- Input `str` is encoded using `encoding` with `errors="replace"`.
- Received bytes are decoded with `errors="replace"` and used for ACK building.

## Future API Extensions (Not in Phase 1)
- Async APIs (`async_send`, `serve_async`).
- Custom ACK handlers.
- TLS configuration.
