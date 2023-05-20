import os  
import sys
import shutil
import re

folder_sort_path = sys.argv[1]

translate_dict = {ord('а'):'a', ord('б'):'b', ord('в'):'v', ord('г'):'g', ord('д'):'d', ord('е'):'e', 
    ord('ё'):'yo', ord('ж'):'zh', ord('з'):'z', ord('и'):'i', ord('й'):'i', ord('к'):'k', ord('л'):'l', 
    ord('м'):'m', ord('н'):'n', ord('о'):'o', ord('п'):'p', ord('р'):'r', ord('с'):'s', ord('т'):'t', 
    ord('у'):'u', ord('ф'):'f', ord('х'):'h', ord('ц'):'c', ord('ч'):'ch', ord('ш'):'sh', ord('щ'):'sch', 
    ord('ъ'):'', ord('ы'):'y', ord('ь'):'', ord('э'):'e', ord('ю'):'u', ord('я'):'ya', ord('А'):'A', 
    ord('Б'):'B', ord('В'):'V', ord('Г'):'G', ord('Д'):'D', ord('Е'):'E', ord('Ё'):'YO', ord('Ж'):'ZH', 
    ord('З'):'Z', ord('И'):'I', ord('Й'):'I', ord('К'):'K', ord('Л'):'L', ord('М'):'M', ord('Н'):'N',
    ord('О'):'O', ord('П'):'P', ord('Р'):'R', ord('С'):'S', ord('Т'):'T', ord('У'):'U', ord('Ф'):'F', 
    ord('Х'):'H', ord('Ц'):'C', ord('Ч'):'CH', ord('Ш'):'SH', ord('Щ'):'SCH', ord('Ъ'):'', ord('Ы'):'y', 
    ord('Ь'):'', ord('Э'):'E', ord('Ю'):'U', ord('Я'):'YA', ord('ґ'):'', ord('ї'):'', ord('є'):'', 
    ord('Ґ'):'g', ord('Ї'):'i', ord('Є'):'e', ord(' '):'_'}

# Список Папок та розшинень може оновлятись
folders_list = {
    "Images":['.jpeg', '.png', '.jpg', '.svg'],
    "Documents":['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx','.rtf'],
    "Audio":['.mp3', '.ogg', '.wav', '.amr'],
    "Video":['.avi', '.mp4', '.mov', '.mkv'],
    "Archives":['.zip', '.gz', '.tar'],
    "Exe":['.exe'],
    "Python":['.py'],
    "Html_css":['.html', '.css'],
    "Other":[]
}

# Якщо користувач ввів неправильний шлях
def new_path():
    global folder_sort_path
    folder_sort_path = input("Введіть будь ласка коректний шлях --->>>")
    main()

# Рекурсивно обходить усі папки, та переміщає всі файли в материнську папку.
def check_in_folders(path_f):
    try:
        for el in os.listdir(path_f):
            audit = os.path.isdir(os.path.join(path_f, el))
            print(el, audit)
            if audit:
                check_in_folders(os.path.join(path_f, el))
            else:
                os.replace(os.path.join(path_f, el), os.path.join(folder_sort_path, el))
    except FileNotFoundError:
        print(f"Шлях --> {path_f} <-- не є вірним")
        new_path()
        
# Замінює кириліцю на латиницю
def normalize(text):
    normal_text = text.translate(translate_dict)
    normal_text = re.sub(r"[^a-zA-Z0-9]", "_", normal_text)
    return normal_text

# Розбиває файл на filename та .txt, потім замінює кирилицю, та переменовує файл.
def fiks():
    for filename in os.listdir(folder_sort_path):
            name, form = os.path.splitext(filename)
            new_name = normalize(name)
            if not filename[0] == new_name:
                try:
                    if os.path.isdir(filename):
                        os.rename(os.path.join(folder_sort_path, filename[0], folder_sort_path, new_name))
                    else:
                        os.rename(os.path.join(folder_sort_path, filename), os.path.join(folder_sort_path, (new_name + form)))
                except FileExistsError:
                    pass
                except FileNotFoundError:
                    pass

