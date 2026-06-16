import json
from pathlib import Path

from qidian_save.desktop.panels.qd_decrypt_panel import (
    _build_qd_zip_manifest,
    _chapter_id_from_result_name,
    _metadata_qd_entries,
    _qd_zip_arcname,
)


def test_qd_zip_arcname_includes_user_id_book_id_and_chapter_id():
    chapter = {
        "userId": "499283868",
        "bookId": "1047226185",
        "chapterId": "909754660",
    }

    assert _qd_zip_arcname(chapter) == "499283868/1047226185/909754660.qd"


def test_build_qd_zip_manifest_groups_books_and_chapters():
    chapters = [
        {
            "userId": "499283868",
            "bookId": "1047226185",
            "bookName": "骄阳似我",
            "chapterId": "461",
            "chapterName": "第471章 骄阳似我·茶艺祖师！",
        },
    ]

    manifest = _build_qd_zip_manifest(chapters)

    assert manifest == {
        "books": {
            "1047226185": {
                "bookName": "骄阳似我",
                "chapters": {"461": "第471章 骄阳似我·茶艺祖师！"},
            }
        }
    }
    json.dumps(manifest, ensure_ascii=False)


def test_metadata_qd_entries_include_book_metadata_file_once(tmp_path):
    book_dir = tmp_path / "499283868" / "1047226185"
    book_dir.mkdir(parents=True)
    meta = book_dir / "-10000.qd"
    meta.write_bytes(b"meta")
    chapters = [
        {"userId": "499283868", "bookId": "1047226185", "bookDir": str(book_dir), "chapterId": "461"},
        {"userId": "499283868", "bookId": "1047226185", "bookDir": str(book_dir), "chapterId": "462"},
    ]

    entries = _metadata_qd_entries(chapters)

    assert entries == [(Path(meta), "499283868/1047226185/-10000.qd")]


def test_chapter_id_from_result_name_supports_named_server_output():
    assert _chapter_id_from_result_name("461.txt") == "461"
    assert _chapter_id_from_result_name("461. 第471章 骄阳似我.txt") == "461"
    assert _chapter_id_from_result_name("nested/461. 第471章 骄阳似我.txt") == "461"
