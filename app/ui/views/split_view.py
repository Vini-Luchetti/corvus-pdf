"""View de Split — 1+ PDFs → N PDFs (por página ou por ranges).

Implementa progressive disclosure: cada etapa aparece apenas quando
a etapa anterior está completa, reduzindo ruído visual.
Todo o conteúdo fica dentro de um QScrollArea para que nenhum elemento
desapareça quando a janela for redimensionada.
"""
from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QScrollArea, QTextEdit,
    QVBoxLayout, QWidget,
)
from pypdf import PdfReader

from app.services.pdf_service import SplitWorker
from app.ui.widgets.drop_zone import DropZone


class SplitView(QWidget):
    """Tela de Split com interface por etapas (progressive disclosure)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ViewContainer")
        self._files: list[dict] = []
        self._mode: str = "all"
        self._range_inputs: list[QLineEdit] = []
        self._worker: SplitWorker | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        # ScrollArea envolvendo todo o conteúdo — garante que nada
        # desapareça quando a janela for menor que o conteúdo da view.
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        inner_widget = QWidget()
        inner_widget.setObjectName("ViewContainer")
        root = QVBoxLayout(inner_widget)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        scroll.setWidget(inner_widget)
        outer.addWidget(scroll)

        # Header
        title = QLabel("Separar PDF")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("Divida um PDF em partes ou extraia páginas específicas")
        subtitle.setObjectName("SectionSubtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        # ── Etapa 1: Drop Zone ────────────────────────────────────────────────
        step1_lbl = QLabel("1  SELECIONAR ARQUIVO(S)")
        step1_lbl.setObjectName("SectionLabel")
        root.addWidget(step1_lbl)

        self._drop = DropZone(
            label="Arraste seu PDF aqui",
            hint="ou clique para selecionar arquivo",
            multi=True,
        )
        self._drop.setMinimumHeight(100)
        self._drop.files_dropped.connect(self._add_files)
        root.addWidget(self._drop)

        # Lista de arquivos carregados
        list_scroll = QScrollArea()
        list_scroll.setWidgetResizable(True)
        list_scroll.setFrameShape(QFrame.Shape.NoFrame)
        list_scroll.setMaximumHeight(120)
        list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._file_list_container = QWidget()
        self._file_list_layout = QVBoxLayout(self._file_list_container)
        self._file_list_layout.setContentsMargins(0, 0, 0, 0)
        self._file_list_layout.setSpacing(0)
        self._file_list_layout.addStretch()
        list_scroll.setWidget(self._file_list_container)
        root.addWidget(list_scroll)

        # ── Etapa 2: Modo (aparece após carregar arquivo) ─────────────────────
        self._step2 = QWidget()
        self._step2.setVisible(False)
        step2_layout = QVBoxLayout(self._step2)
        step2_layout.setContentsMargins(0, 0, 0, 0)
        step2_layout.setSpacing(8)

        step2_lbl = QLabel("2  ESCOLHER MODO")
        step2_lbl.setObjectName("SectionLabel")
        step2_layout.addWidget(step2_lbl)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(8)
        self._btn_all = self._make_mode_card(
            "Todas as páginas", "Uma página por arquivo", "all"
        )
        self._btn_ranges = self._make_mode_card(
            "Ranges específicos", "Um arquivo por range", "ranges"
        )
        cards_row.addWidget(self._btn_all)
        cards_row.addWidget(self._btn_ranges)
        step2_layout.addLayout(cards_row)
        root.addWidget(self._step2)

        # ── Etapa 3: Configuração contextual (só ranges) ──────────────────────
        self._step3 = QWidget()
        self._step3.setVisible(False)
        step3_layout = QVBoxLayout(self._step3)
        step3_layout.setContentsMargins(0, 0, 0, 0)
        step3_layout.setSpacing(8)

        step3_lbl = QLabel("3  CONFIGURAR RANGES")
        step3_lbl.setObjectName("SectionLabel")
        step3_layout.addWidget(step3_lbl)

        ranges_card = QFrame()
        ranges_card.setObjectName("Card")
        ranges_inner = QVBoxLayout(ranges_card)
        ranges_inner.setContentsMargins(12, 12, 12, 12)
        ranges_inner.setSpacing(8)

        self._ranges_layout = QVBoxLayout()
        self._ranges_layout.setSpacing(6)
        ranges_inner.addLayout(self._ranges_layout)

        add_range_btn = QPushButton("+ Adicionar range")
        add_range_btn.setObjectName("SecondaryBtn")
        add_range_btn.clicked.connect(self._add_range)
        ranges_inner.addWidget(add_range_btn)

        hint = QLabel("Sintaxe: 1-3, 5, 7-9  (igual ao diálogo de impressão do Windows)")
        hint.setObjectName("DropZoneHint")
        ranges_inner.addWidget(hint)
        step3_layout.addWidget(ranges_card)
        root.addWidget(self._step3)

        # ── Saída ─────────────────────────────────────────────────────────────
        self._step4 = QWidget()
        self._step4.setVisible(False)
        step4_layout = QVBoxLayout(self._step4)
        step4_layout.setContentsMargins(0, 0, 0, 0)
        step4_layout.setSpacing(8)

        out_lbl = QLabel("SAÍDA")
        out_lbl.setObjectName("SectionLabel")
        step4_layout.addWidget(out_lbl)

        out_row = QHBoxLayout()
        self._folder_input = QLineEdit()
        self._folder_input.setObjectName("Input")
        self._folder_input.setPlaceholderText("Pasta de saída…")
        folder_btn = QPushButton("Pasta")
        folder_btn.setObjectName("SecondaryBtn")
        folder_btn.clicked.connect(self._pick_folder)
        out_row.addWidget(self._folder_input, 1)
        out_row.addWidget(folder_btn)
        step4_layout.addLayout(out_row)
        root.addWidget(self._step4)

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
        self._clear_btn = QPushButton("Limpar")
        self._clear_btn.setObjectName("SecondaryBtn")
        self._clear_btn.clicked.connect(self._clear)

        self._split_btn = QPushButton("▶  DIVIDIR PDF")
        self._split_btn.setObjectName("PrimaryBtn")
        self._split_btn.setEnabled(False)
        self._split_btn.clicked.connect(self._run_split)

        actions.addWidget(self._clear_btn)
        actions.addStretch()
        actions.addWidget(self._split_btn)
        root.addLayout(actions)
        root.addStretch()

        # Seleciona modo padrão
        self._select_mode("all")

    def _make_mode_card(self, title: str, desc: str, mode: str) -> QPushButton:
        btn = QPushButton(f"{title}\n{desc}")
        btn.setObjectName("OptionCard")
        btn.setProperty("selected", False)
        btn.setMinimumHeight(60)
        btn.clicked.connect(lambda: self._select_mode(mode))
        return btn

    def _select_mode(self, mode: str) -> None:
        self._mode = mode
        for btn, m in [(self._btn_all, "all"), (self._btn_ranges, "ranges")]:
            btn.setProperty("selected", m == mode)
            btn.setStyle(btn.style())
        self._step3.setVisible(mode == "ranges")
        if mode == "ranges" and not self._range_inputs:
            self._add_range()

    # ── Arquivos ──────────────────────────────────────────────────────────────

    def _add_files(self, paths: list[str]) -> None:
        for path in paths:
            try:
                total = len(PdfReader(path).pages)
            except Exception as e:
                self._log_msg(f"Erro: {os.path.basename(path)}: {e}")
                continue
            self._files.append({"path": path, "total": total})
            self._add_file_row(path, total)
            if not self._folder_input.text():
                self._folder_input.setText(os.path.dirname(os.path.abspath(path)))
            self._log_msg(f"Carregado: {os.path.basename(path)} ({total}p)")

        if self._files:
            self._step2.setVisible(True)
            self._step4.setVisible(True)
            self._split_btn.setEnabled(True)

    def _add_file_row(self, path: str, total: int) -> None:
        row = QWidget()
        row.setObjectName("FileRow")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(8, 6, 8, 6)
        rl.setSpacing(10)

        icon = QLabel("📄")
        icon.setFixedWidth(20)
        rl.addWidget(icon)

        name = os.path.basename(path)
        if len(name) > 50:
            name = name[:47] + "…"
        name_lbl = QLabel(name)
        name_lbl.setObjectName("FileName")
        rl.addWidget(name_lbl, 1)

        meta = QLabel(f"{total}p")
        meta.setObjectName("FileMeta")
        rl.addWidget(meta)

        idx = len(self._files) - 1
        rm = QPushButton("✕")
        rm.setObjectName("GhostBtn")
        rm.setFixedWidth(28)
        rm.clicked.connect(lambda checked=False, i=idx: self._remove_file(i))
        rl.addWidget(rm)

        self._file_list_layout.insertWidget(
            self._file_list_layout.count() - 1, row
        )

    def _remove_file(self, idx: int) -> None:
        if idx < len(self._files):
            self._files.pop(idx)
        for i in reversed(range(self._file_list_layout.count() - 1)):
            w = self._file_list_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        for i, f in enumerate(self._files):
            self._add_file_row(f["path"], f["total"])
        if not self._files:
            self._step2.setVisible(False)
            self._step4.setVisible(False)
            self._split_btn.setEnabled(False)

    # ── Ranges ───────────────────────────────────────────────────────────────

    def _add_range(self) -> None:
        idx = len(self._range_inputs)
        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        lbl = QLabel(f"Range {idx + 1}:")
        lbl.setObjectName("FileMeta")
        lbl.setFixedWidth(64)
        rl.addWidget(lbl)

        inp = QLineEdit()
        inp.setObjectName("Input")
        inp.setPlaceholderText("ex: 1-5, 8-10")
        self._range_inputs.append(inp)
        rl.addWidget(inp, 1)

        arrow = QLabel(f"→ arquivo_{idx + 1:02d}.pdf")
        arrow.setObjectName("FileMeta")
        rl.addWidget(arrow)

        rm = QPushButton("✕")
        rm.setObjectName("GhostBtn")
        rm.setFixedWidth(28)
        rm.clicked.connect(lambda checked=False, i=idx: self._remove_range(i))
        rl.addWidget(rm)

        self._ranges_layout.addWidget(row)

    def _remove_range(self, idx: int) -> None:
        if idx < len(self._range_inputs):
            self._range_inputs.pop(idx)
        for i in reversed(range(self._ranges_layout.count())):
            w = self._ranges_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        vals = [inp.text() for inp in self._range_inputs]
        self._range_inputs.clear()
        for v in vals:
            self._add_range()
            self._range_inputs[-1].setText(v)

    # ── Output ───────────────────────────────────────────────────────────────

    def _pick_folder(self) -> None:
        d = QFileDialog.getExistingDirectory(self, "Pasta de saída")
        if d:
            self._folder_input.setText(d)

    # ── Split ─────────────────────────────────────────────────────────────────

    def _run_split(self) -> None:
        if not self._files:
            return
        folder = self._folder_input.text() or os.getcwd()
        ranges = [inp.text() for inp in self._range_inputs]

        self._set_busy(True)
        self._log.clear()
        self._worker = SplitWorker(self._files, folder, self._mode, ranges)
        self._worker.log.connect(self._log_msg)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_finished(self, n_out: int, n_pages: int, elapsed: float) -> None:
        self._set_busy(False)
        self._log_msg(f"✓ {n_out} arquivo(s) gerado(s) · {n_pages} página(s) · {elapsed:.2f}s")

    def _on_error(self, msg: str) -> None:
        self._set_busy(False)
        self._log_msg(f"Erro: {msg}")

    def _clear(self) -> None:
        self._files.clear()
        for i in reversed(range(self._file_list_layout.count() - 1)):
            w = self._file_list_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        self._step2.setVisible(False)
        self._step3.setVisible(False)
        self._step4.setVisible(False)
        self._split_btn.setEnabled(False)
        self._log.clear()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        self._split_btn.setEnabled(not busy)
        self._clear_btn.setEnabled(not busy)
        self._progress.setVisible(busy)

    def _log_msg(self, msg: str) -> None:
        self._log.append(msg)
        self._log.verticalScrollBar().setValue(
            self._log.verticalScrollBar().maximum()
        )