# Створює папки в які будуть сортуватися файли 
def create_folder(folders_list):
    try:
        for name in folders_list:
            os.makedirs(os.path.join(folder_sort_path, name))
    except FileExistsError:
        pass

# Сортирує файли за .txt, по підходящим папкам.
def sorter_files():
    for filename in os.listdir(folder_sort_path):
        if __file__ == os.path.join(folder_sort_path, filename):
            continue
        elif os.path.isfile(os.path.join(folder_sort_path, filename)):
            _, form = os.path.splitext(filename)
            for keys, list_suffix in folders_list.items():
                for suffix in list_suffix:
                    try:
                        if form == '.zip' or form == '.gz' or form == '.tar':
                            q = os.path.join(folder_sort_path, filename)
                            b = os.path.join(folder_sort_path, "Archives", _)
                            arx = os.path.join(folder_sort_path, filename)
                            shutil.unpack_archive(q, b)
                            os.remove(arx)
                            continue
                        elif str(form) == str(suffix):
                            f = os.path.join(folder_sort_path, filename)
                            v = os.path.join(folder_sort_path, keys, filename)
                            shutil.move(f, v)
                            sorter_files()
                    except FileNotFoundError:
                        pass
                    except shutil.ReadError:
                        pass
                    except FileExistsError:
                        pass
    return len(os.listdir(folder_sort_path))

# Якщо залишилися файли с невідомим розщиренням всі вони будут переміщені в папку "Other"
def sorter_Other():
    print(folder_sort_path)
    print(os.listdir(folder_sort_path))
    for filename in os.listdir(folder_sort_path):
        if __file__ == os.path.join(folder_sort_path, filename):
            continue
        _, form = os.path.splitext(filename)
        print(_, form)
        if form:
            shutil.move(os.path.join(folder_sort_path, "Other", filename), os.path.join(folder_sort_path, "Other", filename))
        else:
            pass

# Видаляємо порожні папки
def remove_empty_directories(root_directory):
    for dirpath, dirnames, _ in os.walk(root_directory, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            print(os.listdir(folder_path))
            if not os.listdir(folder_path):  # Перевіряємо, чи папка порожня
                print(f"Видаляємо {folder_path}")
                os.rmdir(folder_path)

# Рекульсивно обходить усі папки та показує всі файли в  красиво в консоль.
def check_in_folder_contents(folder_sort_path):
    for el in os.listdir(folder_sort_path):
        audit = os.path.isdir(os.path.join(folder_sort_path, el))
        try:
            if audit:
                print("{:^100}".format("|" + "_"*100 + "|"))
                print("|{:^100}|".format(f" Folder - {el}"))
                print("{:^100}".format("|" + "_"*100 + "|"))
            else:
                print("|{:^100}|".format(el))
            os.path.join(folder_sort_path, el)
            if audit:
                check_in_folder_contents(os.path.join(folder_sort_path, el))
        except UnicodeEncodeError:
            pass

def no_extensions_are_knownos(path_ext):
        ext = set()
        for el in os.listdir(path_ext):
            _, form = os.path.splitext(el)
            ext.add(form)
        return ext

# Функція яка відповідає за порядок та логіку виконання сортування.
def main():               
    check_in_folders(folder_sort_path)
    fiks()
    create_folder(folders_list)
    s = sorter_files()
    if s > len(folders_list):
        sorter_Other()
    remove_empty_directories(folder_sort_path)
    check_in_folder_contents(folder_sort_path)
    ext = no_extensions_are_knownos(os.path.join(folder_sort_path,"Other"))
    if len(ext) >= 1:
        print("{:^100}".format("|" + "_"*100 + "|"))
        print("|{:^100}|".format(f"Невідомі розширення {ext}"))
        print("|{:^100}|".format(f"Розширте список відомих розширень"))
        print("{:^100}".format("|" + "_"*100 + "|"))
        
if __name__ == "__main__":
    main()
