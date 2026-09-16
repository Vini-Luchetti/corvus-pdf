# 🐦‍⬛ Corvus PDF

> **Organizar documentos sem transformar uma tarefa simples em uma novela.**

**Corvus PDF 1.0** é uma ferramenta desktop para Windows, construída em Python, para operações práticas com arquivos PDF.

Esta é a **primeira versão pública** do projeto: simples, funcional e organizada para evoluir a partir daqui.

## ✦ O que faz

- **Mesclar PDFs** — combina vários arquivos em um único PDF, com seleção opcional de páginas por arquivo.
- **Separar PDFs** — gera um arquivo por página ou trabalha com ranges específicos.
- **Arrastar e soltar** arquivos PDF.
- **Processamento assíncrono** — operações fora da interface principal para manter a janela responsiva.
- **Interface PySide6** — aplicação desktop em Python/Qt.
- **Sistema de temas** — tokens visuais centralizados e temas alternáveis.
- **Build para Windows** — empacotamento com PyInstaller.

## 🧱 Arquitetura

```text
corvus-pdf/
├── app/
│   ├── core/              # regras utilitárias
│   ├── services/          # operações PDF e workers
│   ├── ui/
│   │   ├── theme/         # temas e design tokens
│   │   ├── views/         # Merge, Split e About
│   │   └── widgets/       # componentes reutilizáveis
│   └── assets/            # identidade visual e ícones
├── main.py
├── requirements.txt
├── CorvusPDF.spec
└── build.bat
```

A lógica de PDF fica separada da interface. Workers baseados em `QThread` executam as operações e comunicam resultados, logs e erros por sinais Qt.

## 🛠️ Stack

- Python
- PySide6
- pypdf
- PyInstaller

## ▶️ Executar localmente

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## 📦 Gerar o executável

No Windows:

```bat
build.bat
```

O executável é gerado em `dist/`. Artefatos de build e executáveis não fazem parte do código-fonte versionado.

## 🧭 Versionamento

A linha pública do projeto começa em **1.0.0**. Iterações anteriores permanecem no histórico do Git, mas não fazem parte da estrutura pública atual.

A regra é simples: **release funcional primeiro; evolução depois**.

## 🔐 Licença

A licença de redistribuição/reutilização ainda não foi definida. O projeto permanece público para acompanhamento e portfólio, sem assumir permissões adicionais que não tenham sido expressamente escolhidas.

---

## Corvus Labs

Um projeto de **GeralZona**, construído por **Vinicius Luchetti** em colaboração com ferramentas de IA.

> **Construir. Testar. Quebrar. Aprender. Repetir.**

[geralzona.com](https://geralzona.com) · [Luchetti Advocacia](https://luchetti.adv.br)