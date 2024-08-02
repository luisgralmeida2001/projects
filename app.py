import os
from pdf2image import convert_from_path

#Diretório dos downloads
pasta = r'C:\Users\luis.almeida\Downloads'
pdf_filename = 'Tradener'

#Procura os arquivos com "Tradener" na pasta de downloads
files = [f for f in os.listdir(pasta) if f.startswith(pdf_filename) and f.endswith('.pdf')]

if files:
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(pasta, f)))
    caminho_completo = os.path.join(pasta, latest_file)
    print(f'O arquivo "{pdf_filename}" mais recente é "{latest_file}".')

    poppler_path = r'C:/Users/luis.almeida/Documents/poppler-23.11.0/Library/bin'

    images = convert_from_path(caminho_completo, 100, poppler_path=poppler_path)

    for i, image in enumerate(images):
        image.save(f'Tradener_page_{i + 1}.jpg', 'JPEG')

    print(f'O PDF "{latest_file}" foi convertido para imagens')
else:
    print(f'Nenhum arquivo encontrado')