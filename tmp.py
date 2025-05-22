import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox
)
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主窗口布局：垂直排列两个分组
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 分组1：用户信息（包含姓名和邮箱输入）
        group_user = QWidget()
        group_user.setStyleSheet("background: #f0f0f0; border: 1px solid #999;")  # 设置分组样式
        layout_user = QVBoxLayout()
        group_user.setLayout(layout_user)

        # 添加控件到分组1
        layout_user.addWidget(QLabel("用户信息"))
        self.name_input = QLineEdit(placeholderText="请输入姓名")
        layout_user.addWidget(self.name_input)
        self.email_input = QLineEdit(placeholderText="请输入邮箱")
        layout_user.addWidget(self.email_input)

        # 分组2：设置选项（包含复选框和按钮）
        group_settings = QWidget()
        group_settings.setStyleSheet("background: #fff; border: 1px solid #999;")
        layout_settings = QHBoxLayout()
        group_settings.setLayout(layout_settings)

        # 添加控件到分组2
        self.checkbox = QCheckBox("启用高级选项")
        layout_settings.addWidget(self.checkbox)
        self.button = QPushButton("保存设置")
        layout_settings.addWidget(self.button)

        # 将两个分组添加到主窗口布局
        main_layout.addWidget(group_user)
        main_layout.addWidget(group_settings)

        # 窗口设置
        self.setWindowTitle("多分组窗口示例")
        self.setGeometry(300, 300, 400, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())