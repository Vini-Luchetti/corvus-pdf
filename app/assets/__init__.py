"""Utilitário de resolução de caminhos para assets empacotados.

Quando a aplicação roda via PyInstaller (frozen), o sys._MEIPASS aponta
para o diretório temporário onde os recursos foram extraídos. Em modo de
desenvolvimento, usa o diretório real do projeto. Usar sempre esta função
para referenciar qualquer arquivo dentro de app/assets/.
"""
from __future__ import annotations

import os
import sys


def asset_path(*parts: str) -> str:
    """Retorna o caminho absoluto de um asset, compatível com PyInstaller.

    Args:
        *parts: partes do caminho relativo ao diretório raiz do projeto.
                Ex: asset_path('app', 'assets', 'icons', 'corvo_logo.png')

    Returns:
        Caminho absoluto do arquivo.
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    return os.path.join(base, *parts)
