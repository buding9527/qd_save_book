# -*- coding: utf-8 -*-
"""Shared announcement panel for desktop pages."""

import threading

from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QVBoxLayout

from ..components import SurfaceCard


class _AnnouncementSignals(QObject):
    ready = pyqtSignal(list)


_PRIORITY_LABEL = {"urgent": "【紧急】", "important": "【重要】", "normal": ""}


class AnnouncementPanel(SurfaceCard):
    """Fetch and render active server announcements without blocking the UI."""

    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.setObjectName("announcementPanel")
        self.client = client
        self._sig = _AnnouncementSignals()
        self._sig.ready.connect(self._on_announcements_ready)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        self.title_label = QLabel("公告")
        self.title_label.setProperty("ui-role", "section-title")
        layout.addWidget(self.title_label)

        self.body_label = QLabel("正在加载公告...")
        self.body_label.setProperty("ui-role", "status")
        self.body_label.setTextFormat(Qt.TextFormat.PlainText)
        self.body_label.setWordWrap(True)
        layout.addWidget(self.body_label)

        self.refresh()

    def refresh(self):
        def _run():
            try:
                items = self.client.get_announcements()
            except Exception:
                items = []
            self._sig.ready.emit(items or [])

        threading.Thread(target=_run, daemon=True).start()

    def _on_announcements_ready(self, items: list):
        if not items:
            self.hide()
            return

        lines = []
        for item in items:
            prefix = _PRIORITY_LABEL.get(str(item.get("priority", "")), "")
            title = str(item.get("title", "")).strip()
            content = str(item.get("content", "")).strip()
            if title:
                lines.append(f"{prefix}{title}")
            if content:
                lines.append(content)

        if not lines:
            self.hide()
            return

        self.body_label.setText("\n".join(lines))
        self.show()
