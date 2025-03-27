import requests
import zipfile
import os
import shutil

# URL dos PDFs
pdf_urls = [
    'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf',
    'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf'
]

os.makedirs('pdfs_temp', exist_ok=True) # Cria uma pasta temporária para salvar os arquivos

pdf_paths = [] # Guarda o caminho dos PDFs

# Realiza o download dos PDFs e depois os escreve em um arquivo
for i, url in enumerate(pdf_urls, start=1): 
    pdf_path = f"pdfs_temp/anexo{i}.pdf"
    response = requests.get(url) # Realiza o download do arquivo PDF
    if response.status_code == 200: 
        with open(pdf_path, "wb") as file: # Vai utilizar a escrita binária para registrar as informações no arquivo
            file.write(response.content)
        pdf_paths.append(pdf_path)
        print(f"Baixado: {pdf_path}")
    else:
        print(f"Erro ao baixar {url}")


zip_filename = 'anexos.zip' # Nome do arquivo ZIP

# Cria o ZIP e coloca os PDFs dentro dele
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf: 
    for pdf in pdf_paths:
        zipf.write(pdf, os.path.basename(pdf))
        print(f'Adicionado ao ZIP: {pdf}')


origin_path = r'C:\dev\Desafios Vagas\Intuitive_Care_Teste\anexos.zip' # Caminho de origem do arquivo ZIP
destination_path = r'C:\dev\Desafios Vagas\Intuitive_Care_Teste\assets\anexos.zip' # Caminho de destino do arquivo ZIP

shutil.move(origin_path, destination_path) # Move o arquivo ZIP para a pasta assets
print(f'Movido para assets: {zip_filename}')
    

for pdf in pdf_paths: # Apaga os PDFs
    os.remove(pdf)

os.rmdir('pdfs_temp') # Apaga a pasta temporária

print(f'ZIP criado: {zip_filename}')