import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
CLIENT_DIR = Path(__file__).resolve().parents[1]
if str(CLIENT_DIR) not in sys.path:
    sys.path.insert(0, str(CLIENT_DIR))

from PyQt6.QtWidgets import QApplication, QLabel

from qidian_save.desktop.panels.announcement_panel import AnnouncementPanel


class FakeClient:
    def get_announcements(self):
        return []


class AnnouncementPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_renders_priority_title_and_content(self):
        panel = AnnouncementPanel(FakeClient())
        panel._on_announcements_ready([
            {
                "title": "维护通知",
                "content": "今晚会短暂维护",
                "priority": "important",
            }
        ])

        labels = "\n".join(child.text() for child in panel.findChildren(QLabel))
        self.assertIn("公告", labels)
        self.assertIn("【重要】维护通知", labels)
        self.assertIn("今晚会短暂维护", labels)
        self.assertFalse(panel.isHidden())

    def test_hides_when_no_announcements(self):
        panel = AnnouncementPanel(FakeClient())
        panel._on_announcements_ready([])

        self.assertTrue(panel.isHidden())


if __name__ == "__main__":
    unittest.main()
