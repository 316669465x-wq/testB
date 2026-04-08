#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Programming Tool Interface - Qt5 Python Implementation

基于AI编程工具界面设计框架的高效IDE界面实现
核心特性:
- 三栏黄金比例布局 (60%编辑器, 20%左侧功能区, 20%右侧辅助区)
- 深色模式优化
- AI生成代码视觉标识
- 响应式设计与多设备适配
- 交互反馈设计
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTextEdit, QTreeWidget, QTreeWidgetItem, QToolBar,
    QStatusBar, QMenuBar, QMenu, QAction, QDockWidget, QListWidget,
    QListWidgetItem, QPushButton, QLabel, QFrame, QScrollArea,
    QSizePolicy, QShortcut, QMessageBox, QTabWidget, QComboBox,
    QCheckBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QKeySequence, QIcon, QTextCursor


class CodeEditor(QTextEdit):
    """
    代码编辑器组件
    - 使用等宽字体 (Fira Code / JetBrains Mono)
    - 字号14px, 行高22px (1.57倍行高)
    - 支持AI生成代码的视觉标识
    """
    
    # 信号：当用户接受/拒绝AI建议时触发
    ai_suggestion_accepted = pyqtSignal(str)
    ai_suggestion_rejected = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置等宽字体
        self.setFont(QFont("Courier New", 14))
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # 设置行高 (通过文档默认文本格式)
        font_metrics = self.fontMetrics()
        line_height = int(font_metrics.height() * 1.57)
        
        # 设置深色主题
        self.setup_dark_theme()
        
        # AI建议相关属性
        self.ai_suggestion_start = None
        self.ai_suggestion_end = None
        self.ai_suggestion_text = ""
        self.ai_suggestion_visible = False
        
        # 自动隐藏计时器
        self.auto_hide_timer = QTimer(self)
        self.auto_hide_timer.timeout.connect(self.hide_ai_suggestion)
        
        # 示例代码
        self.setPlaceholderText("在此编写代码...")
        self.load_sample_code()
    
    def setup_dark_theme(self):
        """设置深色主题配色"""
        # 背景色: #1e1e1e (VS Code风格)
        # 前景色: #d4d4d4
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                selection-background-color: #264f78;
                selection-color: #ffffff;
                border: none;
                padding: 5px;
            }
            QTextEdit:focus {
                border: none;
            }
        """)
        
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("#1e1e1e"))
        palette.setColor(QPalette.Text, QColor("#d4d4d4"))
        self.setPalette(palette)
    
    def load_sample_code(self):
        """加载示例代码"""
        sample_code = """# AI Programming Tool - Sample Code
# 演示AI生成代码的视觉标识功能

def calculate_fibonacci(n: int) -> list:
    \"\"\"计算斐波那契数列\"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_value = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_value)
    
    return fib_sequence

# 主函数
def main():
    result = calculate_fibonacci(10)
    print(f"斐波那契数列: {result}")

if __name__ == "__main__":
    main()
