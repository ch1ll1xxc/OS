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
        self.setWindowIcon(QIcon("LOGO.png"))
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
        # Создаем кнопку для экспорта информации
        self.btn_export = QPushButton("Экспорт данных", self)
        self.btn_export.adjustSize()
        self.btn_export.move(50, 236)
        self.btn_export.clicked.connect(self.exportMetadata)

        # Создаем кнопку для удаления метаданных
        self.btn_delete = QPushButton("Удалить один тег", self)
        self.btn_delete.adjustSize()
        self.btn_delete.move(168, 236)
        self.btn_delete.clicked.connect(self.deleteTag)

        # Cоздаем кнопку для удаления всех метаданных
        self.btn_delete_all = QPushButton("Удалить все метаданные", self)
        self.btn_delete_all.adjustSize()
        self.btn_delete_all.move(292, 236)
        self.btn_delete_all.clicked.connect(self.deleteAllMetadata)

        # Создаем кнопку для получения информации о программе
        self.btn_about = QPushButton("О программе", self)
        self.btn_about.setIcon(QIcon("Info_Simple_bw.svg.png"))
        self.btn_about.adjustSize()
        self.btn_about.move(342, 30)
        self.btn_about.clicked.connect(self.showInfo)

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

        # Функция для экспорта информации о метаданных в .txt файл

    def exportMetadata(self):
        # Получаем текст из поля с метаданными
        metadata = self.metadata_field.toPlainText()
        if metadata == "" or metadata == "Файл не содержит метаданных":
            QMessageBox.warning(self, "Ошибка", "Нет информации, подлежащей экспорту")
            return
        # Открываем диалоговое окно для выбора директории
        save_path = QFileDialog.getExistingDirectory(self, 'Выбрать директорию')
        if not save_path:
            QMessageBox.warning(self, "Ошибка", "Директория не выбрана!")
            return
        # Создаем файл с расширением .txt в выбранной директории
        file = open(os.path.join(save_path, "metadata.txt"), "w")
        # Записываем в файл информацию о метаданных
        file.write(metadata)
        file.close()
        QMessageBox.information(self, "Экспорт данных", "Информация о метаданных успешно экспортирована")

    def deleteTag(self):
        # Получаем текст из поля с метаданными
        metadata = self.metadata_field.toPlainText()
        if metadata == "" or metadata == "Файл не содержит метаданных":
            QMessageBox.warning(self, "Ошибка", "Удаление запрещено")
            return
        if not self.file_name:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать изображение!")
            return
        tag_to_delete, ok = QInputDialog.getText(self, "Удаление метаданных", "Введите тег, который нужно удалить")
        if not ok:
            # Выводим сообщение об ошибке
            QMessageBox.warning(self, "Ошибка", "Невозможно удалить метаданные!")
            return
        img = Image.open(self.file_name)
        name = os.path.basename(self.file_name)[:-4]
        exif_dict = piexif.load(img.info["exif"])
        if not (tag_to_delete in self.inverseTAGS.keys()):
            # Выводим сообщение об ошибке
            QMessageBox.warning(self, "Ошибка", "Тег не найден!")
            return
        if tag_to_delete == "GPSInfo":
            # Удаляем метаданные GPSInfo
            del exif_dict["GPS"]
        else:
            # Удаляем метаданные, которые совпадают с тегом, который нужно удалить
            for key, value in exif_dict.items():
                if not isinstance(value, dict):
                    continue
                correct_tag = self.inverseTAGS[tag_to_delete]
                if correct_tag in value:
                    del exif_dict[key][correct_tag]
        exif_bytes = piexif.dump(exif_dict)
        img.save(f"{name}_no_{tag_to_delete}.jpg", exif=exif_bytes)
        # Выводим сообщение об успешном удалении метаданных
        QMessageBox.information(self, "Успех", "Метаданные успешно удалены!")

    # Функция для удаления всех метаданных из изображения
    def deleteAllMetadata(self):
        # Получаем текст из поля с метаданными
        metadata = self.metadata_field.toPlainText()
        if metadata == "" or metadata == "Файл не содержит метаданных":
            QMessageBox.warning(self, "Ошибка", "Удаление запрещено")
            return
        # Открываем диалоговое окно для выбора директории
        save_path = QFileDialog.getExistingDirectory(self, 'Выбрать директорию')
        if not self.file_name:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать изображение!")
            return
        if not save_path:
            QMessageBox.warning(self, "Ошибка", "Директория не выбрана!")
            return
        # Открываем изображение с помощью библиотеки Pillow
        image = Image.open(self.file_name)
        # Создаем копию без метаданных
        img_no_md = Image.new(image.mode, image.size)
        img_no_md.putdata(list(image.getdata()))
        # Сохраняем изображение без метаданных
        img_no_md.save(f"{self.name}_no_tags.jpg")
        # Выводим сообщение об успешном удалении метаданных
        QMessageBox.information(self, "Успех", "Метаданные успешно удалены!")

    # Функция для вывода информации о программе
    def showInfo(self):
        QMessageBox.information(self, "Информация о программе",
                                "Создано студентом группы ИКБО-10-22.\nВерсия 1.0.0.\nНикаких прав не защищено")


# Main function
def window():
    # Создаем экземпляр класса главного окна и запускаем приложение
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    window()
