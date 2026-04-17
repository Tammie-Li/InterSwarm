from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(2179, 1210)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        # 创建中心部件
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # 创建 frame_2
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 设置字体
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        # 创建另一个页面
        self.paradigm_widget = QtWidgets.QWidget()

        # 创建 QStackedWidget 并添加页面
        self.stack_widget = QtWidgets.QStackedWidget()
        self.stack_widget.addWidget(self.centralwidget)  # 添加 centralwidget
        self.stack_widget.addWidget(self.paradigm_widget)  # 添加 paradigm_widget

        # 设置 QStackedWidget 为 MainWindow 的中心部件
        self.setCentralWidget(self.stack_widget)

        # 设置默认显示的页面（centralwidget）
        self.stack_widget.setCurrentIndex(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