"""
        self.setText(sample_code)
    
    def show_ai_suggestion(self, suggestion_text: str, position: int = None):
        """
        显示AI代码建议
        - 使用浅蓝色背景 (#E0F2FE) 标识AI生成代码
        - 不透明度80%
        - 3-5秒后自动隐藏
        """
        if position is None:
            cursor = self.textCursor()
            position = cursor.position()
        
        self.ai_suggestion_start = position
        self.ai_suggestion_text = suggestion_text
        
        # 在当前位置插入AI建议
        cursor.setPosition(position)
        cursor.insertText(suggestion_text)
        
        # 标记AI生成的代码范围
        self.ai_suggestion_end = cursor.position()
        
        # 高亮AI生成的代码 (浅蓝色背景)
        self.highlight_ai_suggestion()
        
        self.ai_suggestion_visible = True
        
        # 启动自动隐藏计时器 (4秒)
        self.auto_hide_timer.start(4000)
    
    def highlight_ai_suggestion(self):
        """高亮显示AI生成的代码"""
        if self.ai_suggestion_start is None or self.ai_suggestion_end is None:
            return
        
        cursor = self.textCursor()
        cursor.setPosition(self.ai_suggestion_start)
        cursor.setPosition(self.ai_suggestion_end, QTextCursor.KeepAnchor)
        
        # 创建格式：浅蓝色背景，80%不透明度效果
        format = cursor.charFormat()
        format.setBackground(QColor("#E0F2FE"))
        format.setForeground(QColor("#1e1e1e"))
        cursor.setCharFormat(format)
        
        self.setTextCursor(cursor)
    
    def hide_ai_suggestion(self):
        """隐藏AI建议标识"""
        self.auto_hide_timer.stop()
        self.ai_suggestion_visible = False
        
        # 移除高亮 (恢复默认样式)
        if self.ai_suggestion_start is not None and self.ai_suggestion_end is not None:
            cursor = self.textCursor()
            cursor.setPosition(self.ai_suggestion_start)
            cursor.setPosition(self.ai_suggestion_end, QTextCursor.KeepAnchor)
            
            format = cursor.charFormat()
            format.setBackground(Qt.transparent)
            format.setForeground(QColor("#d4d4d4"))
            cursor.setCharFormat(format)
            
            self.setTextCursor(cursor)
    
    def accept_ai_suggestion(self):
        """接受AI建议"""
        if self.ai_suggestion_text:
            self.ai_suggestion_accepted.emit(self.ai_suggestion_text)
        self.hide_ai_suggestion()
        self.ai_suggestion_text = ""
    
    def reject_ai_suggestion(self):
        """拒绝AI建议"""
        if self.ai_suggestion_start is not None and self.ai_suggestion_end is not None:
            # 删除AI建议的代码
            cursor = self.textCursor()
            cursor.setPosition(self.ai_suggestion_start)
            cursor.setPosition(self.ai_suggestion_end, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        
        self.ai_suggestion_rejected.emit()
        self.hide_ai_suggestion()
        self.ai_suggestion_text = ""


class FileExplorer(QTreeWidget):
    """
    文件浏览器组件
    - 左侧功能区 (20%宽度)
    - 显示项目结构
    """
    
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setHeaderHidden(True)
        self.setIndentation(20)
        
        # 设置深色主题
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #252526;
                color: #cccccc;
                border: none;
                border-right: 1px solid #3c3c3c;
            }
            QTreeWidget::item {
                height: 25px;
                padding: 2px;
            }
            QTreeWidget::item:hover {
                background-color: #2a2d2e;
            }
            QTreeWidget::item:selected {
                background-color: #37373d;
            }
        """)
        
        # 加载示例项目结构
        self.load_project_structure()
    
    def load_project_structure(self):
        """加载示例项目结构"""
        # 项目根节点
        root = QTreeWidgetItem(["📁 AI Coding Tool"])
        root.setExpanded(True)
        
        # 源代码目录
        src_folder = QTreeWidgetItem(["📁 src"])
        src_files = [
            "📄 main.py",
            "📄 editor.py",
            "📄 ai_engine.py",
            "📄 utils.py"
        ]
        for file_name in src_files:
            src_folder.addChild(QTreeWidgetItem([file_name]))
        
        # 测试目录
        tests_folder = QTreeWidgetItem(["📁 tests"])
        test_files = [
            "📄 test_main.py",
            "📄 test_editor.py"
        ]
        for file_name in test_files:
            tests_folder.addChild(QTreeWidgetItem([file_name]))
        
        # 配置文件
        config_files = [
            "📄 requirements.txt",
            "📄 config.json",
            "📄 README.md"
        ]
        
        root.addChild(src_folder)
        root.addChild(tests_folder)
        
        for file_name in config_files:
            root.addChild(QTreeWidgetItem([file_name]))
        
        self.addTopLevelItem(root)
        
        # 连接信号
        self.itemClicked.connect(self.on_item_clicked)
    
    def on_item_clicked(self, item, column):
        """处理文件点击事件"""
        file_name = item.text(column)
        if not file_name.startswith("📁"):
            self.file_selected.emit(file_name)


