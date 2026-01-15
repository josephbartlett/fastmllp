# AGENTS.md

This file describes local expectations for coding agents working in this repo.

## Workflow
- Prefer Docker for development, linting, and tests.
- Build the dev image with `docker build -t fastmllp-dev .`.
- Lint with `docker run --rm -v "$PWD":/app -w /app fastmllp-dev ruff check .`.
- Test with `docker run --rm -v "$PWD":/app -w /app fastmllp-dev pytest -q`.

## Versioning
- Use Semantic Versioning with `0.y.z` until APIs stabilize.
- The single source of truth is `pyproject.toml`; runtime reads it via
  `importlib.metadata.version("fastmllp")`.
- Do not hardcode `__version__` values outside the package metadata.

## Changelog
- Keep `CHANGELOG.md` in Keep a Changelog format.
- Add new changes under `[Unreleased]`.
- On release, move entries to a dated version section and keep `[Unreleased]` empty.

## CI and Releases
- CI runs Dockerized lint and tests on every push/PR.
- Tagging `vX.Y.Z` triggers the release workflow:
  - Build sdist/wheel
  - Create a GitHub Release and attach artifacts
- Ensure the version in `pyproject.toml` matches the tag.
