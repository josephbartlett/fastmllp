# fastmllp CLI Spec

## Command Layout
```
fastmllp <command> [options]
```

Commands:
- `server` : run MLLP server
- `send`   : send a single HL7 message and wait for ACK
- `version`: print version

## Common Options
- `--config <path>`: optional TOML config file (only loaded if provided)
- `--log-level <level>`: `debug|info|warning|error`
- `--log-message` / `--no-log-message`: opt-in/out for raw HL7 payload logging

## Server Command
```
fastmllp server --host <host> --port <port> [options]
```

Options:
- `--host <host>`: default `0.0.0.0`
- `--port <port>`: default `2575`
- `--timeout <seconds>`: idle read timeout, default `10`
- `--encoding <name>`: default `utf-8`
- `--max-size <bytes>`: max payload size excluding MLLP framing, default `1048576`

Behavior:
- Always ACKs every complete frame (phase 1).
- Keeps connections open until the client closes or error occurs.
- Closes idle connections after `--timeout` seconds.
- Drops connections if a frame exceeds `--max-size`.

Exit codes:
- `0`: graceful shutdown
- `2`: failed to bind or startup error
- `3`: runtime fatal error

## Send Command
```
fastmllp send --host <host> --port <port> [input options] [options]
```

Input options (exactly one required):
- `--message <hl7>`: inline message string
- `--file <path>`: read message from file
- `--stdin`: read message from stdin

Other options:
- `--host <host>`: default `127.0.0.1`
- `--port <port>`: default `2575`
- `--timeout <seconds>`: connect/read timeout, default `10`
- `--encoding <name>`: default `utf-8`

Behavior:
- Sends a single message.
- Prints the ACK to stdout.
- Does not normalize or transform message bytes.
- `--message` is treated literally (no escape processing).

Exit codes:
- `0`: ACK received
- `1`: usage error
- `3`: connection error or timeout
- `4`: ACK parse/unframe error

## Environment Variables
- `FASTMLLP_HOST`
- `FASTMLLP_PORT`
- `FASTMLLP_TIMEOUT`
- `FASTMLLP_ENCODING`
- `FASTMLLP_LOG_LEVEL`
- `FASTMLLP_LOG_MESSAGE`
- `FASTMLLP_MAX_SIZE`

CLI flags override environment variables.
