import sys
from PyQt5 import QtWidgets
from ltxcxTool import LTXCXApp


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LTXCXApp(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())