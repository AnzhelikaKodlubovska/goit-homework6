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
    
    new_name = ''
    for char in name:
        if char.lower() in kirilic_dict:
            if char.isupper():
                new_name += kirilic_dict[char.lower()].capitalize()
            else:
                new_name += kirilic_dict[char.lower()]
        elif char.isalnum():
            new_name += char
        else:
            new_name += '_'
    return new_name


def process_folder(path):
    script_name = os.path.basename(__file__)
    
    for root, dirs, files in os.walk(path):
        for folder_name in ('Pictures', 'Video', 'Docs', 'Music', 'Archives', 'Unfounded'):
            target_folder_path = os.path.join(path, folder_name)
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)

        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file != script_name and file_extension:
                normalized_name = normalize(file)
                ext = file_extension[1:].upper()
                if ext in ('JPG', 'PNG', 'JPEG', 'SVG'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Pictures', normalize(normalized_name)))
                elif ext in ('AVI', 'MP4', 'MOV', 'MKV'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Video', normalize(normalized_name)))
                elif ext in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Docs', normalize(normalized_name)))
                elif ext in ('MP3', 'OGG', 'WAV', 'AMR','MP3'):
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Music', normalize(normalized_name)))
                elif ext in ('ZIP', 'GZ', 'TAR'):
                    archive_folder = os.path.join(path, 'Archives', os.path.splitext(normalize(normalized_name))[0])
                    shutil.unpack_archive(os.path.join(root, file), archive_folder)
                    for item in os.listdir(archive_folder):
                        new_item_name = f"{os.path.splitext(item)[0]}_{os.path.splitext(normalize(normalized_name))[0]}{os.path.splitext(item)[1]}"
                        os.rename(os.path.join(archive_folder, item), os.path.join(archive_folder, new_item_name))
                    os.remove(os.path.join(root, file))
                    for item in os.listdir(archive_folder):
                        shutil.move(os.path.join(archive_folder, item), os.path.join(path, 'Archives'))
                    os.rmdir(archive_folder)
                else:
                    shutil.move(os.path.join(root, file), os.path.join(path, 'Unfounded', normalize(normalized_name)))
            elif not file_extension:
                print(f"File '{file}' has no extension, skipping...")

    for root, dirs, files in os.walk(path, topdown=False):
        for folder in dirs:
            full_folder_path = os.path.join(root, folder)
            try:
                os.rmdir(full_folder_path)
                print(f"Empty folder '{full_folder_path}' has been removed.")
            except OSError:
                pass 
            

def main():
    if len(sys.argv) < 2:
        print("Usage: python <script_name.py> <folder_path>")
        sys.exit(1)
    
    path = sys.argv[1]
    process_folder(path)

if __name__ == "__main__":
    main()
