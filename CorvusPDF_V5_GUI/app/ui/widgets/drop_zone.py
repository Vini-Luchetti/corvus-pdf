"""Widget DropZone — área de arrastar e soltar arquivos PDF."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFileDialog, QFrame, QLabel, QPushButton, QVBoxLayout


class DropZone(QFrame):
    """Área de drop com fallback de clique para diálogo de arquivo.

    Signals:
        files_dropped: emitido com lista de caminhos PDF quando arquivos são
                       recebidos (via drag-and-drop ou diálogo de seleção).
    """

    files_dropped: Signal = Signal(list)

    def __init__(
        self,
        label: str = "Arraste seus PDFs aqui",
        hint: str = "ou clique para adicionar arquivos",
        multi: bool = True,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._multi = multi
        self._build_ui(label, hint)

    def _build_ui(self, label: str, hint: str) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)
        layout.setContentsMargins(24, 32, 24, 32)

        icon = QLabel("📄")
        icon.setObjectName("DropZoneIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(label)
        lbl.setObjectName("DropZoneText")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h = QLabel(hint)
        h.setObjectName("DropZoneHint")
        h.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon)
        layout.addWidget(lbl)
        layout.addWidget(h)

    # ── DnD ───────────────────────────────────────────────────────────────────

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            pdfs = self._extract_pdfs(event.mimeData().urls())
            if pdfs:
                self.setObjectName("DropZoneActive")
                self.setStyle(self.style())
                event.acceptProposedAction()
                return
        event.ignore()

    def dragLeaveEvent(self, event) -> None:
        self.setObjectName("DropZone")
        self.setStyle(self.style())

    def dropEvent(self, event) -> None:
        self.setObjectName("DropZone")
        self.setStyle(self.style())
        pdfs = self._extract_pdfs(event.mimeData().urls())
        if pdfs:
            self.files_dropped.emit(pdfs)
        event.acceptProposedAction()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._open_dialog()

    def _open_dialog(self) -> None:
        if self._multi:
            paths, _ = QFileDialog.getOpenFileNames(
                self, "Selecionar PDFs", "", "PDF (*.pdf)"
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self, "Selecionar PDF", "", "PDF (*.pdf)"
            )
            paths = [path] if path else []
        if paths:
            self.files_dropped.emit(paths)

    @staticmethod
    def _extract_pdfs(urls) -> list[str]:
        return [
            u.toLocalFile()
            for u in urls
            if u.isLocalFile() and Path(u.toLocalFile()).suffix.lower() == ".pdf"
        ]
