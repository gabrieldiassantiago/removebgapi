import requests
import PySimpleGUI as sg
import io
from PIL import Image
from io import BytesIO

api_key = 'Y8FFoQJxStbPFCk4XipwTbS3'
url = 'https://api.remove.bg/v1.0/removebg'

def remove_background(api_key, image_path):
    try:
        if image_path.startswith(('http://', 'https://')):
            # Se a imagem for uma URL, faz uma solicitação GET para obter a imagem
            response = requests.get(image_path)
            response.raise_for_status()  # Lança uma exceção em caso de erro HTTP
            image_bytes = BytesIO(response.content)
        else:
            # Se a imagem for local, lê o arquivo
            image_bytes = open(image_path, 'rb')

        # Faz a solicitação POST para remover o fundo
        response = requests.post(
            url,
            files={'image_file': image_bytes},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )

        if response.status_code == requests.codes.ok:
            # Exibe a imagem removida na tela
            img = Image.open(io.BytesIO(response.content))
            img.show()

            # Pede ao usuário para salvar a imagem
            save_path = sg.popup_get_file('Salvar Imagem Como', file_types=(("PNG files", "*.png"), ("All files", "*.*")),
                                          default_extension=".png")
            if save_path:
                img.save(save_path)
                print(f"Imagem salva em {save_path}")
            else:
                print("A imagem não foi salva.")
        else:
            print("Erro:", response.status_code, response.text)
    except Exception as e:
        print("Ocorreu um erro:", e)
    finally:
        if 'image_bytes' in locals():
            image_bytes.close()  # Fecha o arquivo ou o objeto BytesIO

# Layout da interface gráfica
layout = [
    [sg.Text('Selecione a imagem para remover o fundo:')],
    [sg.InputText(key='image_path', size=(30, 1)), sg.FileBrowse()],
    [sg.Text('OU')],
    [sg.Text('Informe a URL da imagem:')],
    [sg.InputText(key='url_path', size=(30, 1))],
    [sg.Button('Remover Fundo'), sg.Button('Sair')],
]

window = sg.Window('Removedor de Fundo', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break
    elif event == 'Remover Fundo':
        image_path = values['image_path']
        url_path = values['url_path']
        if image_path:
            remove_background(api_key, image_path)
        elif url_path:
            remove_background(api_key, url_path)
        else:
            print("Por favor, selecione uma imagem ou informe uma URL.")

window.close()
