"""View de Merge — N PDFs com seleção de páginas → 1 PDF."""
from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QScrollArea, QTextEdit,
    QVBoxLayout, QWidget,
)
from pypdf import PdfReader

from app.services.pdf_service import MergeWorker
from app.ui.widgets.drop_zone import DropZone


class _FileRow(QWidget):
    """Linha de arquivo na lista de merge (nome + campo de páginas + remover)."""

    def __init__(self, path: str, total: int, on_remove, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("FileRow")
        self.path = path
        self.total = total

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Ícone
        icon = QLabel("📄")
        icon.setFixedWidth(20)
        layout.addWidget(icon)

        # Nome do arquivo
        name = os.path.basename(path)
        if len(name) > 38:
            name = name[:35] + "…"
        name_lbl = QLabel(name)
        name_lbl.setObjectName("FileName")
        name_lbl.setMinimumWidth(200)
        layout.addWidget(name_lbl, 1)

        # Total de páginas
        meta = QLabel(f"{total}p")
        meta.setObjectName("FileMeta")
        meta.setFixedWidth(36)
        layout.addWidget(meta)

        # Campo de seleção de páginas
        pages_label = QLabel("Páginas:")
        pages_label.setObjectName("FileMeta")
        layout.addWidget(pages_label)

        self.pages_input = QLineEdit()
        self.pages_input.setObjectName("Input")
        self.pages_input.setPlaceholderText(f"ex: 1-3, 5  (vazio = todas)")
        self.pages_input.setFixedWidth(160)
        layout.addWidget(self.pages_input)

        # Botão remover
        rm_btn = QPushButton("✕")
        rm_btn.setObjectName("GhostBtn")
        rm_btn.setFixedWidth(28)
        rm_btn.clicked.connect(on_remove)
        layout.addWidget(rm_btn)

    def get_data(self) -> dict:
        return {
            "path": self.path,
            "pages": self.pages_input.text(),
            "total": self.total,
        }


class MergeView(QWidget):
    """Tela de Merge: adicionar PDFs, selecionar páginas, gerar um PDF único."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ViewContainer")
        self._rows: list[_FileRow] = []
        self._worker: MergeWorker | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Header
        title = QLabel("Mesclar PDFs")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("Combine vários PDFs em um único arquivo")
        subtitle.setObjectName("SectionSubtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        # Drop zone
        self._drop = DropZone(multi=True)
        self._drop.setMinimumHeight(110)
        self._drop.files_dropped.connect(self._add_files)
        root.addWidget(self._drop)

        # Lista de arquivos
        list_label = QLabel("ARQUIVOS")
        list_label.setObjectName("SectionLabel")
        root.addWidget(list_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setMinimumHeight(140)

        self._list_container = QWidget()
        self._list_container.setObjectName("FileRow")
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(0)
        self._list_layout.addStretch()

        scroll.setWidget(self._list_container)
        root.addWidget(scroll, 1)

        # Saída
        out_label = QLabel("SAÍDA")
        out_label.setObjectName("SectionLabel")
        root.addWidget(out_label)

        out_frame = QFrame()
        out_frame.setObjectName("Card")
        out_layout = QVBoxLayout(out_frame)
        out_layout.setContentsMargins(12, 12, 12, 12)
        out_layout.setSpacing(8)

        # Pasta
        folder_row = QHBoxLayout()
        self._folder_input = QLineEdit()
        self._folder_input.setObjectName("Input")
        self._folder_input.setPlaceholderText("Pasta de saída…")
        folder_btn = QPushButton("Pasta")
        folder_btn.setObjectName("SecondaryBtn")
        folder_btn.clicked.connect(self._pick_folder)
        folder_row.addWidget(self._folder_input, 1)
        folder_row.addWidget(folder_btn)
        out_layout.addLayout(folder_row)

        # Nome do arquivo
        name_row = QHBoxLayout()
        name_lbl = QLabel("Nome:")
        name_lbl.setObjectName("FileMeta")
        name_lbl.setFixedWidth(48)
        self._name_input = QLineEdit("resultado.pdf")
        self._name_input.setObjectName("Input")
        name_row.addWidget(name_lbl)
        name_row.addWidget(self._name_input)
        out_layout.addLayout(name_row)
        root.addWidget(out_frame)

        # Log
        self._log = QTextEdit()
        self._log.setObjectName("LogBox")
        self._log.setReadOnly(True)
        self._log.setMaximumHeight(80)
        root.addWidget(self._log)

        # Progress
        self._progress = QProgressBar()
        self._progress.setRange(0, 0)
        self._progress.setVisible(False)
        root.addWidget(self._progress)

        # Actions
        actions = QHBoxLayout()
        self._clear_btn = QPushButton("Limpar lista")
        self._clear_btn.setObjectName("SecondaryBtn")
        self._clear_btn.clicked.connect(self._clear_list)

        self._merge_btn = QPushButton("▶  JUNTAR PDF")
        self._merge_btn.setObjectName("PrimaryBtn")
        self._merge_btn.clicked.connect(self._run_merge)

        actions.addWidget(self._clear_btn)
        actions.addStretch()
        actions.addWidget(self._merge_btn)
        root.addLayout(actions)

    # ── File Management ───────────────────────────────────────────────────────

    def _add_files(self, paths: list[str]) -> None:
        for path in paths:
            try:
                total = len(PdfReader(path).pages)
            except Exception as e:
                self._log_msg(f"Erro ao abrir {os.path.basename(path)}: {e}")
                continue
            idx = len(self._rows)
            row = _FileRow(path, total, lambda i=idx: self._remove_row(i))
            self._rows.append(row)
            self._list_layout.insertWidget(self._list_layout.count() - 1, row)
            if not self._folder_input.text():
                self._folder_input.setText(os.path.dirname(os.path.abspath(path)))
            self._log_msg(f"Adicionado: {os.path.basename(path)} ({total}p)")

    def _remove_row(self, idx: int) -> None:
        if idx < len(self._rows):
            row = self._rows.pop(idx)
            row.setParent(None)
            row.deleteLater()

    def _clear_list(self) -> None:
        for row in self._rows:
            row.setParent(None)
            row.deleteLater()
        self._rows.clear()
        self._log.clear()

    # ── Output ───────────────────────────────────────────────────────────────

    def _pick_folder(self) -> None:
        d = QFileDialog.getExistingDirectory(self, "Pasta de saída")
        if d:
            self._folder_input.setText(d)

    # ── Merge ─────────────────────────────────────────────────────────────────

    def _run_merge(self) -> None:
        if not self._rows:
            self._log_msg("Nenhum arquivo na lista.")
            return
        folder = self._folder_input.text() or os.getcwd()
        name = self._name_input.text().strip() or "resultado.pdf"
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        out_path = os.path.join(folder, name)
        files = [row.get_data() for row in self._rows]

        self._set_busy(True)
        self._log.clear()
        self._worker = MergeWorker(files, out_path)
        self._worker.log.connect(self._log_msg)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_finished(self, n_files: int, n_pages: int, elapsed: float) -> None:
        self._set_busy(False)
        self._log_msg(f"✓ {n_files} arquivo(s) · {n_pages} página(s) · {elapsed:.2f}s")

    def _on_error(self, msg: str) -> None:
        self._set_busy(False)
        self._log_msg(f"Erro: {msg}")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        self._merge_btn.setEnabled(not busy)
        self._clear_btn.setEnabled(not busy)
        self._progress.setVisible(busy)

    def _log_msg(self, msg: str) -> None:
        self._log.append(msg)
        self._log.verticalScrollBar().setValue(
            self._log.verticalScrollBar().maximum()
        )
