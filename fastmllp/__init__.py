from importlib.metadata import PackageNotFoundError, version

from .ack import build_ack
from .client import send
from .hl7 import parse_msh
from .mllp import frame, unframe_stream
from .server import serve

__all__ = [
    "__version__",
    "build_ack",
    "frame",
    "parse_msh",
    "send",
    "serve",
    "unframe_stream",
]

try:
    __version__ = version("fastmllp")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
