START_BLOCK = b"\x0b"
END_BLOCK = b"\x1c"
CARRIAGE_RETURN = b"\x0d"


def frame(message: bytes) -> bytes:
    """Wrap payload bytes in MLLP framing."""
    return START_BLOCK + message + END_BLOCK + CARRIAGE_RETURN


def unframe_stream(buffer: bytes) -> tuple[list[bytes], bytes]:
    """Extract MLLP frames from a byte buffer and return frames plus remainder."""
    frames: list[bytes] = []
    if not buffer:
        return frames, b""

    start = buffer.find(START_BLOCK)
    if start == -1:
        return frames, b""
    buffer = buffer[start:]

    while buffer:
        if buffer[:1] != START_BLOCK:
            start = buffer.find(START_BLOCK)
            if start == -1:
                return frames, b""
            buffer = buffer[start:]
            continue

        end = buffer.find(END_BLOCK, 1)
        if end == -1:
            return frames, buffer

        payload = buffer[1:end]
        next_index = end + 1
        if buffer[next_index:next_index + 1] == CARRIAGE_RETURN:
            next_index += 1
        frames.append(payload)
        buffer = buffer[next_index:]

        if not buffer:
            return frames, b""

        start = buffer.find(START_BLOCK)
        if start == -1:
            return frames, b""
        if start > 0:
            buffer = buffer[start:]

    return frames, b""
