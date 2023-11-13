import piexif as piexif
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image
from PIL.ExifTags import TAGS
import os
# Создаем класс главного окна
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Извлечение метаданных из изображения")
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

        # Создаем поле для отображения метаданных
        self.metadata_field = QTextEdit(self)
        self.metadata_field.setGeometry(50, 75, 400, 140)
        self.metadata_field.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Создаем кнопку для удаления метаданных
        self.btn_delete = QPushButton("Удалить один тег", self)
        self.btn_delete.adjustSize()
        self.btn_delete.move(168, 236)

    # Функция для выбора изображения
    def selectImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.jpg *.png)")
        self.file_name = file_name
        self.name = os.path.basename(self.file_name)[:-4]
        if not self.file_name:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать изображение!")
            return
        # Отображаем метаданные о выбранном файле
        self.showMetadata()

    # Функция для отображения метаданных о файле
    def showMetadata(self):
        if self.file_name is None:
            return
        # Открываем изображение с помощью библиотеки Pillow
        image = Image.open(self.file_name)
        # Получаем метаданные с помощью метода getexif()
        exifdata = image._getexif()
        # Проверяем, есть ли метаданные в файле
        if not exifdata:
            self.metadata_field.setText("Файл не содержит метаданных")
            return
        # Создаем строку для отображения метаданных
        metadata_str = "Метаданные файла:\n"
        # Проходимся по всем метаданным и добавляем их к строке
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            metadata_str += f"{tag}: {data}\n"
        # Отображаем строку в поле для метаданных
        self.metadata_field.setText(metadata_str)


# Main function
def window():
    # Создаем экземпляр класса главного окна и запускаем приложение
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    window()
