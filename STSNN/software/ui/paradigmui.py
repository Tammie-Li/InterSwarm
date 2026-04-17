from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

import os
from PyQt5.QtCore import *

from PyQt5.QtGui import QFont
import numpy as np
import ctypes


MAX = 60
NORM = 16
MIN = 12


class BaseGUI:
    def __init__(self):
        # 设置字体格式
        self.font_en_bold = QFont("Times New Roman", NORM, QFont.Bold)
        self.font_ch_bold = QFont("微软雅黑", NORM, QFont.Bold)

        self.font_en = QFont("Times New Roman", NORM)
        self.font_ch = QFont("微软雅黑", NORM)

        self.font_en_min = QFont("Times New Roman", MIN)
        self.font_ch_min = QFont("微软雅黑", MIN)

        self.font_ch_tips = QFont("微软雅黑", MAX, QFont.Bold)


class TaskWidget(QtWidgets.QWidget):
    def __init__(self, gif_path_list, prompt="开始采集", duration=20, rest_duration=5, rounds_total=20, parent=None):
        super().__init__(parent)
        self.gif_path_list = gif_path_list  # GIF 路径
        self.prompt = prompt  # 提示词
        self.duration = duration  # 提示词和 GIF 显示时长
        self.rest_duration = rest_duration  # 休息时长
        self.rounds_total = rounds_total  # 总轮次
        self.rounds = 0  # 当前执行轮次
        self.state = "ready"  # 状态：ready, task, rest
        self.start_time = None  # 当前状态开始时间
        self.timer = QtCore.QTimer(self)  # 定时器

        # 初始化 UI
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 文字居中
        self.label.setFont(QtGui.QFont("Arial", 30))  # 设置较大的字体大小
        self.label.setWordWrap(True)  # 允许换行
        self.label.setStyleSheet("font-weight: bold;")  # 加粗字体
        self.label.setFixedHeight(200)

        self.movie = QtGui.QMovie("Lib/init.png")
        self.image_label = QtWidgets.QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setMovie(self.movie)
        self.movie.start()

        # 进度条
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)  # 最小值
        self.progress_bar.setMaximum(self.duration)  # 最大值
        self.progress_bar.setValue(0)  # 当前值
        # self.progress_bar.setFormat("进度: %p%")  # 显示百分比
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)  # 文字居中
        self.progress_bar.setFixedHeight(30)

        # 布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label, 1)  # label 占据大部分空间
        layout.addWidget(self.image_label, 1)  # gif_label 占据剩余空间
        layout.addWidget(self.progress_bar)  # 添加进度条
        self.setLayout(layout)

        # 初始化状态
        self.label.setText("点击开始按钮启动数据采集...")
        self.timer.timeout.connect(self.update_task)  # 连接定时器

    def start_task(self):
        """启动任务"""
        self.state = "ready"
        self.start_time = QtCore.QDateTime.currentDateTime()
        self.timer.start(100)  # 每 100ms 检查一次状态

    def update_task(self):
        """任务状态更新"""
        current_time = QtCore.QDateTime.currentDateTime()
        elapsed_time = self.start_time.msecsTo(current_time) / 1000  # 转换为秒
        if self.state == "ready":
            # 准备阶段，显示手势提示
            self.label.setText(f"请熟悉下一个指令: {int(5 - elapsed_time)}s 后开始")
            if elapsed_time >= 5:  # 5 秒倒计时
                self.state = "task"
                self.start_time = current_time
            if elapsed_time < 1:
                self.movie = QtGui.QMovie(os.path.join(os.getcwd(), "Lib", "gesture", self.gif_path_list[self.rounds]))
                self.image_label.setMovie(self.movie)
                self.movie.start()  # 开始播放 GIF
                self.image_label.show()



        elif self.state == "task":
            # 显示提示词和 GIF
            self.label.setText(f"{self.prompt} (第 {self.rounds + 1} 轮 / 共 {self.rounds_total} 轮)")
            self.image_label.show()

            # 更新进度条
            self.progress_bar.setValue(elapsed_time)


            if elapsed_time >= self.duration:  # 提示词和 GIF 显示时长
                self.state = "rest"
                self.start_time = current_time
                self.movie.stop()  # 停止播放 GIF
        elif self.state == "rest":
            # 休息
            self.label.setText(f"休息中... ({int(self.rest_duration - elapsed_time)}s)")
            self.label.setFont(QtGui.QFont("Arial", 30))  # 休息时字体稍小
            # self.image_label.hide()
            if elapsed_time >= self.rest_duration:  # 休息时长
                self.rounds += 1
                if self.rounds < self.rounds_total:
                    self.state = "ready"  # 进入下一轮准备阶段
                    self.start_time = current_time
                else:
                    self.state = "idle"
                    self.timer.stop()
                    self.label.setText("任务完成！")
                    self.progress_bar.setValue(self.duration)  # 完成时进度条满
                    self.movie.stop()  # 停止播放 GIF




