"""Serviço de operações PDF com workers assíncronos (QThread).

A lógica de merge e split vive aqui, isolada da UI. Os workers emitem
sinais Qt para comunicar progresso, log e conclusão — a UI apenas conecta
slots a esses sinais, sem bloquear a thread principal.
"""
from __future__ import annotations

import os
import time

from PySide6.QtCore import QThread, Signal
from pypdf import PdfReader, PdfWriter

from app.core.pdf_utils import parse_pages, safe_path


class MergeWorker(QThread):
    """Worker de merge: N PDFs (com seleção de páginas) → 1 PDF.

    Signals:
        log: mensagem de log para exibição na UI.
        finished: emitido ao concluir (n_arquivos, n_paginas, elapsed_s).
        error: emitido se uma exceção não tratada ocorrer.
    """

    log: Signal = Signal(str)
    finished: Signal = Signal(int, int, float)
    error: Signal = Signal(str)

    def __init__(self, files: list[dict], out_path: str) -> None:
        """
        Args:
            files: lista de dicts {'path': str, 'pages': str, 'total': int}.
            out_path: caminho completo do PDF de saída.
        """
        super().__init__()
        self._files = files
        self._out_path = out_path

    def run(self) -> None:
        t0 = time.time()
        writer = PdfWriter()
        total_pages = 0
        try:
            for item in self._files:
                reader = PdfReader(item['path'])
                indices = parse_pages(item['pages'], item['total'])
                name = os.path.basename(item['path'])
                self.log.emit(f"Adicionando {name} — {len(indices)} página(s)")
                for idx in indices:
                    writer.add_page(reader.pages[idx])
                total_pages += len(indices)

            with open(self._out_path, 'wb') as f:
                writer.write(f)
            writer.close()

            elapsed = time.time() - t0
            self.log.emit(f"Concluído → {os.path.basename(self._out_path)}")
            self.finished.emit(len(self._files), total_pages, elapsed)
        except Exception as exc:
            self.error.emit(str(exc))


class SplitWorker(QThread):
    """Worker de split: 1+ PDFs → N PDFs por página ou por ranges.

    Signals:
        log: mensagem de log para exibição na UI.
        finished: emitido ao concluir (n_arquivos_gerados, n_paginas, elapsed_s).
        error: emitido se uma exceção não tratada ocorrer.
    """

    log: Signal = Signal(str)
    finished: Signal = Signal(int, int, float)
    error: Signal = Signal(str)

    def __init__(
        self,
        files: list[dict],
        out_folder: str,
        mode: str,
        ranges: list[str],
    ) -> None:
        """
        Args:
            files: lista de dicts {'path': str, 'total': int}.
            out_folder: pasta de saída.
            mode: 'all' (uma página por arquivo) ou 'ranges'.
            ranges: lista de strings de range (usado apenas se mode=='ranges').
        """
        super().__init__()
        self._files = files
        self._out_folder = out_folder
        self._mode = mode
        self._ranges = ranges

    def run(self) -> None:
        t0 = time.time()
        total_out = 0
        total_pages = 0
        try:
            for item in self._files:
                reader = PdfReader(item['path'])
                base = os.path.splitext(os.path.basename(item['path']))[0]
                total = item['total']
                total_pages += total
                self.log.emit(f"Processando {base}.pdf — {total} página(s)")

                if self._mode == 'all':
                    for i, page in enumerate(reader.pages):
                        writer = PdfWriter()
                        writer.add_page(page)
                        out = safe_path(self._out_folder, f'{base}_p{i + 1:03d}')
                        with open(out, 'wb') as f:
                            writer.write(f)
                        writer.close()
                        total_out += 1
                    self.log.emit(f"{total} arquivo(s) gerado(s)")
                else:
                    for i, rng in enumerate(self._ranges):
                        pages = parse_pages(rng, total)
                        if not pages:
                            self.log.emit(f"Range {i + 1} vazio, ignorado")
                            continue
                        writer = PdfWriter()
                        for pg in pages:
                            writer.add_page(reader.pages[pg])
                        out = safe_path(self._out_folder, f'{base}_{i + 1:02d}')
                        with open(out, 'wb') as f:
                            writer.write(f)
                        writer.close()
                        total_out += 1
                        self.log.emit(f"Range {i + 1} → {os.path.basename(out)}")

            elapsed = time.time() - t0
            self.finished.emit(total_out, total_pages, elapsed)
        except Exception as exc:
            self.error.emit(str(exc))
