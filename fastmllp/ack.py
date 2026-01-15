import datetime as dt
import uuid

from .hl7 import DEFAULT_ENCODING_CHARS, DEFAULT_FIELD_SEP, parse_msh


def build_ack(message: str, *, ack_code: str = "AA") -> str:
    msh = parse_msh(message)

    field_sep = msh.get("field_sep") or DEFAULT_FIELD_SEP
    encoding_chars = msh.get("encoding_chars") or DEFAULT_ENCODING_CHARS
    comp_sep = encoding_chars[0] if encoding_chars else "^"

    trigger_event = msh.get("trigger_event") or ""
    ack_type = "ACK"
    if trigger_event:
        ack_type = f"ACK{comp_sep}{trigger_event}"

    inbound_control_id = msh.get("control_id") or ""
    if inbound_control_id:
        msa_control_id = inbound_control_id
        ack_control_id = uuid.uuid4().hex
    else:
        ack_control_id = uuid.uuid4().hex
        msa_control_id = ack_control_id

    sending_app = msh.get("receiving_app") or "FASTMLLP"
    sending_fac = msh.get("receiving_fac") or "FASTMLLP"
    receiving_app = msh.get("sending_app") or "UNKNOWN"
    receiving_fac = msh.get("sending_fac") or "UNKNOWN"

    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    processing_id = msh.get("processing_id") or "P"
    version = msh.get("version") or "2.3"

    msh_fields = [
        "MSH",
        encoding_chars,
        sending_app,
        sending_fac,
        receiving_app,
        receiving_fac,
        timestamp,
        "",
        ack_type,
        ack_control_id,
        processing_id,
        version,
    ]
    msa_fields = ["MSA", ack_code, msa_control_id]

    return field_sep.join(msh_fields) + "\r" + field_sep.join(msa_fields) + "\r"
