"""Utilitários de domínio PDF — lógica pura, sem dependência de UI ou framework.

Estas funções representam regras do domínio (como interpretar seleção de
páginas, como gerar paths seguros) e podem ser reutilizadas por qualquer
camada da aplicação ou por outros projetos Corvus Labs.
"""
from __future__ import annotations

import os


def parse_pages(s: str, total: int) -> list[int]:
    """Converte uma string de seleção de páginas em lista de índices (0-based).

    Sintaxe aceita: '1-3, 5, 7-9' (igual ao diálogo de impressão do Windows).
    String vazia retorna todas as páginas.

    Args:
        s: string de seleção (ex: '1-3, 5').
        total: total de páginas do documento.

    Returns:
        Lista ordenada de índices 0-based.
    """
    if not s.strip():
        return list(range(total))
    pages: set[int] = set()
    for part in s.replace(';', ',').split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                pages.update(range(max(1, int(a)) - 1, min(total, int(b))))
            except ValueError:
                pass
        else:
            try:
                n = int(part)
                if 1 <= n <= total:
                    pages.add(n - 1)
            except ValueError:
                pass
    return sorted(pages)


def safe_path(folder: str, base: str) -> str:
    """Gera um caminho de arquivo que não sobrescreve arquivos existentes.

    Se 'resultado.pdf' já existe, retorna 'resultado (1).pdf', e assim por diante.

    Args:
        folder: pasta de destino.
        base: nome base do arquivo sem extensão.

    Returns:
        Caminho completo seguro para criação do arquivo.
    """
    p = os.path.join(folder, base + '.pdf')
    if not os.path.exists(p):
        return p
    i = 1
    while True:
        p = os.path.join(folder, f'{base} ({i}).pdf')
        if not os.path.exists(p):
            return p
        i += 1
