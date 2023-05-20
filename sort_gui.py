import sys
import os 
import shutil
import re

from PyQt5 import QtCore, QtGui, QtWidgets

folder_sort_path  = "" #sys.argv[1]

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
    folder_sort_path = input("Введіть будласка коректний шлях")
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
        print(f"Шлях {path_f} не є вірним")
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
    remove_empty_directories(folder_sort_path)
    create_folder(folders_list)
    s = sorter_files()
    if s > len(folders_list):
        sorter_Other()
    
    check_in_folder_contents(folder_sort_path)
    ext = no_extensions_are_knownos(os.path.join(folder_sort_path,"Other"))
    
    if len(ext) >= 1:
        print("{:^100}".format("|" + "_"*100 + "|"))
        print("|{:^100}|".format(f"Невідомі розширення {ext}"))
        print("|{:^100}|".format(f"Розширте список відомих розширень"))
        print("{:^100}".format("|" + "_"*100 + "|"))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(445, 220)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(81, 0, 135, 255), stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(155, 79, 165, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color:rgba(255,255,255,30);\n"
"border: 1px solid rgba(255,255,255,40);\n"
"border-radius:7px;")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setStyleSheet("font-size: 24pt;\n"
"font: 20pt \"Comic Sans MS\";\n"
"color: white;")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton.setStyleSheet("QPushButton { \n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255,255,255,40);\n"
"border-bottom-right-radius: 7px;\n"
"border-bottom-left-radius: 7px; \n"
"color: white;\n"
"font-size: 24pt;\n"
"font: 22pt \"Comic Sans MS\";\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgba(255, 255, 255, 50); \n"
"border: 1px solid rgba(255,255,255,90);\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: rgba(255, 255, 255, 70); \n"
"border: 1px solid rgba(255,255,255,60);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 1)
        self.input_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.input_bar.setObjectName("input_bar")    # <--------
        self.gridLayout.addWidget(self.input_bar, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStyleSheet("QPushButton { \n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255,255,255,40);\n"
"border-bottom-right-radius: 7px;\n"
"border-bottom-left-radius: 7px; \n"
"color: white;\n"
"font-size: 24pt;\n"
"font: 16pt \"Comic Sans MS\";\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgba(255, 255, 255, 50); \n"
"border: 1px solid rgba(255,255,255,90);\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: rgba(255, 255, 255, 70); \n"
"border: 1px solid rgba(255,255,255,60);\n"
"}")
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox") # <--------
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.label_2.raise_()
        self.pushButton.raise_()
        self.input_bar.raise_()
        self.buttonBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_function()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sorting files"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Path to sorting</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "---> Sort <---"))
        
    def add_function(self):
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)
        self.pushButton.clicked.connect(lambda: self.input_uzer(self.pushButton.text()))

    def on_accept(self):
        global folder_sort_path
        folder_sort_path = self.input_bar.text()
        
    def on_reject(self):
        global folder_sort_path
        folder_sort_path = None
        self.input_bar.clear()
        
    def input_uzer(self, input_uzer_path):
        print(input_uzer_path)
        try:
            if input_uzer_path == "---> Sort <---":
                if folder_sort_path != "":
                    main()
        except TypeError:
            pass
        except FileNotFoundError:
            pass
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
