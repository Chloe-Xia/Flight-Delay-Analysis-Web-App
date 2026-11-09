import os
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def run_py_file(py_file_path):
    try:
        result = subprocess.check_output(['python', py_file_path], stderr = subprocess.STDOUT, universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output

def create_pdf_with_code_and_result(py_file_path):
    c = canvas.Canvas("output.pdf", pagesize = letter)
    width, height = letter
    # 设置字体
    c.setFont("Courier", 10)
    code_text = ""
    with open(py_file_path, 'r') as file:
        code_text = file.read()
    # 将代码写入PDF
    c.drawString(100, height - 100, "Python Code:")
    c.drawString(100, height - 120, code_text)
    # 运行.py文件并获取结果
    result_text = run_py_file(py_file_path)
    c.drawString(100, height - 200, "Result:")
    c.drawString(100, height - 220, result_text)
    c.save()
if __name__ == "__main__":
    py_file_path = "your_script.py"  # 替换为实际的.py文件路径
    create_pdf_with_code_and_result(py_file_path)