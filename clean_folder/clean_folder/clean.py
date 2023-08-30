import shutil
import sys
from pathlib import Path
import re

path = sys.argv[1]
arg = Path(path)

RUSSIAN_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "jo", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ji", "", "a" , "ju", "ja")

TRANS = {}

for key, value in zip(RUSSIAN_SYMBOLS, TRANSLATION) :
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name) :
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W','_', new_name)
    return f"{new_name}.{'.'.join(extension)}"


jpeg_files = list()
png_files = list()
jpg_files = list()
txt_files = list()
docx_files = list()
folders = list()
archives = list()
others = list()
unknown = list()
extensions = list()

registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": png_files,
    "JPG": jpg_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "ZIP": archives,
    "FOLDERS": folders,
    "UNKNOWN EXTENSIONS": unknown,
    "OTHER FILES": others,
    "KNOWN EXTENSIONS": extensions
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(root_folder) :
    for file in root_folder.iterdir() :
        if file.is_dir() :
            folders.append(file.name)
            scan(file)

        else :
            extension = get_extensions(file)
            file_preffix = str(root_folder.parent)
            file_name = str(root_folder/file.name)
            if not extension :
                others.append(file_name.removeprefix(file_preffix))
            elif extension not in extensions :
                extensions.append(extension)
                try :
                    container = registered_extensions[extension]
                    container.append(file_name.removeprefix(file_preffix))
                except KeyError :
                    unknown.append(extension)
                    others.append(file_name.removeprefix(file_preffix))




def write_info(root_folder) :
    test_file = root_folder/'ScanInfo'
    with open(str(test_file),'w+') as fh :
        for key, value in registered_extensions.items() :
            fh.write(f'{key} : {value}\n')


''' List of extensions'''

images = ['.JPEG', '.PNG', '.JPG', '.SVG']
videos = ['.AVI', '.MP4', '.MOV', '.MKV']
docs = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
music = ['.MP3', '.OGG', '.WAV', '.AMR']
archives = ['.ZIP', '.GZ', '.TAR']
FOLDERS = ['IMAGES','VIDEOS', 'DOCS', 'MUSIC', 'ARCHIVES', 'UNKNOWN', 'UNPACKED']



def handle(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))




def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    new_path = path.replace(target_folder / normalize(path.name))
    unpack(new_path, target_folder)


def unpack(new_path, archives_folder):
    dist = new_path.name + '_unpacked'
    unpack_folder = archives_folder/dist
    unpack_folder.mkdir(exist_ok=True)
    shutil.unpack_archive(str(new_path.resolve()), str(unpack_folder.resolve()))






def remove_empty_folders(folder_path):
    for folder in folder_path.iterdir() :
        if folder.is_dir() :
            remove_empty_folders(folder)
            try :
                folder.rmdir()
            except OSError :
                pass








def clean(folder_path):

    for iter_file in folder_path.iterdir() :
        if iter_file.is_dir() :
            if iter_file.name in FOLDERS :
                continue
            clean(iter_file)
        else :
            if iter_file.suffix.upper() in images:
                handle(iter_file,arg.resolve() ,'IMAGES')

            elif iter_file.suffix.upper() in videos:
                handle(iter_file, arg.resolve(), 'VIDEOS')

            elif iter_file.suffix.upper() in docs:
                handle(iter_file, arg.resolve(), 'DOCS')

            elif iter_file.suffix.upper() in music:
                handle(iter_file, arg.resolve(), 'MUSIC')

            elif iter_file.suffix.upper() in archives:
                handle_archive(iter_file, arg.resolve(),'ARCHIVES')


            else :
                handle(iter_file, arg.resolve() , 'UNKNOWN')

    remove_empty_folders(folder_path)



def main():

    print(f"Start in {path}")

    clean(arg.resolve())
    scan(arg.resolve())
    write_info(arg.resolve())
    print("Sorting finished successfully")





if __name__ == '__main__':
   main()