class AIPanel(QWidget):
    """
    AI助手面板组件
    - 右侧辅助区 (20%宽度)
    - 提供AI对话、代码生成等功能
    """
    
    code_generated = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        self.setup_dark_theme()
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        title_label = QLabel("🤖 AI 助手")
        title_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        
        layout.addWidget(title_bar)
        
        # AI对话区域
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(10)
        
        # 添加欢迎消息
        self.add_chat_message("ai", "你好！我是你的AI编程助手。我可以帮助你：\n\n• 生成代码\n• 解释代码\n• 调试问题\n• 代码重构\n\n请告诉我你需要什么帮助？")
        
        self.chat_area.setWidget(self.chat_content)
        layout.addWidget(self.chat_area, stretch=1)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setFixedHeight(120)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)
        input_layout.setSpacing(5)
        
        # 快捷操作按钮
        quick_actions = QHBoxLayout()
        
        btn_generate = QPushButton("✨ 生成代码")
        btn_generate.setFixedSize(90, 28)
        btn_generate.setStyleSheet(self.get_button_style("#0e639c"))
        btn_generate.clicked.connect(lambda: self.quick_action("generate"))
        
        btn_explain = QPushButton("📖 解释代码")
        btn_explain.setFixedSize(90, 28)
        btn_explain.setStyleSheet(self.get_button_style("#3c3c3c"))
        btn_explain.clicked.connect(lambda: self.quick_action("explain"))
        
        btn_debug = QPushButton("🐛 调试")
        btn_debug.setFixedSize(70, 28)
        btn_debug.setStyleSheet(self.get_button_style("#3c3c3c"))
        btn_debug.clicked.connect(lambda: self.quick_action("debug"))
        
        quick_actions.addWidget(btn_generate)
        quick_actions.addWidget(btn_explain)
        quick_actions.addWidget(btn_debug)
        quick_actions.addStretch()
        
        input_layout.addLayout(quick_actions)
        
        # 输入框
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("描述你的需求...")
        self.input_field.setMaximumHeight(60)
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
            }
            QTextEdit:focus {
                border: 1px solid #0e639c;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        # 发送按钮
        send_btn = QPushButton("➤ 发送")
        send_btn.setFixedHeight(32)
        send_btn.setStyleSheet(self.get_button_style("#0e639c"))
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(input_frame)
    
    def setup_dark_theme(self):
        """设置深色主题"""
        self.setStyleSheet("""
            QWidget {
                background-color: #252526;
            }
            QScrollArea {
                border: none;
                border-left: 1px solid #3c3c3c;
            }
        """)
    
    def get_button_style(self, bg_color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {bg_color}dd;
            }}
            QPushButton:pressed {{
                background-color: {bg_color}aa;
            }}
        """
    
    def add_chat_message(self, sender: str, message: str):
        """添加聊天消息"""
        message_frame = QFrame()
        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(10, 8, 10, 8)
        
        # 消息气泡
        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        if sender == "ai":
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #3c3c3c;
                    color: #cccccc;
                    border-radius: 8px;
                    padding: 8px;
                    margin-left: 10px;
                }
            """)
        else:
            bubble.setStyleSheet("""
                QLabel {
                    background-color: #0e639c;
                    color: #ffffff;
                    border-radius: 8px;
                    padding: 8px;
                    margin-right: 10px;
                }
            """)
        
        message_layout.addWidget(bubble)
        self.chat_layout.addWidget(message_frame)
        
        # 滚动到底部
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def quick_action(self, action_type: str):
        """快捷操作"""
        actions = {
            "generate": "请帮我生成一段代码...",
            "explain": "请解释这段代码的功能...",
            "debug": "帮我找出代码中的问题..."
        }
        
        if action_type in actions:
            self.input_field.setText(actions[action_type])
            self.send_message()
    
    def send_message(self):
        """发送消息"""
        message = self.input_field.toPlainText().strip()
        if not message:
            return
        
        # 添加用户消息
        self.add_chat_message("user", message)
        self.input_field.clear()
        
        # 模拟AI响应
        QTimer.singleShot(1000, lambda: self.simulate_ai_response(message))
    
    def simulate_ai_response(self, user_message: str):
        """模拟AI响应"""
        responses = {
            "generate": "我已经为你生成了以下代码：\n\n```python\ndef hello_world():\n    print('Hello, World!')\n```\n\n你可以点击'插入代码'按钮将代码插入到编辑器中。",
            "explain": "这段代码的主要功能是...\n\n**关键点:**\n1. 使用了递归算法\n2. 时间复杂度为 O(n)\n3. 空间复杂度为 O(1)",
            "debug": "我发现了以下问题:\n\n⚠️ **警告**: 第 5 行可能存在空指针异常\n💡 **建议**: 添加空值检查\n\n```python\nif value is not None:\n    # 处理逻辑\n```"
        }
        
        # 根据用户消息内容选择合适的响应
        response = responses.get("generate", responses["generate"])
        
        if "解释" in user_message or "explain" in user_message.lower():
            response = responses["explain"]
        elif "调试" in user_message or "debug" in user_message.lower():
            response = responses["debug"]
        
        self.add_chat_message("ai", response)
        
        # 如果是代码生成，触发生成信号
        if "generate" in user_message.lower() or "生成" in user_message:
            sample_code = "\n# AI 生成的代码\ndef optimized_function(data):\n    result = [x * 2 for x in data if x > 0]\n    return result\n"
            self.code_generated.emit(sample_code)


