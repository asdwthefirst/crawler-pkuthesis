from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# def sort_by_number(filename):
#     return int(filename.split('.')[0][3:])

def convert_images_to_pdf(input_folder, output_filename):
    # 获取文件夹中所有图片文件的路径
    image_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    image_paths = sorted(image_paths, key=lambda x: int(os.path.basename(x).split('.')[0][3:]))
    # 创建PDF文件
    c = canvas.Canvas(output_filename, pagesize=letter)

    # 遍历图片文件并将它们添加到PDF文件中
    for image_path in image_paths:
        img = Image.open(image_path)
        width, height = img.size
        c.setPageSize((width, height))
        c.drawImage(image_path, 0, 0, width, height)
        c.showPage()

    # 保存PDF文件
    c.save()

# 示例用法
# input_folder = 'path/to/input/folder'
# output_filename = 'output.pdf'
# convert_images_to_pdf(input_folder, output_filename)
