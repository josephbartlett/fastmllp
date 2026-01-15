# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to
Semantic Versioning.

## [Unreleased]

## [0.1.1] - 2026-01-15
### Added
- MIT license file.
- Docstrings for public API helpers.
- Oversize payload integration test.

### Changed
- CLI supports `--no-log-message` to override config defaults.

### Fixed
- Enforce `max_size` for complete frames before ACKing.

## [0.1.0] - 2026-01-15
### Added
- Initial HL7 MLLP client/server with always-ACK behavior.
- Docker-first dev/test workflow and GitHub Actions CI.
- CLI, library APIs, and test coverage for framing and ACK logic.
- Agent guidance for repo workflows and versioning.
- Tag-triggered release workflow with a GitHub Release and build artifacts.
