import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction
 
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.iniUI()
 
    def iniUI(self):
        self.setWindowTitle("这是一个test")
        self.statusBar().showMessage("文本状态栏")
        self.resize(400, 300)
 
        # 创建一个菜单栏
        menu = self.menuBar()
        # 创建一个菜单
        file_menu = menu.addMenu("文件")
        file_menu.addSeparator()
        edit_meau = menu.addMenu('编辑')
 
        # 创建一个行为
        new_action = QAction('新文件',self)
        # 添加一个行为到菜单
        file_menu.addAction(new_action)
        # 更新状态栏文本
        new_action.setStatusTip('新的文件')

        exit_action = QAction('退出',self)
        exit_action.setStatusTip('点击退出程序')
        
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
