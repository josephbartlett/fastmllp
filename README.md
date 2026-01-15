# fastmllp

Fast HL7 v2 MLLP client/server in Python. Phase 1 always ACKs complete frames
regardless of content.

## Docker-First Development
This repo prefers Docker for development, linting, and tests to keep the
environment consistent across machines.

## Versioning
`fastmllp` follows SemVer with `0.y.z` while the API stabilizes.
The single source of truth for the version is `pyproject.toml`, and the runtime
reads it via `importlib.metadata`.
Tagging `vX.Y.Z` triggers the release workflow that builds artifacts and
creates a GitHub Release.

## Install
```
pip install -e .
```

## CLI Usage
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
Provide a TOML file with `--config`. See `DESIGN.md` for the schema.

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
