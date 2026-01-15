import argparse
import sys

from . import __version__
from .client import send
from .config import load_config, resolve_client_config, resolve_server_config
from .logging import configure_logging
from .server import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fastmllp")
    parser.add_argument("--config", help="Path to TOML config file")
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default=None,
    )
    parser.add_argument(
        "--log-message",
        action="store_true",
        default=None,
        help="Log raw HL7 payloads",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    server_parser = subparsers.add_parser("server", help="Run MLLP server")
    server_parser.add_argument("--host", default=None)
    server_parser.add_argument("--port", type=int, default=None)
    server_parser.add_argument("--timeout", type=float, default=None)
    server_parser.add_argument("--encoding", default=None)
    server_parser.add_argument("--max-size", type=int, default=None)

    send_parser = subparsers.add_parser("send", help="Send one HL7 message")
    send_parser.add_argument("--host", default=None)
    send_parser.add_argument("--port", type=int, default=None)
    send_parser.add_argument("--timeout", type=float, default=None)
    send_parser.add_argument("--encoding", default=None)

    input_group = send_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--message", help="Inline HL7 message")
    input_group.add_argument("--file", help="Read message from file")
    input_group.add_argument("--stdin", action="store_true", help="Read message from stdin")

    subparsers.add_parser("version", help="Print version")

    return parser


def load_message(args: argparse.Namespace) -> str | bytes:
    if args.message is not None:
        return args.message
    if args.file is not None:
        with open(args.file, "rb") as handle:
            return handle.read()
    if args.stdin:
        return sys.stdin.buffer.read()
    raise ValueError("no input source specified")


def run_server(args: argparse.Namespace) -> int:
    try:
        config = load_config(args.config)
        resolved = resolve_server_config(args, config)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    configure_logging(resolved["log_level"])
    try:
        serve(
            resolved["host"],
            resolved["port"],
            timeout=resolved["timeout"],
            encoding=resolved["encoding"],
            max_size=resolved["max_size"],
            log_message=resolved["log_message"],
        )
    except KeyboardInterrupt:
        return 0
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    return 0


def run_send(args: argparse.Namespace) -> int:
    try:
        config = load_config(args.config)
        resolved = resolve_client_config(args, config)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    configure_logging(resolved["log_level"])
    try:
        message = load_message(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        ack = send(
            message,
            resolved["host"],
            resolved["port"],
            timeout=resolved["timeout"],
            encoding=resolved["encoding"],
        )
        sys.stdout.write(ack)
        return 0
    except TimeoutError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    except ConnectionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "server":
        return run_server(args)
    if args.command == "send":
        return run_send(args)

    print("error: unknown command", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
