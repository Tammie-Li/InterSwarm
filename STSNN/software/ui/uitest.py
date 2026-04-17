from PyQt5 import QtWidgets, QtCore, QtGui

class TaskWidget(QtWidgets.QWidget):
    def __init__(self, gif_path, prompt="做出动作", duration=20, rest_duration=5, rounds_total=20, parent=None):
        super().__init__(parent)
        self.gif_path = gif_path  # GIF 路径
        self.prompt = prompt  # 提示词
        self.duration = duration  # 提示词和 GIF 显示时长
        self.rest_duration = rest_duration  # 休息时长
        self.rounds_total = rounds_total  # 总轮次
        self.rounds = 0  # 当前执行轮次
        self.state = "ready"  # 状态：ready, task, rest
        self.start_time = None  # 当前状态开始时间
        self.timer = QtCore.QTimer(self)  # 定时器

        # 检查 GIF 路径
        if not QtCore.QFile.exists(self.gif_path):
            print(f"错误：GIF 文件不存在，路径为 {self.gif_path}")
            return

        # 初始化 UI
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 文字居中
        self.label.setFont(QtGui.QFont("Arial", 50))  # 设置较大的字体大小
        self.label.setWordWrap(True)  # 允许换行
        self.label.setStyleSheet("font-weight: bold;")  # 加粗字体

        # GIF 控件
        self.movie = QtGui.QMovie(self.gif_path)
        self.gif_label = QtWidgets.QLabel(self)
        self.gif_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gif_label.setMovie(self.movie)

        # 进度条
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setMinimum(0)  # 最小值
        self.progress_bar.setMaximum(self.rounds_total)  # 最大值
        self.progress_bar.setValue(0)  # 当前值
        self.progress_bar.setFormat("进度: %p%")  # 显示百分比
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)  # 文字居中

        # 布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label, 1)  # label 占据大部分空间
        layout.addWidget(self.gif_label, 1)  # gif_label 占据剩余空间
        layout.addWidget(self.progress_bar)  # 添加进度条
        self.setLayout(layout)

        # 初始化状态
        self.label.setText("准备阶段，请摆好手势...")
        self.gif_label.hide()
        self.timer.timeout.connect(self.update_task)  # 连接定时器
        self.start_task()  # 启动任务

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
            self.label.setText(f"准备阶段: {int(3 - elapsed_time)}s 后开始")
            if elapsed_time >= 3:  # 3 秒倒计时
                self.state = "task"
                self.start_time = current_time
                self.movie.start()  # 开始播放 GIF
        elif self.state == "task":
            # 显示提示词和 GIF
            self.label.setText(f"{self.prompt} (第 {self.rounds + 1} 轮 / 共 {self.rounds_total} 轮)")
            self.label.setFont(QtGui.QFont("Arial", 50))  # 设置较大的字体大小
            self.gif_label.show()

            # 更新进度条
            self.progress_bar.setValue(self.rounds)

            if elapsed_time >= self.duration:  # 提示词和 GIF 显示时长
                self.state = "rest"
                self.start_time = current_time
                self.movie.stop()  # 停止播放 GIF
        elif self.state == "rest":
            # 休息
            self.label.setText(f"休息中... ({int(self.rest_duration - elapsed_time)}s)")
            self.label.setFont(QtGui.QFont("Arial", 30))  # 休息时字体稍小
            self.gif_label.hide()
            if elapsed_time >= self.rest_duration:  # 休息时长
                self.rounds += 1
                if self.rounds < self.rounds_total:
                    self.state = "ready"  # 进入下一轮准备阶段
                    self.start_time = current_time
                else:
                    self.state = "idle"
                    self.timer.stop()
                    self.label.setText("任务完成！")
                    self.progress_bar.setValue(self.rounds_total)  # 完成时进度条满
                    self.movie.stop()  # 停止播放 GIF

if __name__ == "__main__":
    import sys, os
    app = QtWidgets.QApplication(sys.argv)
    widget = TaskWidget(os.path.join(os.getcwd(), "Lib", "gesture", "001.GIF"))  # 替换为你的视频路径
    widget.resize(800, 600)  # 初始窗口大小
    widget.show()
    sys.exit(app.exec_())
