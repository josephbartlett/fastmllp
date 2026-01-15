from fastmllp.ack import build_ack


def test_build_ack_from_msh() -> None:
    message = (
        "MSH|^~\\&|SND|SF|RCV|RF|20240101120000||ADT^A01|CTRL|P|2.5\r"
        "PID|1||123"
    )
    ack = build_ack(message)
    assert ack.endswith("\r")
    segments = ack.strip("\r").split("\r")
    msh_fields = segments[0].split("|")
    msa_fields = segments[1].split("|")

    assert msh_fields[0] == "MSH"
    assert msh_fields[1] == "^~\\&"
    assert msh_fields[2] == "RCV"
    assert msh_fields[3] == "RF"
    assert msh_fields[4] == "SND"
    assert msh_fields[5] == "SF"
    assert msh_fields[8] == "ACK^A01"
    assert msh_fields[9]
    assert msh_fields[10] == "P"
    assert msh_fields[11] == "2.5"

    assert msa_fields[0] == "MSA"
    assert msa_fields[1] == "AA"
    assert msa_fields[2] == "CTRL"


def test_build_ack_without_msh() -> None:
    ack = build_ack("PID|1")
    msh_fields = ack.split("\r")[0].split("|")
    assert msh_fields[0] == "MSH"
    assert msh_fields[1] == "^~\\&"
    assert msh_fields[2] == "FASTMLLP"
    assert msh_fields[3] == "FASTMLLP"
    assert msh_fields[4] == "UNKNOWN"
    assert msh_fields[5] == "UNKNOWN"
