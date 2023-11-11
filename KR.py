import piexif as piexif
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image
from PIL.ExifTags import TAGS
import os
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)
        self.setGeometry(300, 300, 500, 300)
        self.initUI()
        self.inverseTAGS = {value: key for key, value in TAGS.items()}

    def initUI(self):
        # Создаем кнопку для выбора изображения
        self.btn_select = QPushButton("Выбрать изображение", self)
        self.btn_select.setFont(QFont("Mono", 8))
        self.btn_select.adjustSize()
        self.btn_select.move(175, 30)
        self.btn_select.clicked.connect(self.selectImage)

    def selectImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.jpg *.png)")
        self.file_name = file_name
        self.name = os.path.basename(self.file_name)[:-4]
        if not self.file_name:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать изображение!")
            return
        self.showMetadata()


def window():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    window()
