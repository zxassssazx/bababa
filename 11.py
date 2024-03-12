import tkinter as tk
from tkinter import scrolledtext, Label, Entry, Button
import pyperclip
import keyboard
import random
import threading

class TextCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" 文本复制器 ")

        self.text_box = scrolledtext.ScrolledText(root, height=15, width=50)
        self.text_box.pack()

        self.save_button = Button(root, text=" 保存文本 ", command=self.save_text)
        self.save_button.pack()

        self.hotkey_label = Label(root, text=" 输入热键（如 'ctrl+shift+a'）然后按 '设置热键'：")
        self.hotkey_label.pack()

        self.hotkey_entry = Entry(root)
        self.hotkey_entry.pack()

        self.set_hotkey_button = Button(root, text=" 设置热键 ", command=self.set_hotkey)
        self.set_hotkey_button.pack()

        self.hotkey_info = Label(root, text=" 未设置热键 ")
        self.hotkey_info.pack()

        # 存储文本库和当前热键
        self.text_lines = []
        self.current_hotkey = None  # 初始化时没有设置热键

    def save_text(self):
        text_content = self.text_box.get("1.0", tk.END).strip()
        self.text_lines = text_content.split('\n')
        print(" 文本已保存。")

    def set_hotkey(self):
        new_hotkey = self.hotkey_entry.get().strip()

        # 使用 threading 确保键盘事件在后台线程中处理，避免阻塞 UI
        threading.Thread(target=self.change_hotkey, args=(new_hotkey,), daemon=True).start()

    def change_hotkey(self, new_hotkey):
        # 移除旧热键监听，如果有的话
        if self.current_hotkey:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
                self.hotkey_info.config(text=f" 热键已移除: {self.current_hotkey}")
            except KeyError:
                # 如果尝试移除一个未注册的热键，忽略 KeyError
                pass

        # 设置新的热键
        self.current_hotkey = new_hotkey
        try:
            keyboard.add_hotkey(self.current_hotkey, self.copy_and_paste, suppress=True)
            self.hotkey_info.config(text=f" 新热键已设置: {self.current_hotkey}")
        except ValueError as e:
            self.hotkey_info.config(text=f" 设置热键失败: {e}")
        self.hotkey_entry.delete(0, tk.END)  # 清空输入框

    def copy_and_paste(self):
        if self.text_lines:
            selected_text = random.choice(self.text_lines)
            pyperclip.copy(selected_text)
            # 在新线程中执行粘贴，避免冻结界面
            threading.Thread(target=self.paste_text, daemon=True).start()

    def paste_text(self):
        # 模拟粘贴文本和回车操作
        keyboard.send('ctrl+v')
        keyboard.send('enter')

# 创建 Tkinter 主窗口
root = tk.Tk()
app = TextCopierApp(root)
root.mainloop()
