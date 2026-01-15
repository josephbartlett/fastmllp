# fastmllp Design Decisions

Record key architectural decisions here. Add new entries as choices are made.

## Decision 001: Use stdlib sockets (no heavy deps)
- Status: Accepted
- Rationale: Keep the tool lightweight and easy to install.

## Decision 002: Always ACK in Phase 1
- Status: Accepted
- Rationale: Aligns with initial requirement to ACK regardless of content.

## Decision 003: Best-effort MSH parsing
- Status: Accepted
- Rationale: Allows reasonable ACK construction without full HL7 parsing.

## Decision 004: Minimal CLI interface
- Status: Accepted
- Rationale: Keep surface area small while core features mature.

## Decision 005: Thread-per-connection server
- Status: Accepted
- Rationale: Simplest model with clear behavior and low dependency cost.

## Decision 006: Multi-message connections
- Status: Accepted
- Rationale: Common for MLLP clients; reduces connection churn.

## Decision 007: Framing recovery and terminator handling
- Status: Accepted
- Rationale: Discard garbage before VT and accept FS with optional CR to improve interoperability.

## Decision 008: No message normalization in phase 1
- Status: Accepted
- Rationale: Avoids unintended content changes; keeps tool predictable.

## Decision 009: ACK defaults
- Status: Accepted
- Rationale: Use UTC `YYYYMMDDHHMMSS` timestamps, default HL7 version `2.3`, and UUID4 hex for missing control IDs.
