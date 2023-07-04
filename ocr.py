import argparse
import pytesseract
import sys
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extrair_texto_do_pdf(caminho_pdf):
    try:
        # Converter PDF em imagens
        imagens = convert_from_path(caminho_pdf)

        # Extrair texto de cada imagem
        texto = ""
        for imagem in imagens:
            # Converter imagem para escala de cinza
            imagem = imagem.convert('L')

            # Utilizar o Tesseract OCR para extrair o texto da imagem
            texto_extraido = pytesseract.image_to_string(imagem)
            texto += texto_extraido + "\n"

        return texto
    except Exception as e:
        print(f"[ERRO] Ao extrair o texto do PDF: {str(e)}")


# Verificar se o pytesseract está instalado
try:
    pytesseract.get_tesseract_version()
except pytesseract.TesseractNotFoundError:
    print("[ERRO] O pytesseract não está instalado no local especificado.")
    sys.exit()

# Criar um analisador de argumentos
parser = argparse.ArgumentParser(description='Extrair texto de um arquivo PDF usando OCR Tesseract')

# Adicionar o argumento do caminho do arquivo PDF
parser.add_argument('arquivo_pdf', type=str, help='Caminho para o arquivo PDF')

# Analisar os argumentos
try:
    args = parser.parse_args()
except SystemExit as e:
    print(f"\n[ERRO] Arquivo de entrada inválido ou vazio. Exceção: {str(e)}")
    sys.exit()
except Exception as e:
    print(f"\n[ERRO] Arquivo de entrada inválido ou vazio. Exceção: {str(e)}")

# Extrair texto do PDF
texto_extraido = extrair_texto_do_pdf(args.arquivo_pdf)

# Imprimir o texto extraído, se não houver erro
if texto_extraido:
    print(texto_extraido)