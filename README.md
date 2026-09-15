# 🐦‍⬛ Corvus PDF

> **Organizar documentos sem transformar uma tarefa simples em uma novela.**

**Corvus PDF V6** é uma ferramenta desktop para Windows, construída em Python, para operações práticas com arquivos PDF.

A V6 é o novo **baseline público** do projeto: uma versão funcional, modular e preparada para evoluir sem sacrificar o que já funciona.

## ✦ O que faz

- **Mesclar PDFs** — combina vários arquivos em um único PDF, com seleção opcional de páginas por arquivo.
- **Separar PDFs** — gera um arquivo por página ou trabalha com ranges específicos.
- **Arrastar e soltar** arquivos PDF.
- **Processamento assíncrono** — as operações são executadas fora da interface principal para manter a janela responsiva.
- **Interface PySide6** — aplicação desktop nativa em Python/Qt.
- **Sistema de temas** — tokens visuais centralizados e temas alternáveis.
- **Build para Windows** — empacotamento com PyInstaller.

## 🧱 Arquitetura

```text
CorvusPDF_V5_GUI/          # nome histórico do diretório; projeto: V6
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

A lógica de PDF é mantida separada da interface. Workers baseados em `QThread` executam as operações e comunicam resultado, log e erros por sinais Qt.

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

O executável é gerado em `dist/` — artefatos de build não fazem parte do código-fonte versionado.

## 🧭 Versionamento

O projeto possui histórico anterior preservado no Git. A partir daqui, a nomenclatura pública passa a tratar esta linha como **V6**.

A regra é simples: **release funcional primeiro; evolução visual e experimental depois**. Nem toda experiência de bancada precisa virar uma release pública.

## 🔐 Licença

A licença de redistribuição/reutilização ainda não foi definida. O projeto permanece público para acompanhamento e portfólio, mas não assume permissões adicionais que não tenham sido expressamente escolhidas.

---

## Corvus Labs

Um projeto de **GeralZona**, construído por **Vinicius Luchetti** em colaboração com ferramentas de IA.

> **Construir. Testar. Quebrar. Aprender. Repetir.**

[geralzona.com](https://geralzona.com) · [Luchetti Advocacia](https://luchetti.adv.br)
