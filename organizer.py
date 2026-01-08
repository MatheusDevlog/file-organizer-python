"""
File Organizer in Python
Autor: Matheus Santos
Descrição: Organiza arquivos por extensão ou data, com proteção contra sobrescrita.
"""


import os
import shutil
from datetime import datetime
from tkinter import Tk, filedialog

def create_default_extension_map():
    return {
        'Imagens': ['.jpg', '.png','.avif','.jpeg','.gif'],
        'Videos': ['.mov','.mp4','.log','.mkv','.flv'],
        'Documentos': ['.pdf','.doc','.docx','.txt','.ppt','.pptx','.xls','.xlsx'],
        'Musicas': ['.mp3','.wav'],
        'Design': ['.af','.psd','.cdr','.ai'],
        'Arquivos': ['.zip','.rar','.7z'],
        'Codigos': ['.py','.html','.js','.css'],
        'Outros' : [],
    }

def get_folder_for_extensions(extension, extension_map):
    for folder, extensions in extension_map.items():
        if extension in extensions:
            return folder
        
    return 'Outros'

def get_unique_filename(folder_path, file_name):
    name, extension = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name

    while os.path.exists(os.path.join(folder_path, new_file_name)):
        new_file_name = f'{name} ({counter}){extension}'
        counter += 1

    return new_file_name

def move_file(file_path, folder_name, directory):
    folder_path = os.path.join (directory, folder_name)
    os.makedirs (folder_path, exist_ok=True)

    file_name = os.path.basename(file_path)
    unique_file_name = get_unique_filename(folder_path, file_name)
    new_path = os.path.join(folder_path, unique_file_name)
    shutil.move(file_path, new_path)
    print(f'Movido {file_name} para {folder_path}')

    return new_path

def organize_by_extension(directory):
    extension_map = create_default_extension_map()
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            extension = os.path.splitext(file_path)[1].lower()
            folder_name = get_folder_for_extensions(extension, extension_map)
            move_file(file_path, folder_name, directory)

def organize_by_date(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            created_at = datetime.fromtimestamp(os.path.getmtime(file_path))
            folder_name = created_at.strftime ('%y-%m-%d')
            move_file(file_path, folder_name, directory)

def main():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title= 'Selecionar diretorio:')
    if not directory:
        print('O diretorio selecionado não existe')
        return
    
    while True:
        print('\n --- ORGANIZADOR DE ARQUIVOS ---')
        print('1 - Organizar por tipo de arquivo')
        print('2 - Organizar por data')
        print('3 - Sair')

        choice = input('Escolha uma opção [1 - 3]: ')
        if choice == '1':
            organize_by_extension(directory)
        elif choice == '2':
            organize_by_date(directory)
        elif choice == '3':
            break
        else:
            print('Opção Invalida! Tente novamente')

if __name__ == '__main__':
    main()    
