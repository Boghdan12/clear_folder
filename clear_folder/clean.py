import sys
import os
import re
import shutil
from pathlib import Path 


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ARCHIVES = []


REGISTER_EXTENSION = {    
    'JPEG' : JPEG_IMAGES,
    'JPG' : JPG_IMAGES,
    'PNG' : PNG_IMAGES,
    'SVG' : SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}
FOLDERS = []
EXCEPTIONS = set()
UNKNOWN = set()

def get_extansion(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images','MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue 
        
        
        extension = get_extansion(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
               ext_reg = REGISTER_EXTENSION[extension]
               ext_reg.append(full_name)
               EXCEPTIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)
if __name__ == '__main__': 
    folder_procees = sys.argv[1]
    scan(Path(folder_procees))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images png: {PNG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Archives zip: {ARCHIVES}')
    
    print(f'Extension: {EXCEPTIONS}')
    print(f'UNKNOWN: {UNKNOWN}')
    


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic,latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normalize(name: str) -> str:
    name, extension = os.path.splitext(name)
    translated_name = re.sub(r'\W', '_', name.translate(TRANS))
    return f"{translated_name}{extension}"





def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents= True)
    file_name.replace(target_folder / normalize(file_name.name))
    
def handle_document(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents= True)
    file_name.replace(target_folder / normalize(file_name.name))
    
def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents= True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents= True) 
    try:
        shutil.unpack_archive(str(file_name.absolute()),str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
    file_name.unlink()
    

            
def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / ' JPEG')
    
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / ' JPG')
        
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / ' PNG')
        
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / ' SVG')
         
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
        
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in DOC_DOCUMENTS:
        handle_document(file, folder / 'documents' / 'DOC')
    
    for file in DOCX_DOCUMENTS:
        handle_document(file, folder / 'documents' / 'DOCX')
    
    for file in TXT_DOCUMENTS:
        handle_document(file, folder / 'documents' / 'TXT')
    
    for file in PDF_DOCUMENTS:
        handle_document(file, folder / 'documents' / 'PDF')

    for file in XLSX_DOCUMENTS:
        handle_document(file, folder / 'documents' / 'XLSX')

    for file in PPTX_DOCUMENTS:
        handle_document(file, folder / 'documents' / 'PPTX')

    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')

    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')

    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
        
    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')
        
    for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')
        
    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')
        
def start():
    if sys.argv[1]:
    folder_procees = Path(sys.argv[1])
    main(folder_procees)
        