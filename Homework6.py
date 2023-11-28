import sys
from pathlib import Path
import shutil
from transliterate import translit

images = '.jpg .png .jpeg .svg'.split()
video = '.avi .mp4 .mov .mkv'.split()
documents = '.doc .docx .txt .pdf .xlsx .pptx'.split()
audio = '.mp3 .ogg .wav .amr'.split()
archives = '.zip .gz .tar'.split()

dict_suf = {'images': images,
            'video': video,
            'documents': documents,
            'audio': audio,
            'archives': archives,
            'other': []
}

dict_suf_reversed = {}
for key, value in dict_suf.items():
    dict_suf_reversed.update(dict.fromkeys(value, key))
    dict.fromkeys(value, key)


def normalize(name: str):
    translit_name = translit(name, 'uk', reversed=True)
    normalized_name = ''.join(el if el.isalnum() else '_' for el in translit_name)
    return normalized_name


def unpack_archive(root_path, file_path):
    try:
        unpack_folder = root_path / file_path.stem
        shutil.unpack_archive(str(file_path), str(unpack_folder))
    except Exception as e:
        print(f"Extraction failed for '{file_path}': {e}")
        file_path.unlink()
    
    
def move(root_path: Path,path: Path): 
    file_suffix = path.suffix
    file_name = path.stem
    kategory = dict_suf_reversed.get(file_suffix.lower(), 'other')
    new_path = root_path / kategory
    if not new_path.exists():
        new_path.mkdir()
    new_file_name = normalize(file_name) + file_suffix
    path.replace(new_path / new_file_name)
    
    
def sorted_files(root_path, path):
   for el in path.iterdir():
       if el.is_file():
           move(root_path, el)
       elif el.is_dir():
           if el.parts[-1] in dict_suf and el.parts[:-1] == root_path.parts:
               continue
           sorted_files(root_path, el)
           el.rmdir()
                     
           
def main():
   path = Path(sys.argv[1]) 
   sorted_files(path, path)
   
    
if __name__ == '__main__':
    main()