class InstructionCard:
    # 创建卡片用于显示 指令名称/指令数量/指令对应有动作手势/指令对应无动作手势
    def __init__(self, instruction_name, instruction_count, with_action_image, without_action_image, parent=None):

        self.widget = QtWidgets.QWidget()
        # 设置卡片布局
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)  # 设置边距

        self.widget.setLayout(self.layout)

        # 指令名称
        self.label_name = QtWidgets.QLabel(instruction_name)
        self.label_name.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_name, 0, 0, 1, 1)

        # 指令数量
        self.label_count = QtWidgets.QLabel(f"数量: {instruction_count}")
        self.label_count.setFont(QtGui.QFont("Arial", 12))
        self.label_count.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_count, 1, 0, 1, 1)

        # 有动作手势图片
        self.label_with_action = QtWidgets.QLabel()
        self.label_with_action.setFixedHeight(108)
        self.label_with_action.setFixedWidth(192)

        movie = QtGui.QMovie(with_action_image)
        self.label_with_action.setMovie(movie)

        # self.label_with_action.setPixmap(movie.scaled(150, 150, QtCore.Qt.KeepAspectRatio))
        movie.start()
        self.label_with_action.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_with_action, 0, 1, 2, 1)

        # 无动作手势图片
        self.label_without_action = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(without_action_image)
        self.label_without_action.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio))
        self.label_without_action.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_without_action, 0, 2, 2, 1)

        self.widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 15px;
            }
            QLabel{
                border: 0px solid #cccccc;
            }
        """)



class ChoiceDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("三选一选择框")
        self.setFixedSize(300, 150)

        # 创建选择框
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.addItems(["选项 1", "选项 2", "选项 3"])  # 添加三个选项
        self.combo_box.setCurrentIndex(0)  # 默认选择第一个选项

        # 确认按钮
        self.confirm_button = QtWidgets.QPushButton("确认", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        # 布局
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.confirm_button)

    def on_confirm(self):
        # 获取当前选择的选项
        selected_option = self.combo_box.currentText()
        print(f"您选择了: {selected_option}")
        self.close()


class Ui_Paradigm(BaseGUI):
    def setupUi(self, paradigm_widget):
        paradigm_widget.setObjectName("paradigm")
        paradigm_widget.setStyleSheet("background-color: rgb(255, 255, 255);")

        gesture_path_list = os.listdir(os.path.join(os.getcwd(), "Lib", "gesture"))
        gesture_free_path_list = os.listdir(os.path.join(os.getcwd(), "Lib", "gesture_free"))




        # 创建一个 QScrollArea
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 已有手势信息显示窗口
        self.gesture_info_show = QtWidgets.QWidget()
        self.layout_gesture_info_show = QtWidgets.QVBoxLayout()
        self.layout_gesture_info_show.setSpacing(20)
        self.layout_gesture_info_show.setContentsMargins(20, 20, 20, 20)

        self.gesture_info_show.setLayout(self.layout_gesture_info_show)

        name = ["向上滑", "向下滑", "向左滑", "向右滑", "确认", "返回"]
        
        for idx, path in enumerate(gesture_free_path_list):
            name_gesture, name_gesture_free = gesture_path_list[idx], gesture_free_path_list[idx]
            path_gesture, path_gesture_free = os.path.join(os.getcwd(), "Lib", "gesture", name_gesture), os.path.join(os.getcwd(), "Lib", "gesture_free", name_gesture_free)
            print(path_gesture)
            card = InstructionCard(name[idx], 60, path_gesture, path_gesture_free)
            self.layout_gesture_info_show.addWidget(card.widget)


        # 将容器设置到 QScrollArea
        scroll_area.setWidget(self.gesture_info_show)
        scroll_area.setMaximumWidth(700)


        # 创建 TaskWidget
        self.task_widget = TaskWidget(gesture_path_list)  # 替换为你的图片路径


        # 创建按钮

        self.modebox = ChoiceDialog()
        layout = QtWidgets.QVBoxLayout()
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setLayout(layout)
        
        self.start_button = QtWidgets.QPushButton("开始任务")
        self.start_button.clicked.connect(self.task_widget.start_task)

        layout.addWidget(self.modebox)
        layout.addWidget(self.start_button)


        self.start_button.setFixedWidth(400)

        self.layout = QtWidgets.QHBoxLayout()
        paradigm_widget.setLayout(self.layout)
        self.layout.addWidget(scroll_area)
        self.layout.addWidget(self.task_widget)
        self.layout.addWidget(self.start_button)






        

