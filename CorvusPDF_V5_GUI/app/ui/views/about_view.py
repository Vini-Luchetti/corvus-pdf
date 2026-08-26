"""Tela Sobre — identidade da GeralZona, enxuta e com personalidade."""
from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons")


class AboutView(QWidget):
    """Tela Sobre com logo, versão e identidade Corvus Labs."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ViewContainer")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(16)

        # Logo
        logo_path = os.path.normpath(os.path.join(_ASSETS_DIR, "corvo_logo.png"))
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path).scaled(
                80, 80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl = QLabel()
            logo_lbl.setPixmap(logo_pixmap)
            logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_lbl)

        # Nome do app
        name = QLabel("ORGANIZADOR PDF CORVUS")
        name.setObjectName("SectionTitle")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet("font-size: 18px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(name)

        # Versão
        version = QLabel("v5.0.0")
        version.setObjectName("SectionSubtitle")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        # Tagline
        tagline = QLabel("Junte. Separe. Organize. Sem frescura.")
        tagline.setObjectName("SectionSubtitle")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("font-style: italic; margin-top: 8px; margin-bottom: 8px;")
        layout.addWidget(tagline)

        # Separador visual
        sep = QLabel("─" * 32)
        sep.setObjectName("FileMeta")
        sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sep)

        # Desenvolvido por
        dev_by = QLabel("Desenvolvido por")
        dev_by.setObjectName("FileMeta")
        dev_by.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(dev_by)

        brand = QLabel("GeralZona")
        brand.setObjectName("SectionTitle")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(brand)

        # Link
        link_btn = QPushButton("geralzona.com")
        link_btn.setObjectName("GhostBtn")
        link_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        link_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://geralzona.com"))
        )
        link_btn.setStyleSheet(
            "font-size: 13px; text-decoration: underline; padding: 4px;"
        )
        layout.addWidget(link_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(8)

        # Ecossistema
        ecosystem = QLabel("Part of the Corvus Labs ecosystem")
        ecosystem.setObjectName("FileMeta")
        ecosystem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ecosystem)

        layout.addStretch()
