#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOBI图片提取工具
功能：从MOBI文件中提取所有图片并保存到指定目录
要求：保存原始尺寸和最佳分辨率
"""

import os
import sys
import argparse
import shutil
import tempfile
import subprocess
import zipfile


def extract_images_from_mobi(mobi_file, output_dir):
    """
    从MOBI文件中提取图片
    
    Args:
        mobi_file: MOBI文件路径
        output_dir: 图片输出目录
    """
    # 检查MOBI文件是否存在
    if not os.path.exists(mobi_file):
        print(f"错误: MOBI文件 '{mobi_file}' 不存在")
        return False
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查KindleUnpack目录是否存在
    script_dir = os.path.dirname(os.path.abspath(__file__))
    kindleunpack_dir = os.path.join(script_dir, 'KindleUnpack')
    kindleunpack_script = os.path.join(kindleunpack_dir, 'lib', 'kindleunpack.py')
    
    if not os.path.exists(kindleunpack_script):
        print("错误: 未找到KindleUnpack脚本")
        print("请先运行以下命令克隆KindleUnpack仓库:")
        print("  git clone https://github.com/kevinhendricks/KindleUnpack")
        return False
    
    # 创建临时目录用于解包
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"正在解包MOBI文件到临时目录...")
        
        try:
            # 使用subprocess调用kindleunpack命令行工具
            cmd = [sys.executable, kindleunpack_script, mobi_file, temp_dir]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # 查找图片文件
            image_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    # 常见图片格式
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        image_files.append(os.path.join(root, file))
            
            if not image_files:
                print("未找到任何图片")
                return True
            
            print(f"找到 {len(image_files)} 张图片，正在复制到输出目录...")
            
            # 复制图片到输出目录
            for i, image_path in enumerate(image_files, 1):
                # 生成新的文件名
                ext = os.path.splitext(image_path)[1]
                new_filename = f"image_{i:05d}{ext}"
                output_path = os.path.join(output_dir, new_filename)
                
                # 复制文件（保留原始尺寸和分辨率）
                shutil.copy2(image_path, output_path)
                print(f"  复制 {new_filename}")
            
            print(f"图片提取完成！所有图片已保存到: {output_dir}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"解包过程中出错: {e}")
            print(f"错误输出: {e.stderr}")
            return False
        except Exception as e:
            print(f"处理过程中出错: {e}")
            return False


def extract_images_from_epub(epub_file, output_dir):
    """
    从EPUB文件中提取图片
    
    Args:
        epub_file: EPUB文件路径
        output_dir: 图片输出目录
    """
    # 检查EPUB文件是否存在
    if not os.path.exists(epub_file):
        print(f"错误: EPUB文件 '{epub_file}' 不存在")
        return False
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建临时目录用于解压
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"正在解压EPUB文件到临时目录...")
        
        try:
            # 解压EPUB文件
            with zipfile.ZipFile(epub_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 查找图片文件
            image_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    # 常见图片格式
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        image_files.append(os.path.join(root, file))
            
            if not image_files:
                print("未找到任何图片")
                return True
            
            print(f"找到 {len(image_files)} 张图片，正在复制到输出目录...")
            
            # 复制图片到输出目录
            for i, image_path in enumerate(image_files, 1):
                # 生成新的文件名
                ext = os.path.splitext(image_path)[1]
                new_filename = f"image_{i:05d}{ext}"
                output_path = os.path.join(output_dir, new_filename)
                
                # 复制文件（保留原始尺寸和分辨率）
                shutil.copy2(image_path, output_path)
                print(f"  复制 {new_filename}")
            
            print(f"图片提取完成！所有图片已保存到: {output_dir}")
            return True
            
        except zipfile.BadZipFile:
            print(f"错误: '{epub_file}' 不是有效的EPUB文件")
            return False
        except Exception as e:
            print(f"处理过程中出错: {e}")
            return False


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="从MOBI或EPUB文件中提取图片")
    parser.add_argument("input_file", help="MOBI或EPUB文件路径")
    parser.add_argument("-o", "--output", help="图片输出目录", default="./book_images")
    
    args = parser.parse_args()
    
    # 根据文件扩展名选择提取方法
    file_ext = os.path.splitext(args.input_file)[1].lower()
    
    if file_ext in ('.mobi', '.azw', '.azw3'):
        # 执行MOBI图片提取
        success = extract_images_from_mobi(args.input_file, args.output)
    elif file_ext == '.epub':
        # 执行EPUB图片提取
        success = extract_images_from_epub(args.input_file, args.output)
    else:
        print(f"错误: 不支持的文件格式 '{file_ext}'")
        print("支持的格式: .mobi, .azw, .azw3, .epub")
        success = False
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()