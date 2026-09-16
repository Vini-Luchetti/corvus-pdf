"""ThemeManager — converte design tokens em QSS e aplica à aplicação.

Trocar de tema = uma chamada a apply(). Nenhum widget conhece qual tema
está ativo; todos usam classes de objeto Qt que este manager estiliza.
"""
from __future__ import annotations

from PySide6.QtWidgets import QApplication

from app.ui.theme.tokens import THEMES


def _build_qss(t: dict[str, str]) -> str:
    """Gera o stylesheet completo a partir de um dicionário de tokens."""
    return f"""
    /* ── App Shell ─────────────────────────────────────────────── */
    QMainWindow, QDialog {{
        background-color: {t['--bg-app']};
    }}
    QWidget#AppShell {{
        background-color: {t['--bg-app']};
    }}

    /* ── Top Bar ────────────────────────────────────────────────── */
    QWidget#TopBar {{
        background-color: {t['--bg-sidebar']};
        border-bottom: 1px solid {t['--border-subtle']};
    }}
    QLabel#AppTitle {{
        color: {t['--text-primary']};
        font-size: 14px;
        font-weight: 600;
    }}
    QLabel#AppSubtitle {{
        color: {t['--text-muted']};
        font-size: 11px;
    }}

    /* ── Sidebar ────────────────────────────────────────────────── */
    QWidget#Sidebar {{
        background-color: {t['--bg-sidebar']};
        border-right: 1px solid {t['--border-subtle']};
    }}
    QPushButton#NavItem {{
        background-color: transparent;
        color: {t['--text-secondary']};
        text-align: left;
        padding: 10px 16px;
        border: none;
        border-radius: 6px;
        font-size: 13px;
    }}
    QPushButton#NavItem:hover {{
        background-color: {t['--nav-item-hover']};
        color: {t['--text-primary']};
    }}
    QPushButton#NavItem[active=true] {{
        background-color: {t['--nav-item-active-bg']};
        color: {t['--nav-item-active-fg']};
        font-weight: 600;
    }}

    /* ── Content Area ───────────────────────────────────────────── */
    QWidget#ContentArea {{
        background-color: {t['--bg-app']};
    }}
    QWidget#ViewContainer {{
        background-color: {t['--bg-app']};
    }}

    /* ── Cards / Surfaces ───────────────────────────────────────── */
    QFrame#Card {{
        background-color: {t['--bg-surface']};
        border: 1px solid {t['--border-subtle']};
        border-radius: 8px;
    }}
    QFrame#CardElevated {{
        background-color: {t['--bg-surface-elevated']};
        border: 1px solid {t['--border-default']};
        border-radius: 8px;
    }}

    /* ── Drop Zone ──────────────────────────────────────────────── */
    QFrame#DropZone {{
        background-color: {t['--bg-surface']};
        border: 2px dashed {t['--border-default']};
        border-radius: 10px;
    }}
    QFrame#DropZone:hover {{
        border-color: {t['--accent-primary']};
        background-color: {t['--bg-surface-elevated']};
    }}
    QFrame#DropZoneActive {{
        background-color: {t['--bg-surface-elevated']};
        border: 2px dashed {t['--accent-primary']};
        border-radius: 10px;
    }}
    QLabel#DropZoneIcon {{
        color: {t['--text-muted']};
        font-size: 28px;
    }}
    QLabel#DropZoneText {{
        color: {t['--text-secondary']};
        font-size: 13px;
    }}
    QLabel#DropZoneHint {{
        color: {t['--text-muted']};
        font-size: 11px;
    }}

    /* ── File List ──────────────────────────────────────────────── */
    QWidget#FileRow {{
        background-color: {t['--bg-surface']};
        border-bottom: 1px solid {t['--border-subtle']};
    }}
    QWidget#FileRow:hover {{
        background-color: {t['--bg-surface-elevated']};
    }}
    QLabel#FileName {{
        color: {t['--text-primary']};
        font-size: 13px;
    }}
    QLabel#FileMeta {{
        color: {t['--text-muted']};
        font-size: 11px;
    }}

    /* ── Inputs ─────────────────────────────────────────────────── */
    QLineEdit, QLineEdit#Input {{
        background-color: {t['--bg-input']};
        color: {t['--text-primary']};
        border: 1px solid {t['--border-default']};
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 12px;
        selection-background-color: {t['--accent-primary']};
    }}
    QLineEdit:focus {{
        border-color: {t['--border-focus']};
    }}

    /* ── Buttons ────────────────────────────────────────────────── */
    QPushButton#PrimaryBtn {{
        background-color: {t['--accent-primary']};
        color: {t['--text-on-accent']};
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#PrimaryBtn:hover {{
        background-color: {t['--accent-primary-hover']};
    }}
    QPushButton#PrimaryBtn:pressed {{
        background-color: {t['--accent-primary-active']};
    }}
    QPushButton#PrimaryBtn:disabled {{
        background-color: {t['--border-default']};
        color: {t['--text-muted']};
    }}
    QPushButton#SecondaryBtn {{
        background-color: transparent;
        color: {t['--text-secondary']};
        border: 1px solid {t['--border-default']};
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 12px;
    }}
    QPushButton#SecondaryBtn:hover {{
        border-color: {t['--border-focus']};
        color: {t['--text-primary']};
    }}
    QPushButton#SecondaryBtn:disabled {{
        color: {t['--text-muted']};
        border-color: {t['--border-subtle']};
    }}
    QPushButton#GhostBtn {{
        background-color: transparent;
        color: {t['--text-muted']};
        border: none;
        padding: 4px 8px;
        font-size: 12px;
        border-radius: 4px;
    }}
    QPushButton#GhostBtn:hover {{
        color: {t['--color-error']};
        background-color: {t['--bg-surface-elevated']};
    }}
    QPushButton#ThemeBtn {{
        background-color: transparent;
        color: {t['--text-secondary']};
        border: 1px solid {t['--border-subtle']};
        border-radius: 5px;
        padding: 5px 12px;
        font-size: 12px;
    }}
    QPushButton#ThemeBtn:hover {{
        border-color: {t['--border-default']};
        color: {t['--text-primary']};
    }}
    QPushButton#ThemeBtn::menu-indicator {{ width: 0px; }}

    /* ── Option Cards (Split mode selector) ─────────────────────── */
    QPushButton#OptionCard {{
        background-color: {t['--bg-surface']};
        color: {t['--text-secondary']};
        border: 1px solid {t['--border-default']};
        border-radius: 8px;
        padding: 12px 16px;
        text-align: left;
        font-size: 12px;
    }}
    QPushButton#OptionCard:hover {{
        border-color: {t['--accent-primary']};
        color: {t['--text-primary']};
        background-color: {t['--bg-surface-elevated']};
    }}
    QPushButton#OptionCard[selected=true] {{
        border-color: {t['--accent-primary']};
        background-color: {t['--nav-item-active-bg']};
        color: {t['--nav-item-active-fg']};
        font-weight: 600;
    }}

    /* ── Section Labels ─────────────────────────────────────────── */
    QLabel#SectionTitle {{
        color: {t['--text-primary']};
        font-size: 16px;
        font-weight: 600;
    }}
    QLabel#SectionSubtitle {{
        color: {t['--text-secondary']};
        font-size: 12px;
    }}
    QLabel#SectionLabel {{
        color: {t['--text-muted']};
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    /* ── Log / Status ───────────────────────────────────────────── */
    QTextEdit#LogBox {{
        background-color: {t['--bg-input']};
        color: {t['--text-secondary']};
        border: 1px solid {t['--border-subtle']};
        border-radius: 6px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 11px;
        padding: 8px;
    }}

    /* ── Progress Bar ───────────────────────────────────────────── */
    QProgressBar {{
        background-color: {t['--bg-surface']};
        border: none;
        border-radius: 3px;
        height: 4px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: {t['--accent-primary']};
        border-radius: 3px;
    }}

    /* ── Scrollbars ─────────────────────────────────────────────── */
    QScrollBar:vertical {{
        background: {t['--bg-app']};
        width: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {t['--border-default']};
        border-radius: 4px;
        min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {t['--text-muted']};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background: {t['--bg-app']};
        height: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background: {t['--border-default']};
        border-radius: 4px;
        min-width: 24px;
    }}

    /* ── Menu (theme dropdown) ──────────────────────────────────── */
    QMenu {{
        background-color: {t['--bg-surface-elevated']};
        border: 1px solid {t['--border-default']};
        border-radius: 6px;
        padding: 4px;
        color: {t['--text-primary']};
        font-size: 12px;
    }}
    QMenu::item {{
        padding: 7px 24px 7px 12px;
        border-radius: 4px;
    }}
    QMenu::item:selected {{
        background-color: {t['--nav-item-active-bg']};
        color: {t['--nav-item-active-fg']};
    }}

    /* ── Misc ───────────────────────────────────────────────────── */
    QLabel {{
        color: {t['--text-secondary']};
    }}
    QSplitter::handle {{
        background-color: {t['--border-subtle']};
    }}
    """


class ThemeManager:
    """Gerencia o tema ativo da aplicação.

    Mantém o nome do tema atual e aplica o QSS correspondente à QApplication.
    """

    def __init__(self, app: QApplication, initial: str = "Clean Dark") -> None:
        self._app = app
        self._current = initial
        self.apply(initial)

    @property
    def current(self) -> str:
        return self._current

    def apply(self, name: str) -> None:
        """Aplica um tema pelo nome. Troca instantânea, zero reboot."""
        if name not in THEMES:
            raise ValueError(f"Tema desconhecido: {name!r}. Disponíveis: {list(THEMES)}")
        self._current = name
        self._app.setStyleSheet(_build_qss(THEMES[name]))
