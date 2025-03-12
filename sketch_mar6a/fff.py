import serial
import xlwings as xw
import os
import threading
import pythoncom
from tkinter import *
from tkinter import ttk, messagebox


class ArduinoToExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino to Excel")
        self.root.geometry("400x250")

        self.ser = None
        self.running = False
        self.wb = None
        self.ws = None

        # تغيير مسار الحفظ إلى مجلد المشروع الحالي
        self.file_path = os.path.join(os.getcwd(), "data.xlsx")  # <-- التعديل هنا

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self.root, padding="10 10 10 10")
        input_frame.pack(fill=BOTH, expand=True)

        ttk.Label(input_frame, text="COM Port:").grid(column=0, row=0, sticky=W)
        self.com_port = ttk.Entry(input_frame, width=15)
        self.com_port.grid(column=1, row=0, sticky=W)
        self.com_port.insert(0, "COM8")

        ttk.Label(input_frame, text="Baud Rate:").grid(column=0, row=1, sticky=W)
        self.baud_rate = ttk.Entry(input_frame, width=15)
        self.baud_rate.grid(column=1, row=1, sticky=W)
        self.baud_rate.insert(0, "9600")

        self.start_btn = ttk.Button(input_frame, text="Start", command=self.start_logging)
        self.start_btn.grid(column=0, row=2, pady=10)

        self.stop_btn = ttk.Button(input_frame, text="Stop", command=self.stop_logging, state=DISABLED)
        self.stop_btn.grid(column=1, row=2, pady=10)

        self.status_label = ttk.Label(input_frame, text="Status: Ready", foreground="gray")
        self.status_label.grid(column=0, row=3, columnspan=2, pady=10)

    def start_logging(self):
        com = self.com_port.get()
        baud = self.baud_rate.get()

        try:
            self.ser = serial.Serial(com, int(baud), timeout=1)
            self.running = True

            # تشغيل الثريد مع تهيئة COM
            self.thread = threading.Thread(target=self.thread_target)
            self.thread.start()

            self.update_ui_state(True)
            self.show_status("Status: Running...", "green")

        except Exception as e:
            messagebox.showerror("Error", f"فشل الاتصال: {str(e)}")
            self.show_status("Status: Error", "red")

    def thread_target(self):
        """الدالة الرئيسية للثريد حيث تتم تهيئة COM"""
        pythoncom.CoInitialize()  # تهيئة COM هنا

        try:
            self.setup_excel()  # فتح ملف الإكسل داخل الثريد
            self.read_serial()
        finally:
            if self.wb:
                self.wb.close()
            pythoncom.CoUninitialize()  # تنظيف الموارد

    def read_serial(self):
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('utf-8', errors='replace').strip()
                    values = data.split(',')
                    self.write_to_excel(values)
            except Exception as e:
                self.show_status("Status: Connection Lost", "red")
                self.running = False
                break

    def setup_excel(self):
        try:
            if os.path.exists(self.file_path):
                self.wb = xw.Book(self.file_path)
                self.ws = self.wb.sheets[0]
                # تحديد الصف الأول الفارغ عند فتح ملف موجود
                self.row = self.ws.range('A' + str(self.ws.cells.last_cell.row)).end('up').row + 1
            else:
                self.wb = xw.Book()
                self.ws = self.wb.sheets[0]
                self.row = 1  # <-- البدء من الصف الأول للملف الجديد
                self.wb.save(self.file_path)

        except Exception as e:
            messagebox.showerror("Error", f"فشل تحميل ملف الإكسل: {str(e)}")
            self.running = False
    def write_to_excel(self, values):
        try:
            self.ws.range(f'A{self.row}').value = values
            self.row += 1
            self.wb.save()
        except Exception as e:
            error_msg = f"Excel Error: {str(e)}"
            self.show_status(error_msg, "red")
            messagebox.showerror("Error", error_msg)
            self.running = False

    def stop_logging(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.update_ui_state(False)
        self.show_status("Status: Stopped", "blue")

    def update_ui_state(self, is_running):
        state_btn = NORMAL if not is_running else DISABLED
        self.start_btn['state'] = state_btn
        self.stop_btn['state'] = NORMAL if is_running else DISABLED
        self.com_port['state'] = state_btn
        self.baud_rate['state'] = state_btn

    def show_status(self, text, color):
        self.status_label.config(text=text, foreground=color)

    def on_closing(self):
        self.stop_logging()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = ArduinoToExcelApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()