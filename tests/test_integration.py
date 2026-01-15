import multiprocessing
import socket
import time

import pytest

from fastmllp.client import send
from fastmllp.server import serve


def run_server(port: int) -> None:
    serve("127.0.0.1", port, timeout=1.0, max_size=1024)


def get_free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def wait_for_port(host: str, port: int, timeout: float = 2.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return True
        except OSError:
            time.sleep(0.05)
    return False


def test_client_server_round_trip() -> None:
    port = get_free_port()
    process = multiprocessing.Process(target=run_server, args=(port,), daemon=True)
    process.start()
    try:
        assert wait_for_port("127.0.0.1", port)
        message = (
            "MSH|^~\\&|S|F|R|RF|20240101120000||ADT^A01|123|P|2.3\r"
            "PID|1||123"
        )
        ack = send(message, "127.0.0.1", port, timeout=2.0)
        assert "MSA|AA|123" in ack
    finally:
        process.terminate()
        process.join(timeout=2)


def test_server_rejects_oversize_payload() -> None:
    port = get_free_port()
    process = multiprocessing.Process(target=run_server, args=(port,), daemon=True)
    process.start()
    try:
        assert wait_for_port("127.0.0.1", port)
        payload = (
            "MSH|^~\\&|S|F|R|RF|20240101120000||ADT^A01|123|P|2.3\r"
            + ("X" * 2000)
        )
        with pytest.raises(ConnectionError):
            send(payload, "127.0.0.1", port, timeout=1.0)
    finally:
        process.terminate()
        process.join(timeout=2)
