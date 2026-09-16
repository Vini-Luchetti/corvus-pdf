"""Tela Sobre — identidade da GeralZona e do ecossistema Corvus Labs."""
from __future__ import annotations

import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)

from app.assets import asset_path


class AboutView(QWidget):
    """Tela Sobre — identidade do Corvus PDF 1.0 e seu ecossistema."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ViewContainer")
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        inner = QWidget()
        inner.setObjectName("ViewContainer")
        root = QVBoxLayout(inner)
        root.setContentsMargins(48, 40, 48, 40)
        root.setSpacing(0)
        root.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        scroll.setWidget(inner)
        outer.addWidget(scroll)

        logo_file = asset_path("app", "assets", "icons", "corvo_logo.png")
        if os.path.exists(logo_file):
            pix = QPixmap(logo_file).scaled(
                72, 72,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl = QLabel()
            logo_lbl.setPixmap(pix)
            logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            root.addWidget(logo_lbl)
            root.addSpacing(12)

        app_name = QLabel("ORGANIZADOR PDF CORVUS")
        app_name.setObjectName("SectionTitle")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setStyleSheet("font-size: 16px; font-weight: 700; letter-spacing: 1.5px;")
        root.addWidget(app_name)

        version = QLabel("v1.0.0")
        version.setObjectName("SectionSubtitle")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("font-size: 12px; margin-bottom: 32px;")
        root.addWidget(version)

        root.addSpacing(24)

        crew_title = QLabel("THE CREW")
        crew_title.setObjectName("SectionTitle")
        crew_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        crew_title.setStyleSheet("font-size: 13px; font-weight: 700; letter-spacing: 3px;")
        root.addWidget(crew_title)
        root.addSpacing(20)

        for emoji, name, role, desc in [
            ("🐦‍⬛", "CORVUS REX", "Human Representative", "Product Direction · QA · Final Approval"),
            ("🧠", "GPTANGO", "Strategic Intelligence", "Product Strategy · Architecture · Design Direction"),
            ("⚙️", "CLAUDÃO", "Implementation Intelligence", "Engineering · Implementation"),
        ]:
            root.addWidget(self._crew_card(emoji, name, role, desc))
            root.addSpacing(12)

        root.addSpacing(20)

        divider = QLabel("─" * 40)
        divider.setObjectName("FileMeta")
        divider.setAlignment(Qt.AlignmentFlag.AlignCenter)
        divider.setStyleSheet("letter-spacing: 1px;")
        root.addWidget(divider)
        root.addSpacing(16)

        tagline1 = QLabel("One human. Two artificial intelligences.")
        tagline1.setObjectName("SectionSubtitle")
        tagline1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline1.setStyleSheet("font-size: 13px;")
        root.addWidget(tagline1)

        tagline2 = QLabel("One increasingly suspicious amount of software.")
        tagline2.setObjectName("SectionSubtitle")
        tagline2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline2.setStyleSheet("font-size: 13px; font-style: italic; margin-bottom: 24px;")
        root.addWidget(tagline2)

        root.addSpacing(24)

        brand = QLabel("GERALZONA")
        brand.setObjectName("SectionTitle")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet("font-size: 15px; font-weight: 700; letter-spacing: 2px;")
        root.addWidget(brand)

        link_btn = QPushButton("geralzona.com")
        link_btn.setObjectName("GhostBtn")
        link_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        link_btn.setStyleSheet("font-size: 13px; text-decoration: underline; padding: 4px;")
        link_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://geralzona.com")))
        root.addWidget(link_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        root.addSpacing(12)

        ecosystem = QLabel("Part of the Corvus Labs ecosystem")
        ecosystem.setObjectName("FileMeta")
        ecosystem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(ecosystem)
        root.addStretch()

    def _crew_card(self, emoji: str, name: str, role: str, desc: str) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        card.setMaximumWidth(480)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        emoji_lbl = QLabel(emoji)
        emoji_lbl.setFixedWidth(36)
        emoji_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emoji_lbl.setStyleSheet("font-size: 24px;")
        layout.addWidget(emoji_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        name_lbl = QLabel(name)
        name_lbl.setObjectName("FileName")
        name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; letter-spacing: 1px;")
        text_col.addWidget(name_lbl)

        role_lbl = QLabel(role)
        role_lbl.setObjectName("SectionSubtitle")
        role_lbl.setStyleSheet("font-size: 11px; font-weight: 500;")
        text_col.addWidget(role_lbl)

        desc_lbl = QLabel(desc)
        desc_lbl.setObjectName("FileMeta")
        desc_lbl.setStyleSheet("font-size: 11px;")
        text_col.addWidget(desc_lbl)

        layout.addLayout(text_col, 1)
        return card