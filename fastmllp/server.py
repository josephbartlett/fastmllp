import itertools
import logging as std_logging
import socket
import threading

from .ack import build_ack
from .logging import configure_logging, log_event
from .mllp import START_BLOCK, frame, unframe_stream


def serve(
    host: str,
    port: int,
    *,
    timeout: float = 10.0,
    encoding: str = "utf-8",
    max_size: int = 1048576,
    log_message: bool = False,
) -> None:
    logger = std_logging.getLogger("fastmllp")
    if not logger.handlers:
        logger = configure_logging("info")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    conn_counter = itertools.count(1)

    def handle_client(conn: socket.socket, addr: tuple[str, int], conn_id: int) -> None:
        log_event(logger, std_logging.INFO, "connect", conn_id=conn_id, addr=addr)
        buffer = b""
        try:
            conn.settimeout(timeout)
            while True:
                try:
                    chunk = conn.recv(4096)
                except TimeoutError:
                    log_event(logger, std_logging.INFO, "timeout", conn_id=conn_id)
                    break

                if not chunk:
                    break

                buffer += chunk
                frames, buffer = unframe_stream(buffer)

                for payload in frames:
                    message_text = payload.decode(encoding, errors="replace")
                    if log_message:
                        log_event(
                            logger,
                            std_logging.INFO,
                            "message_received",
                            conn_id=conn_id,
                            length=len(payload),
                            message=message_text,
                        )
                    else:
                        log_event(
                            logger,
                            std_logging.INFO,
                            "message_received",
                            conn_id=conn_id,
                            length=len(payload),
                        )

                    try:
                        ack_text = build_ack(message_text)
                    except Exception:
                        ack_text = build_ack("")
                        log_event(
                            logger,
                            std_logging.ERROR,
                            "ack_build_error",
                            conn_id=conn_id,
                        )

                    ack_bytes = frame(ack_text.encode(encoding, errors="replace"))
                    conn.sendall(ack_bytes)
                    log_event(
                        logger,
                        std_logging.INFO,
                        "ack_sent",
                        conn_id=conn_id,
                        length=len(ack_bytes),
                    )

                if buffer.startswith(START_BLOCK):
                    payload_len = max(len(buffer) - 1, 0)
                    if payload_len > max_size:
                        log_event(
                            logger,
                            std_logging.WARNING,
                            "frame_too_large",
                            conn_id=conn_id,
                            length=payload_len,
                        )
                        return
        except OSError as exc:
            log_event(
                logger,
                std_logging.ERROR,
                "connection_error",
                conn_id=conn_id,
                error=str(exc),
            )
        finally:
            conn.close()
            log_event(logger, std_logging.INFO, "disconnect", conn_id=conn_id)

    try:
        while True:
            conn, addr = server_socket.accept()
            conn_id = next(conn_counter)
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, conn_id),
                daemon=True,
            )
            thread.start()
    finally:
        server_socket.close()
