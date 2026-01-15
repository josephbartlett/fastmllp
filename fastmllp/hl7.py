DEFAULT_FIELD_SEP = "|"
DEFAULT_ENCODING_CHARS = "^~\\&"


def parse_msh(message: str) -> dict:
    """Parse MSH with best-effort defaults."""
    defaults = {
        "field_sep": DEFAULT_FIELD_SEP,
        "encoding_chars": DEFAULT_ENCODING_CHARS,
        "sending_app": "",
        "sending_fac": "",
        "receiving_app": "",
        "receiving_fac": "",
        "message_type": "",
        "trigger_event": "",
        "message_structure": "",
        "control_id": "",
        "processing_id": "",
        "version": "",
    }

    if not message.startswith("MSH") or len(message) < 4:
        return defaults

    field_sep = message[3]
    segment = message.split("\r", 1)[0]
    parts = segment.split(field_sep)

    encoding_chars = DEFAULT_ENCODING_CHARS
    if len(parts) > 1 and len(parts[1]) == 4:
        encoding_chars = parts[1]

    comp_sep = encoding_chars[0] if encoding_chars else "^"

    def get_field(index: int) -> str:
        return parts[index] if len(parts) > index else ""

    message_type = ""
    trigger_event = ""
    message_structure = ""
    message_type_field = get_field(8)
    if message_type_field:
        components = message_type_field.split(comp_sep)
        if components:
            message_type = components[0]
        if len(components) > 1:
            trigger_event = components[1]
        if len(components) > 2:
            message_structure = components[2]

    return {
        "field_sep": field_sep,
        "encoding_chars": encoding_chars,
        "sending_app": get_field(2),
        "sending_fac": get_field(3),
        "receiving_app": get_field(4),
        "receiving_fac": get_field(5),
        "message_type": message_type,
        "trigger_event": trigger_event,
        "message_structure": message_structure,
        "control_id": get_field(9),
        "processing_id": get_field(10),
        "version": get_field(11),
    }
