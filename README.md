<div align="center">

```
█▀▀ █▀█ █▀█ █░█ █░█ █▀   █▀█ █▀▄ █▀▀
█▄▄ █▄█ █▀▄ ▀▄▀ █▄█ ▄█   █▀▀ █▄▀ █▀░
```

**PDF tool with amber CRT terminal interface**

[![Python](https://img.shields.io/badge/Python-3.10%2B-ffaa33?style=flat-square&logo=python&logoColor=ffaa33&labelColor=0a0602)](https://python.org)
[![pypdf](https://img.shields.io/badge/pypdf-4.0%2B-994400?style=flat-square&labelColor=0a0602)](https://pypdf.readthedocs.io)
[![License](https://img.shields.io/badge/license-MIT-662A00?style=flat-square&labelColor=0a0602)](LICENSE)
[![Corvus Labs](https://img.shields.io/badge/Corvus_Labs-geralzona.com-ffaa33?style=flat-square&labelColor=0a0602)](https://geralzona.com)

</div>

---

## O que faz

Duas operações. Sem complicação.

**MESCLAR** — Adiciona N arquivos PDF à lista, define quais páginas de cada um entram (ou deixa em branco pra usar todas), escolhe a pasta e o nome do arquivo de saída. Gera 1 PDF.

**SEPARAR** — Abre um ou mais PDFs e separa em arquivos individuais: uma página por arquivo, ou você define ranges específicos (cada range vira um arquivo separado).

Sintaxe de páginas igual ao Windows ao imprimir: `1-3 OU 1;3 OU 5,9 OU 5-9`

Selecione o nome do arquivo de saída. Se gerar mais de um arquivo o nome utilizado para a saída tera mumeros sequenciais ao final do nome, na mesma ordem da divisão.

---

## Download

**→ [Baixar CorvusPDF.exe](../../releases/latest)** — sem instalação, sem dependências.

Para rodar direto do código, veja [Como usar (código-fonte)](#como-usar-código-fonte) abaixo.

---

## Interface

```
╔══════════════════════════════════════════════╗
║  CORVUS PDF // v1.0    CORVUS LABS           ║
╠══════════════════════════════════════════════╣
║  ▶ MESCLAR  │  SEPARAR                       ║
╠══════════════════════════════════════════════╣
║  // ARQUIVOS · PÁGINAS (vazio = todas)       ║
║  ┌──────────────────────────────────────┐    ║
║  │ 01  contrato.pdf         8p  [1-3,5] │    ║
║  │ 02  ata_reuniao.pdf     12p  [     ] │    ║
║  │ 03  procuracao.pdf       3p  [2    ] │    ║
║  │  + ADICIONAR PDF                     │    ║
║  └──────────────────────────────────────┘    ║
║  // SAÍDA                                    ║
║  [ D:\Documentos\          ] [ PASTA ]       ║
║  NOME: [ resultado.pdf               ]       ║
║  ──────────────────────────────────────      ║
║  → Montando 3 arquivo(s)...                  ║
║  ▶  PROCESSAR                                ║
╚══════════════════════════════════════════════╝
```

---

## Funcionalidades

- Seleção de páginas por arquivo (`1-3 OU 1;3 OU 5,9 OU 5-9` — igual ao Windows)
- Reordenação da lista com ↑ ↓
- Separar todas as páginas (uma por arquivo) ou por ranges definidos
- Seletor de pasta de saída
- Log em tempo real do processamento
- Processamento em thread separada (janela não trava)
- Interface âmbar CRT e intuitíva

---

## Como usar (código-fonte)

**Pré-requisitos:** Python 3.10+ e pip

```bash
# 1. Clone o repositório
git clone https://github.com/Vini-Luchetti/corvus-pdf.git
cd corvus-pdf

# 2. Instale a dependência
pip install pypdf

# 3. Execute
python corvus_pdf.py
```

---

## Como empacotar (.exe)

```bash
# Na pasta do projeto, com Python e pip disponíveis:
build.bat
```

O executável é gerado em `dist\CorvusPDF.exe` e abre automaticamente a pasta.

Ou manualmente:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name CorvusPDF corvus_pdf.py
```

---

## Estrutura

```
corvus-pdf/
├── corvus_pdf.py      # aplicação principal
├── build.bat          # empacotador PyInstaller
├── requirements.txt   # dependências
└── README.md
```

---

## Parte do ecossistema Corvus Labs

| Projeto | Status | Descrição |
|---|---|---|
| **CorvusPDF** | ✅ operacional | Este repositório |
| [CorvusOne](https://geralzona.com) | 🔧 em construção | Assistente local com IA |
| [Clube do Corvo](https://github.com/Vini-Luchetti/Project-Club-Pets) | ✅ operacional | Portal de adoção de pets |

---

<div align="center">

`CONSTRUIR. TESTAR. QUEBRAR. APRENDER. REPETIR.`

**[geralzona.com](https://geralzona.com)** · Corvus Labs

</div>
