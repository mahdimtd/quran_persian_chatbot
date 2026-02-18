from quran_persian_chatbot.config import DEFAULT_DATA_FILES
from quran_persian_chatbot.indexing import find_text_files


def test_find_text_files_prefers_default_names(tmp_path) -> None:
    target_file = tmp_path / DEFAULT_DATA_FILES[0]
    other_file = tmp_path / "other.txt"
    target_file.write_text("a", encoding="utf-8")
    other_file.write_text("b", encoding="utf-8")

    files = find_text_files(tmp_path)

    assert files == [target_file]
