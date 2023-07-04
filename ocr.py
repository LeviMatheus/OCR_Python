import argparse
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extrair_texto_do_pdf(caminho_pdf, inicio=0, fim=None):
    try:
        # Converter PDF em imagens
        imagens = convert_from_path(caminho_pdf)

        # Verificar se o fim é maior que o número total de páginas
        if fim is None or fim > len(imagens):
            fim = len(imagens)

        # Extrair texto de cada imagem no intervalo especificado
        texto = ""
        for i, imagem in enumerate(imagens[inicio:fim], start=inicio+1):
            # Converter imagem para escala de cinza
            imagem = imagem.convert('L')

            # Utilizar o Tesseract OCR para extrair o texto da imagem
            texto_extraido = pytesseract.image_to_string(imagem)
            texto += f"=== Página {i} ===\n"
            texto += texto_extraido + "\n"

        return texto
    except Exception as e:
        print(f"[ERRO] Ao extrair o texto do PDF: {str(e)}")


# Criar um analisador de argumentos
parser = argparse.ArgumentParser(description='Extrair texto de um arquivo PDF usando OCR Tesseract')

# Adicionar o argumento do caminho do arquivo PDF
parser.add_argument('arquivo_pdf', type=str, help='Caminho para o arquivo PDF')

# Adicionar os argumentos de intervalo de páginas
parser.add_argument('--inicio', type=int, default=0, help='Página inicial (padrão: 0)')
parser.add_argument('--fim', type=int, help='Página final')

# Adicionar o argumento de padrão regex
parser.add_argument('--padrao', type=str, help='Padrão regex a ser verificado')

# Analisar os argumentos
args = parser.parse_args()

# Extrair texto do PDF com base no intervalo de páginas especificado
texto_extraido = extrair_texto_do_pdf(args.arquivo_pdf, args.inicio, args.fim)

# Verificar se o padrão de entrada existe no texto do PDF
if texto_extraido and args.padrao:
    matches = re.findall(args.padrao, texto_extraido)
    if matches:
        for index,match in enumerate(matches):
            print(f"Correspondência ({index}) encontrada: {match}")
    else:
        print("Nenhuma correspondência encontrada para o padrão especificado.")
else:
    print(texto_extraido)