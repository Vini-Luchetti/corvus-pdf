import os
import sys
from pypdf import PdfReader, PdfWriter

def juntar_pdfs(arquivos_entrada, arquivo_saida="PDF_Mesclado.pdf"):
    """Junta dois ou mais arquivos PDF usando o PdfWriter moderno."""
    writer = PdfWriter()
    print(f"-> Iniciando a mesclagem de {len(arquivos_entrada)} arquivos...")
    
    for pdf in arquivos_entrada:
        if os.path.exists(pdf) and pdf.lower().endswith('.pdf'):
            print(f"Adicionando: {os.path.basename(pdf)}")
            # O PdfWriter moderno consegue ler e anexar o arquivo direto
            writer.append(pdf)
        else:
            print(f"Aviso: Arquivo inválido ou não encontrado: {pdf}")
            
    # Define o caminho de saída na mesma pasta do primeiro PDF arrastado
    pasta_saida = os.path.dirname(os.path.abspath(arquivos_entrada[0]))
    caminho_final = os.path.join(pasta_saida, arquivo_saida)
    
    with open(caminho_final, "wb") as f_saida:
        writer.write(f_saida)
        
    writer.close()
    print(f"==> Sucesso! Arquivo salvo como: {caminho_final}\n")

def separar_pdf(arquivo_entrada):
    """Separa todas as páginas de um PDF em arquivos individuais."""
    if not os.path.exists(arquivo_entrada) or not arquivo_entrada.lower().endswith('.pdf'):
        print("Erro: Arquivo de entrada inválido.")
        return
        
    print(f"-> Iniciando a separação do arquivo: {os.path.basename(arquivo_entrada)}")
    reader = PdfReader(arquivo_entrada)
    nome_base = os.path.splitext(os.path.basename(arquivo_entrada))[0]
    diretorio_saida = os.path.dirname(os.path.abspath(arquivo_entrada))
    
    for i, pagina in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(pagina)
        
        nome_pagina = f"{nome_base}_pagina_{i+1}.pdf"
        caminho_saida = os.path.join(diretorio_saida, nome_pagina)
        
        with open(caminho_saida, "wb") as f_saida:
            writer.write(f_saida)
        writer.close()
        print(f"Gerado: {nome_pagina}")
        
    print(f"==> Sucesso! {len(reader.pages)} páginas extraídas na mesma pasta.\n")

if __name__ == "__main__":
    argumentos = sys.argv[1:]
    
    if not argumentos:
        print("Erro: Nenhum arquivo foi arrastado para o script.")
        print("Modo de uso: Selecione os PDFs e arraste para cima do arquivo .bat")
        os.system("pause")
        sys.exit(1)
        
    if len(argumentos) == 1:
        separar_pdf(argumentos[0])
    else:
        juntar_pdfs(argumentos)