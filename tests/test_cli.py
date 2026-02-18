from quran_persian_chatbot.cli import build_parser


def test_build_index_command_parses() -> None:
    parser = build_parser()
    args = parser.parse_args(["build-index"])

    assert args.command == "build-index"
