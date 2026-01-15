# fastmllp

Fast HL7 v2 MLLP client/server and CLI in Python for integration developers.
Phase 1 always ACKs complete frames regardless of content.

## Overview
`fastmllp` provides:
- A blocking TCP MLLP server that ACKs every complete frame.
- A client that sends one message and waits for the first ACK.
- A small, dependency-light library API with CLI wrappers.

It is designed for easy integration and test harnesses rather than deep HL7
validation or routing logic.

## Features
- MLLP framing/unframing helpers.
- Always-ACK behavior (AA) with best-effort MSH parsing.
- Thread-per-connection server for concurrent clients.
- CLI with file/stdin/message input options.
- Config file and environment overrides.
- Docker-first development workflow.

## Limitations (Phase 1)
- No TLS/mTLS.
- No HL7 schema validation or AE/AR responses.
- No message persistence or routing.
- No async server model.

## Install
```
pip install -e .
```

## Quickstart
Run the server:
```
fastmllp server --host 0.0.0.0 --port 2575
```

Send a message:
```
fastmllp send --host 127.0.0.1 --port 2575 --message "MSH|^~\\&|S|F|R|RF|20240101120000||ADT^A01|123|P|2.3\rPID|1||123"
```

Read from stdin:
```
cat message.hl7 | fastmllp send --stdin
```

## Config File
Provide a TOML file with `--config`:
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

## Library Usage
```
from fastmllp import send, serve

ack = send("MSH|^~\\&|S|F|R|RF|20240101120000||ADT^A01|123|P|2.3\\rPID|1||123", "127.0.0.1", 2575)

# Blocking server example (runs until interrupted)
serve("0.0.0.0", 2575)
```

## Logging and PHI
By default, logs include only message lengths. Use `--log-message` to log raw
payloads when needed, or `--no-log-message` to override config defaults. Be
mindful of PHI.

## Roadmap
See `ROADMAP.md` for planned phases and enhancements.

## Docker-First Development
This repo prefers Docker for development, linting, and tests to keep the
environment consistent across machines.

## Versioning
`fastmllp` follows SemVer with `0.y.z` while the API stabilizes.
The single source of truth for the version is `pyproject.toml`, and the runtime
reads it via `importlib.metadata`.
Tagging `vX.Y.Z` triggers the release workflow that builds artifacts and
creates a GitHub Release.

## Development (Docker)
Build the dev image:
```
docker build -t fastmllp-dev .
```

Run lint:
```
docker run --rm -v "$PWD":/app -w /app fastmllp-dev ruff check .
```

Run tests:
```
docker run --rm -v "$PWD":/app -w /app fastmllp-dev pytest -q
```
