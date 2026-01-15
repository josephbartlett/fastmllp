from fastmllp.hl7 import parse_msh


def test_parse_msh_fields() -> None:
    message = (
        "MSH|^~\\&|SND|SF|RCV|RF|20240101120000||ADT^A01|123|P|2.3\r"
        "PID|1||123"
    )
    parsed = parse_msh(message)
    assert parsed["field_sep"] == "|"
    assert parsed["encoding_chars"] == "^~\\&"
    assert parsed["sending_app"] == "SND"
    assert parsed["sending_fac"] == "SF"
    assert parsed["receiving_app"] == "RCV"
    assert parsed["receiving_fac"] == "RF"
    assert parsed["message_type"] == "ADT"
    assert parsed["trigger_event"] == "A01"
    assert parsed["control_id"] == "123"
    assert parsed["processing_id"] == "P"
    assert parsed["version"] == "2.3"


def test_parse_msh_defaults_when_missing() -> None:
    parsed = parse_msh("PID|1")
    assert parsed["field_sep"] == "|"
    assert parsed["encoding_chars"] == "^~\\&"
    assert parsed["sending_app"] == ""
