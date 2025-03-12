import serial
import xlwings as xw
import time
import os

ser = serial.Serial('COM8', 9600)  # تأكد من المنفذ الصحيح

# إنشاء/فتح الملف
file_path = "data.xlsx"
if not os.path.exists(file_path):
    wb = xw.Book()
    wb.save(file_path)
    wb.close()

wb = xw.Book(file_path)

# اختيار الورقة الأولى بالفهرس (لتجنب مشكلة الأسماء)
ws = wb.sheets[0]  # الفهرس 0 للورقة الأولى

row = 1

while True:
    try:
        data = ser.readline().decode('utf-8', errors='replace').strip()  # استبدال البايتات التالفة برموز خاصة
        values = data.split(',')
        ws.range(f"A{row}").value = values
        row += 1
        time.sleep(0.1)

    except KeyboardInterrupt:
        ser.close()
        wb.save()
        wb.close()
        break