class TerminalPanel(QTextEdit):
    """
    终端面板组件
    - 显示程序输出和命令行交互
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 12))
        
        # 设置深色主题
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: none;
                padding: 5px;
                font-family: 'Courier New', monospace;
            }
        """)
        
        # 欢迎信息
        self.append("=" * 60)
        self.append("AI Programming Tool - Terminal")
        self.append("=" * 60)
        self.append("")
        self.append("就绪。输入命令或运行程序...")
        self.append("")


class StatusBarWidget(QWidget):
    """
    状态栏组件
    - 显示AI状态、光标位置等信息
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(20)
        
        # AI状态指示器
        self.ai_status = QLabel("🟢 AI 就绪")
        self.ai_status.setStyleSheet("color: #4ec9b0; font-size: 13px;")
        layout.addWidget(self.ai_status)
        
        # 分隔符
        separator = QLabel("|")
        separator.setStyleSheet("color: #666666;")
        layout.addWidget(separator)
        
        # 光标位置
        self.cursor_position = QLabel("Ln 1, Col 1")
        self.cursor_position.setStyleSheet("color: #9cdcfe; font-size: 13px;")
        layout.addWidget(self.cursor_position)
        
        # 分隔符
        separator = QLabel("|")
        separator.setStyleSheet("color: #666666;")
        layout.addWidget(separator)
        
        # 编码格式
        encoding_label = QLabel("UTF-8")
        encoding_label.setStyleSheet("color: #9cdcfe; font-size: 13px;")
        layout.addWidget(encoding_label)
        
        # 右侧：AI控制开关
        layout.addStretch()
        
        self.ai_toggle = QCheckBox("AI 辅助")
        self.ai_toggle.setChecked(True)
        self.ai_toggle.setStyleSheet("""
            QCheckBox {
                color: #4ec9b0;
                font-size: 13px;
            }
            QCheckBox::indicator:checked {
                background-color: #4ec9b0;
            }
        """)
        layout.addWidget(self.ai_toggle)


class MainWindow(QMainWindow):
    """
    主窗口类
    实现三栏黄金比例布局:
    - 左侧功能区 (20%): 文件浏览器
    - 中间编辑区 (60%): 代码编辑器
    - 右侧辅助区 (20%): AI助手面板
    """
    
    def __init__(self):
        super().__init__()
        
        self.window_title = "AI Programming Tool"
        self.setWindowTitle(self.window_title)
        self.setMinimumSize(1400, 900)
        
        # 初始化UI
        self.init_ui()
        self.create_menu_bar()
        self.create_toolbar()
        self.create_status_bar()
        self.create_shortcuts()
        
        # 应用全局样式
        self.apply_global_style()
    
    def init_ui(self):
        """初始化UI"""
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器 (三栏布局)
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：文件浏览器 (20%)
        self.file_explorer = FileExplorer()
        self.file_explorer.setMinimumWidth(200)
        self.file_explorer.setMaximumWidth(400)
        
        # 中间：代码编辑器 (60%)
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        # 编辑器标签页
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #cccccc;
                padding: 8px 20px;
                border: none;
                border-right: 1px solid #1e1e1e;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #3e3e3e;
            }
        """)
        
        # 代码编辑器
        self.code_editor = CodeEditor()
        self.editor_tabs.addTab(self.code_editor, "📄 main.py")
        
        editor_layout.addWidget(self.editor_tabs)
        
        # 底部终端面板
        terminal_dock = QDockWidget("终端")
        terminal_dock.setMinimumHeight(150)
        terminal_dock.setMaximumHeight(300)
        self.terminal = TerminalPanel()
        terminal_dock.setWidget(self.terminal)
        terminal_dock.setStyleSheet("""
            QDockWidget {
                titlebar-close-icon: none;
                titlebar-normal-icon: none;
            }
            QDockWidget::title {
                background-color: #2d2d2d;
                padding: 5px;
                color: #cccccc;
            }
        """)
        
        # 添加接受/拒绝AI建议的工具栏
        ai_actions_frame = QFrame()
        ai_actions_frame.setFixedHeight(40)
        ai_actions_layout = QHBoxLayout(ai_actions_frame)
        ai_actions_layout.setContentsMargins(10, 5, 10, 5)
        
        ai_label = QLabel("AI 建议:")
        ai_label.setStyleSheet("color: #cccccc; font-size: 13px;")
        ai_actions_layout.addWidget(ai_label)
        
        self.accept_btn = QPushButton("✓ 接受 (Ctrl+Enter)")
        self.accept_btn.setFixedSize(120, 28)
        self.accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #28a745dd;
            }
        """)
        self.accept_btn.clicked.connect(self.accept_ai_suggestion)
        ai_actions_layout.addWidget(self.accept_btn)
        
        self.reject_btn = QPushButton("✗ 拒绝 (Esc)")
        self.reject_btn.setFixedSize(120, 28)
        self.reject_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #dc3545dd;
            }
        """)
        self.reject_btn.clicked.connect(self.reject_ai_suggestion)
        ai_actions_layout.addWidget(self.reject_btn)
        
        ai_actions_layout.addStretch()
        
        editor_layout.addWidget(ai_actions_frame)
        editor_layout.addWidget(terminal_dock)
        
        # 右侧：AI助手面板 (20%)
        self.ai_panel = AIPanel()
        self.ai_panel.setMinimumWidth(250)
        self.ai_panel.setMaximumWidth(500)
        
        # 添加到分割器
        splitter.addWidget(self.file_explorer)
        splitter.addWidget(editor_container)
        splitter.addWidget(self.ai_panel)
        
        # 设置分割比例 (20% : 60% : 20%)
        total_width = 1400
        splitter.setSizes([280, 840, 280])
        
        main_layout.addWidget(splitter)
        
        # 连接信号
        self.ai_panel.code_generated.connect(self.insert_ai_code)
        self.code_editor.cursorPositionChanged.connect(self.update_cursor_position)
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #3c3c3c;
                color: #ffffff;
                border-bottom: 1px solid #1e1e1e;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #505050;
            }
            QMenu {
                background-color: #252526;
                color: #ffffff;
                border: 1px solid #3c3c3c;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
        """)
        
        # 文件菜单
        file_menu = menubar.addMenu("文件 (&F)")
        
        new_action = QAction("新建 (&N)", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: self.show_info("新建文件"))
        file_menu.addAction(new_action)
        
        open_action = QAction("打开 (&O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(lambda: self.show_info("打开文件"))
        file_menu.addAction(open_action)
        
        save_action = QAction("保存 (&S)", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(lambda: self.show_info("保存文件"))
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出 (&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑 (&E)")
        
        undo_action = QAction("撤销 (&U)", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.code_editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("重做 (&R)", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.code_editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("剪切 (&T)", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.code_editor.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("复制 (&C)", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.code_editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("粘贴 (&P)", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.code_editor.paste)
        edit_menu.addAction(paste_action)
        
        # AI菜单
        ai_menu = menubar.addMenu("AI (&A)")
        
        generate_code_action = QAction("生成代码 (&G)", self)
        generate_code_action.setShortcut("Ctrl+Space")
        generate_code_action.triggered.connect(lambda: self.show_ai_suggestion())
        ai_menu.addAction(generate_code_action)
        
        explain_code_action = QAction("解释代码 (&E)", self)
        explain_code_action.setShortcut("Ctrl+Shift+E")
        explain_code_action.triggered.connect(lambda: self.show_info("AI 代码解释功能"))
        ai_menu.addAction(explain_code_action)
        
        refactor_action = QAction("代码重构 (&R)", self)
        refactor_action.setShortcut("Ctrl+Shift+R")
        refactor_action.triggered.connect(lambda: self.show_info("AI 代码重构功能"))
        ai_menu.addAction(refactor_action)
        
        ai_menu.addSeparator()
        
        toggle_ai_action = QAction("切换 AI 辅助 (&T)", self)
        toggle_ai_action.setShortcut("Ctrl+Shift+A")
        toggle_ai_action.setCheckable(True)
        toggle_ai_action.setChecked(True)
        ai_menu.addAction(toggle_ai_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图 (&V)")
        
        toggle_terminal_action = QAction("显示/隐藏终端 (&T)", self)
        toggle_terminal_action.setShortcut("Ctrl+`")
        toggle_terminal_action.triggered.connect(lambda: self.show_info("切换终端显示"))
        view_menu.addAction(toggle_terminal_action)
        
        toggle_sidebar_action = QAction("显示/隐藏侧边栏 (&S)", self)
        toggle_sidebar_action.setShortcut("Ctrl+B")
        toggle_sidebar_action.triggered.connect(lambda: self.show_info("切换侧边栏显示"))
        view_menu.addAction(toggle_sidebar_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助 (&H)")
        
        about_action = QAction("关于 (&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #3c3c3c;
                border: none;
                border-bottom: 1px solid #1e1e1e;
                padding: 2px;
                spacing: 3px;
            }
            QToolButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-size: 13px;
            }
            QToolButton:hover {
                background-color: #505050;
            }
            QToolButton:pressed {
                background-color: #0e639c;
            }
        """)
        
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        
        # 添加常用操作按钮
        toolbar.addAction("📄 新建")
        toolbar.addAction("📂 打开")
        toolbar.addAction("💾 保存")
        toolbar.addSeparator()
        toolbar.addAction("▶️ 运行")
        toolbar.addAction("🐛 调试")
        toolbar.addSeparator()
        toolbar.addAction("✨ AI 生成")
        toolbar.addAction("🔍 AI 分析")
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar_widget = StatusBarWidget()
        self.statusBar().addWidget(self.status_bar_widget)
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #007acc;
                color: #ffffff;
            }
        """)
    
    def create_shortcuts(self):
        """创建快捷键"""
        # 接受 AI 建议
        shortcut_accept = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut_accept.activated.connect(self.accept_ai_suggestion)
        
        # 拒绝 AI 建议
        shortcut_reject = QShortcut(QKeySequence("Escape"), self)
        shortcut_reject.activated.connect(self.reject_ai_suggestion)
        
        # AI 代码生成
        shortcut_ai = QShortcut(QKeySequence("Ctrl+Space"), self)
        shortcut_ai.activated.connect(self.show_ai_suggestion)
    
    def apply_global_style(self):
        """应用全局样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QSplitter::handle {
                background-color: #3c3c3c;
                width: 1px;
            }
            QSplitter::handle:horizontal {
                width: 1px;
            }
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #424242;
                min-height: 30px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4f4f4f;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background-color: #1e1e1e;
                height: 14px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #424242;
                min-width: 30px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #4f4f4f;
            }
            QScrollBar::add-line:horizontal {
                width: 0px;
            }
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
    
    def update_cursor_position(self):
        """更新光标位置显示"""
        cursor = self.code_editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_bar_widget.cursor_position.setText(f"Ln {line}, Col {col}")
    
    def show_ai_suggestion(self):
        """显示 AI 代码建议"""
        sample_suggestion = """
# AI 智能建议
def optimize_data_processing(items):
    \"\"\"优化的数据处理函数\"\"\"
    # 使用列表推导式提高效率
    processed = [item * 2 for item in items if item > 0]
    return processed
"""
        self.code_editor.show_ai_suggestion(sample_suggestion)
        self.terminal.append("\n[AI] 已生成代码建议，请使用 Ctrl+Enter 接受或 Esc 拒绝")
    
    def insert_ai_code(self, code: str):
        """插入 AI 生成的代码"""
        self.code_editor.show_ai_suggestion(code)
        self.terminal.append("\n[AI] 代码已生成，等待确认...")
    
    def accept_ai_suggestion(self):
        """接受 AI 建议"""
        self.code_editor.accept_ai_suggestion()
        self.terminal.append("\n[✓] AI 建议已接受")
        self.status_bar_widget.ai_status.setText("🟢 AI 已应用")
    
    def reject_ai_suggestion(self):
        """拒绝 AI 建议"""
        self.code_editor.reject_ai_suggestion()
        self.terminal.append("\n[✗] AI 建议已拒绝")
        self.status_bar_widget.ai_status.setText("🟢 AI 就绪")
    
    def show_info(self, message: str):
        """显示信息提示"""
        self.terminal.append(f"\n[INFO] {message}")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>AI Programming Tool</h2>
        <p>版本：1.0.0</p>
        <p>基于 Qt5 和 Python3 构建</p>
        <br>
        <p><b>核心特性:</b></p>
        <ul>
            <li>三栏黄金比例布局 (60% 编辑器)</li>
            <li>深色模式优化</li>
            <li>AI 生成代码视觉标识</li>
            <li>实时交互反馈</li>
            <li>响应式设计</li>
        </ul>
        <br>
        <p>遵循 WCAG 2.1 AA 无障碍标准</p>
        """
        QMessageBox.about(self, "关于 AI Programming Tool", about_text)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("AI Programming Tool")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AI Coding Lab")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
