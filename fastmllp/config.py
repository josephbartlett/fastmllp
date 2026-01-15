import os
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - python < 3.11
    import tomli as tomllib

DEFAULT_SERVER = {
    "host": "0.0.0.0",
    "port": 2575,
    "timeout": 10.0,
    "encoding": "utf-8",
    "max_size": 1048576,
}

DEFAULT_CLIENT = {
    "host": "127.0.0.1",
    "port": 2575,
    "timeout": 10.0,
    "encoding": "utf-8",
}

DEFAULT_LOGGING = {
    "log_level": "info",
    "log_message": False,
}


def load_config(path: str | None) -> dict:
    if not path:
        return {}
    with open(path, "rb") as handle:
        return tomllib.load(handle)


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"invalid boolean value: {value}")


def read_env() -> dict:
    env: dict[str, Any] = {}
    if "FASTMLLP_HOST" in os.environ:
        env["host"] = os.environ["FASTMLLP_HOST"].strip()
    if "FASTMLLP_PORT" in os.environ:
        env["port"] = int(os.environ["FASTMLLP_PORT"])
    if "FASTMLLP_TIMEOUT" in os.environ:
        env["timeout"] = float(os.environ["FASTMLLP_TIMEOUT"])
    if "FASTMLLP_ENCODING" in os.environ:
        env["encoding"] = os.environ["FASTMLLP_ENCODING"].strip()
    if "FASTMLLP_LOG_LEVEL" in os.environ:
        env["log_level"] = os.environ["FASTMLLP_LOG_LEVEL"].strip().lower()
    if "FASTMLLP_LOG_MESSAGE" in os.environ:
        env["log_message"] = parse_bool(os.environ["FASTMLLP_LOG_MESSAGE"])
    if "FASTMLLP_MAX_SIZE" in os.environ:
        env["max_size"] = int(os.environ["FASTMLLP_MAX_SIZE"])
    return env


def resolve_value(
    cli_value: Any,
    env_value: Any,
    file_value: Any,
    default_value: Any,
) -> Any:
    for value in (cli_value, env_value, file_value, default_value):
        if value is not None:
            return value
    return None


def coerce_int(value: Any, name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    raise ValueError(f"{name} must be an integer")


def coerce_float(value: Any, name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a number")
    if isinstance(value, (int, float)):
        return float(value)
    raise ValueError(f"{name} must be a number")


def coerce_bool(value: Any, name: str) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise ValueError(f"{name} must be a boolean")


def validate_port(value: int) -> int:
    if value <= 0 or value > 65535:
        raise ValueError("port must be between 1 and 65535")
    return value


def validate_positive_int(value: int, name: str) -> int:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def validate_positive_float(value: float, name: str) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def resolve_server_config(cli_args: Any, config: dict) -> dict:
    env = read_env()
    server_cfg = config.get("server", {}) if config else {}
    logging_cfg = config.get("logging", {}) if config else {}

    port = resolve_value(
        cli_args.port,
        env.get("port"),
        coerce_int(server_cfg.get("port"), "server.port"),
        DEFAULT_SERVER["port"],
    )
    timeout = resolve_value(
        cli_args.timeout,
        env.get("timeout"),
        coerce_float(server_cfg.get("timeout"), "server.timeout"),
        DEFAULT_SERVER["timeout"],
    )
    max_size = resolve_value(
        cli_args.max_size,
        env.get("max_size"),
        coerce_int(server_cfg.get("max_size"), "server.max_size"),
        DEFAULT_SERVER["max_size"],
    )

    resolved = {
        "host": resolve_value(
            cli_args.host,
            env.get("host"),
            server_cfg.get("host"),
            DEFAULT_SERVER["host"],
        ),
        "port": validate_port(int(port)),
        "timeout": validate_positive_float(float(timeout), "timeout"),
        "encoding": resolve_value(
            cli_args.encoding,
            env.get("encoding"),
            server_cfg.get("encoding"),
            DEFAULT_SERVER["encoding"],
        ),
        "max_size": validate_positive_int(int(max_size), "max_size"),
        "log_level": resolve_value(
            cli_args.log_level,
            env.get("log_level"),
            logging_cfg.get("log_level"),
            DEFAULT_LOGGING["log_level"],
        ),
        "log_message": resolve_value(
            cli_args.log_message,
            env.get("log_message"),
            coerce_bool(logging_cfg.get("log_message"), "logging.log_message"),
            DEFAULT_LOGGING["log_message"],
        ),
    }
    return resolved


def resolve_client_config(cli_args: Any, config: dict) -> dict:
    env = read_env()
    client_cfg = config.get("client", {}) if config else {}
    logging_cfg = config.get("logging", {}) if config else {}

    port = resolve_value(
        cli_args.port,
        env.get("port"),
        coerce_int(client_cfg.get("port"), "client.port"),
        DEFAULT_CLIENT["port"],
    )
    timeout = resolve_value(
        cli_args.timeout,
        env.get("timeout"),
        coerce_float(client_cfg.get("timeout"), "client.timeout"),
        DEFAULT_CLIENT["timeout"],
    )

    resolved = {
        "host": resolve_value(
            cli_args.host,
            env.get("host"),
            client_cfg.get("host"),
            DEFAULT_CLIENT["host"],
        ),
        "port": validate_port(int(port)),
        "timeout": validate_positive_float(float(timeout), "timeout"),
        "encoding": resolve_value(
            cli_args.encoding,
            env.get("encoding"),
            client_cfg.get("encoding"),
            DEFAULT_CLIENT["encoding"],
        ),
        "log_level": resolve_value(
            cli_args.log_level,
            env.get("log_level"),
            logging_cfg.get("log_level"),
            DEFAULT_LOGGING["log_level"],
        ),
        "log_message": resolve_value(
            cli_args.log_message,
            env.get("log_message"),
            coerce_bool(logging_cfg.get("log_message"), "logging.log_message"),
            DEFAULT_LOGGING["log_message"],
        ),
    }
    return resolved
