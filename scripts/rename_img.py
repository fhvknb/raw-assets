#!/usr/bin/env python
# coding=utf-8

import os
import sys

def rename_images(directory):
    # 获取目录中的所有文件
    files = os.listdir(directory)
    
    # 过滤出图片文件（根据扩展名）
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    images = [f for f in files if f.lower().endswith(image_extensions)]
    
    # 重命名图片
    for index, image in enumerate(images):
        # 获取文件扩展名
        file_extension = os.path.splitext(image)[1]
        
        # 创建新的文件名
        new_name = f"image_{(index + 1):05}{file_extension}"
        
        # 获取完整的旧文件路径和新文件路径
        old_file_path = os.path.join(directory, image)
        new_file_path = os.path.join(directory, new_name)
        
        # 重命名文件
        os.rename(old_file_path, new_file_path)
    print(f'finished!')


if __name__ == "__main__":
    dir_name = ''
    if len(sys.argv) > 1:
        dir_name = sys.argv[1]
    
    if dir_name == '':
        raise ValueError("文件路径参数不能为空") 
    
    script_dir = os.path.dirname(os.path.abspath(__file__))

    root_dir = os.path.dirname(script_dir)
    
    files_dir = os.path.join(root_dir,  dir_name)

    rename_images(files_dir)
    
   
    
   
        
        
        
    