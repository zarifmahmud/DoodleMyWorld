from main import *
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QApplication
from PyQt5.QtGui import QPixmap


class App(QWidget):
    """
    GUI for Doodle My World
    """

    def __init__(self):
        super().__init__()
        self.title = 'Doodle My World'
        self.left = 10
        self.top = 10
        self.width = 60
        self.height = 80
        self.text = "https://ichef.bbci.co.uk/news/660/cpsprodpb/E9DF/production/_96317895_gettyimages-164067218.jpg"
        self.voice_save = ""
        self.label = QLabel(self)
        self.textbox = QLineEdit(self)
        self.init_ui()

    def init_ui(self):
        """
        Creates the GUI, with image from image.png on left hand side of screen,
        and buttons on right hand side.
        """

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget

        pixmap = QPixmap('image.png')
        self.label.setPixmap(pixmap)
        self.label.resize(1500, 1000)
        self.resize(pixmap.width(), pixmap.height())
        button = QPushButton('Voice Command', self)
        button.move(1600, 600)
        button.clicked.connect(self.voice_command)
        self.textbox.move(1600, 300)
        self.textbox.resize(280, 40)

        # Create a button in the window
        button2 = QPushButton('Upload image from link', self)
        button2.move(1600, 350)
        button2.clicked.connect(self.upload)

        button3 = QPushButton('Refresh Image!', self)
        button3.move(1600, 400)
        button3.clicked.connect(self.refresh)

        button4 = QPushButton('Redo Command', self)
        button4.move(1600, 650)
        button4.clicked.connect(self.redo_voice)

        self.label.setScaledContents(True)
        self.show()

    def update_image(self):
        """
        Refreshes display with most current version of image.png.
        """
        pixmap = QPixmap('image.png')
        self.label.setPixmap(pixmap)

    def voice_command(self):
        """
        Button function to let user use voice to add to drawing.
        """
        self.voice_save = speech_to_doodle("")
        self.update_image()

    def redo_voice(self):
        """
        Button function that redoes last voice command.
        """
        if self.voice_save != "":
            speech_to_doodle(self.voice_save)
            self.update_image()

    def upload(self):
        """
        Button function to let user doodle-fy a photograph.
        """
        textbox_value = self.textbox.text()
        self.text = textbox_value
        self.textbox.setText("")
        pic_to_doodle(textbox_value)
        self.update_image()

    def refresh(self):
        """
        Button function that re-doodles last uploaded photograph.
        """
        pic_to_doodle(self.text)
        self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
