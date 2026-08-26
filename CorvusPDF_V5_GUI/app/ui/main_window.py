"""MainWindow — App Shell do Corvus PDF.

Estrutura:
    ┌─── TopBar (logo + título + seletor de tema) ─────────────┐
    ├─── Sidebar ──┬─── ContentArea (QStackedWidget) ──────────┤
    │   • Merge    │                                            │
    │   • Split    │         view ativa                         │
    │   • Sobre    │                                            │
    └──────────────┴────────────────────────────────────────────┘
"""
from __future__ import annotations

import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QMainWindow, QMenu, QPushButton,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget,
)

from app.ui.theme.manager import ThemeManager
from app.ui.theme.tokens import THEME_ICONS, THEMES
from app.ui.views.about_view import AboutView
from app.ui.views.merge_view import MergeView
from app.ui.views.split_view import SplitView

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "icons")


class MainWindow(QMainWindow):
    """Janela principal — App Shell com sidebar, top bar e theme switcher."""

    def __init__(self, theme_manager: ThemeManager) -> None:
        super().__init__()
        self._theme_mgr = theme_manager
        self.setWindowTitle("Corvus PDF — GeralZona")
        self.setMinimumSize(860, 600)
        self.resize(960, 660)

        ico_path = os.path.normpath(os.path.join(_ASSETS_DIR, "corvo_logo.ico"))
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))

        self._build_ui()
        self._navigate("merge")

    def _build_ui(self) -> None:
        shell = QWidget()
        shell.setObjectName("AppShell")
        self.setCentralWidget(shell)

        root = QVBoxLayout(shell)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_topbar())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self._build_sidebar())
        body.addWidget(self._build_content(), 1)
        root.addLayout(body, 1)

    # ── Top Bar ───────────────────────────────────────────────────────────────

    def _build_topbar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(52)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        # Logo
        logo_path = os.path.normpath(os.path.join(_ASSETS_DIR, "corvo_logo.png"))
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(
                30, 30,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl = QLabel()
            logo_lbl.setPixmap(pix)
            layout.addWidget(logo_lbl)

        # Título
        title = QLabel("Organizador PDF Corvus")
        title.setObjectName("AppTitle")
        layout.addWidget(title)

        subtitle = QLabel("· GeralZona")
        subtitle.setObjectName("AppSubtitle")
        layout.addWidget(subtitle)

        layout.addStretch()

        # Seletor de tema compacto
        self._theme_btn = QPushButton()
        self._theme_btn.setObjectName("ThemeBtn")
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.clicked.connect(self._open_theme_menu)
        self._update_theme_btn()
        layout.addWidget(self._theme_btn)

        return bar

    def _open_theme_menu(self) -> None:
        menu = QMenu(self)
        for name in THEMES:
            icon = THEME_ICONS.get(name, "")
            action = menu.addAction(f"{icon}  {name}")
            action.setData(name)
        chosen = menu.exec(
            self._theme_btn.mapToGlobal(
                self._theme_btn.rect().bottomLeft()
            )
        )
        if chosen and chosen.data():
            self._theme_mgr.apply(chosen.data())
            self._update_theme_btn()

    def _update_theme_btn(self) -> None:
        name = self._theme_mgr.current
        icon = THEME_ICONS.get(name, "◐")
        self._theme_btn.setText(f"{icon}  {name}  ▾")

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(168)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(4)

        self._nav_buttons: dict[str, QPushButton] = {}
        nav_items = [
            ("merge",  "📄  Mesclar"),
            ("split",  "✂  Separar"),
            ("about",  "ℹ  Sobre"),
        ]
        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("NavItem")
            btn.setCheckable(False)
            btn.setProperty("active", False)
            btn.clicked.connect(lambda checked=False, k=key: self._navigate(k))
            self._nav_buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # Versão discreta no rodapé da sidebar
        ver = QLabel("v5.0.0")
        ver.setObjectName("FileMeta")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ver)

        return sidebar

    def _navigate(self, key: str) -> None:
        for k, btn in self._nav_buttons.items():
            btn.setProperty("active", k == key)
            btn.setStyle(btn.style())
        views = {"merge": 0, "split": 1, "about": 2}
        self._stack.setCurrentIndex(views.get(key, 0))

    # ── Content Area ──────────────────────────────────────────────────────────

    def _build_content(self) -> QWidget:
        area = QWidget()
        area.setObjectName("ContentArea")

        layout = QVBoxLayout(area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._stack = QStackedWidget()
        self._stack.setObjectName("ContentArea")
        self._stack.addWidget(MergeView())
        self._stack.addWidget(SplitView())
        self._stack.addWidget(AboutView())
        layout.addWidget(self._stack)

        return area
