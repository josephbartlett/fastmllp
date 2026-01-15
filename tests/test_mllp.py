from fastmllp import mllp


def test_frame_wraps_payload() -> None:
    assert mllp.frame(b"ABC") == b"\x0bABC\x1c\x0d"


def test_unframe_single_frame() -> None:
    frames, remainder = mllp.unframe_stream(b"\x0bABC\x1c\x0d")
    assert frames == [b"ABC"]
    assert remainder == b""


def test_unframe_without_cr() -> None:
    frames, remainder = mllp.unframe_stream(b"\x0bABC\x1c")
    assert frames == [b"ABC"]
    assert remainder == b""


def test_unframe_discards_garbage_before_vt() -> None:
    frames, remainder = mllp.unframe_stream(b"garbage")
    assert frames == []
    assert remainder == b""


def test_unframe_partial_frame() -> None:
    frames, remainder = mllp.unframe_stream(b"\x0bABC")
    assert frames == []
    assert remainder == b"\x0bABC"


def test_unframe_multiple_frames() -> None:
    data = b"\x0bA\x1c\x0d\x0bB\x1c\x0d"
    frames, remainder = mllp.unframe_stream(data)
    assert frames == [b"A", b"B"]
    assert remainder == b""


def test_unframe_skips_garbage_between_frames() -> None:
    data = b"\x0bA\x1c\x0dgarbage\x0bB\x1c\x0d"
    frames, remainder = mllp.unframe_stream(data)
    assert frames == [b"A", b"B"]
    assert remainder == b""
