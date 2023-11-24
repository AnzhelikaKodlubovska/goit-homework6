import os
import shutil
import sys

def normalize(name):
    kirilic_dict = {
        'а': 'a','А': 'A','б': 'b','Б': 'B','в': 'v','В': 'V','г': 'h','Г': 'H','ґ': 'g','Ґ': 'G',
        'д': 'd','Д': 'D','е': 'e','Е': 'E','є': 'ie','Є': 'Ye','ж': 'zh','Ж': 'Zh','з': 'z','З': 'Z',
        'и': 'y','И': 'Y','і': 'i','І': 'I','ї': 'i','Ї': 'Yi','й': 'i','Й': 'Y','к': 'k','К': 'K',
        'л': 'l','Л': 'L','м': 'm','М': 'M','н': 'n','Н': 'N','о': 'o','О': 'O','п': 'p','П': 'P',
        'р': 'r','Р': 'R','с': 's','С': 'S','т': 't','Т': 'T','у': 'u','У': 'U','ф': 'f','Ф': 'F',
        'х': 'kh','Х': 'Kh','ц': 'ts','Ц': 'Ts','ч': 'ch','Ч': 'Ch','ш': 'sh','Ш': 'Sh','щ': 'shch',
        'Щ': 'Shch','ь': '','Ь': '','ю': 'iu','Ю': 'Yu','я': 'ia','Я': 'Ya'
    }
    name_without_extension, extension = os.path.splitext(name)
    new_name = ''
    for char in name_without_extension:
        if char.isalpha() and char.lower() in kirilic_dict:
            if char.isupper():
                new_name += kirilic_dict[char.lower()].upper()
            else:
                new_name += kirilic_dict[char]
        elif char.isalnum():
            new_name += char
        else:
            new_name += '_'
    return f"{new_name}{extension}"

def process_folder(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file not in ('Video', 'Docs', 'Music', 'Archives', 'Unfounded'):
                normalized_name = normalize(file)
                ext = os.path.splitext(file)[1][1:].upper()
                if ext in ('JPG', 'PNG', 'JPEG', 'SVG'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Pictures', normalize(normalized_name)))
                elif ext in ('AVI', 'MP4', 'MOV', 'MKV'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Video', normalize(normalized_name)))
                elif ext in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Docs', normalize(normalized_name)))
                elif ext in ('MP3', 'OGG', 'WAV', 'AMR'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Music', normalize(normalized_name)))
                elif ext in ('ZIP', 'GZ', 'TAR'):
                    shutil.unpack_archive(os.path.join(root, file), os.path.join(path, 'Archives', os.path.splitext(normalized_name)[0]))
                    os.remove(os.path.join(root, file))
                else:
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Unfounded', normalize(normalized_name)))
        for folder in dirs:
            full_folder_path = os.path.join(root, folder)
            try:
                os.rmdir(full_folder_path)
            except OSError:
                pass  # Папка не пуста или не существует

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)
    
    path = sys.argv[1]
    process_folder(path)

if __name__ == "__main__":
    main()
