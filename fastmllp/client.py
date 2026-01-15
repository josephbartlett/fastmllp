import socket

from .mllp import frame, unframe_stream


def send(
    message: str | bytes,
    host: str,
    port: int,
    *,
    timeout: float = 10.0,
    encoding: str = "utf-8",
) -> str:
    if isinstance(message, str):
        payload = message.encode(encoding, errors="replace")
    elif isinstance(message, (bytes, bytearray)):
        payload = bytes(message)
    else:
        raise ValueError("message must be str or bytes")

    framed = frame(payload)
    buffer = b""

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(framed)
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                frames, buffer = unframe_stream(buffer)
                if frames:
                    return frames[0].decode(encoding, errors="replace")
    except TimeoutError as exc:
        raise TimeoutError("timed out waiting for ACK") from exc
    except OSError as exc:
        raise ConnectionError("connection error") from exc

    raise ConnectionError("no ACK received")
