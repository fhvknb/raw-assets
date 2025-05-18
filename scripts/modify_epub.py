from datetime import datetime
import time
import zipfile
import os
import tempfile
import shutil
import re

def extract_epub(epub_path, output_dir=None):
    """
    解压 EPUB 文件到指定目录
    
    参数:
    epub_path (str): EPUB 文件的路径
    output_dir (str, optional): 解压目标目录，如果不指定则创建临时目录
    
    返回:
    str: 解压后的目录路径
    """
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB 文件不存在: {epub_path}")
    
    # 如果没有指定输出目录，创建临时目录
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="epub_extracted_")
    else:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
    
    # 解压 EPUB 文件
    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        print(f"EPUB 文件已成功解压到: {output_dir}")
        return output_dir
    except Exception as e:
        print(f"解压 EPUB 文件时出错: {str(e)}")
        if output_dir.startswith(tempfile.gettempdir()):
            shutil.rmtree(output_dir, ignore_errors=True)
        raise

def repackage_epub(extracted_dir, output_epub_path=None):
    """
    将解压后的 EPUB 内容重新打包为 EPUB 文件
    
    参数:
    extracted_dir (str): 解压后的 EPUB 内容目录
    output_epub_path (str, optional): 输出的 EPUB 文件路径，如果不指定则基于原目录名生成
    
    返回:
    str: 新生成的 EPUB 文件路径
    """
    if not os.path.exists(extracted_dir):
        raise FileNotFoundError(f"解压目录不存在: {extracted_dir}")
    
    # 如果没有指定输出路径，基于解压目录名生成
    if output_epub_path is None:
        dir_name = os.path.basename(extracted_dir)
        # 移除可能的临时前缀
        dir_name = re.sub(r'^epub_extracted_', '', dir_name)
        output_epub_path = os.path.join(os.path.dirname(extracted_dir), f"{dir_name}.epub")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_epub_path)), exist_ok=True)
    current_time = time.time()
    zip_min_date = datetime(1980, 1, 1).timestamp()
    # 重新打包为 EPUB
    try:
        with zipfile.ZipFile(output_epub_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(extracted_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extracted_dir)
                    
                    # 获取文件的修改时间
                    file_mtime = os.path.getmtime(file_path)
                    
                    # 如果时间戳早于1980年，使用当前时间
                    if file_mtime < zip_min_date:
                        os.utime(file_path, (current_time, current_time))
                    
                    # 将文件添加到 ZIP
                    zipf.write(file_path, arcname)
        
        print(f"EPUB 文件已成功打包到: {output_epub_path}")
        return output_epub_path
    except Exception as e:
        print(f"打包 EPUB 文件时出错: {str(e)}")
        raise


if __name__ == "__main__":
  # process_epub_for_vertical_text('your_book.epub')
  repackage_epub('/Users/shawnxiang/Desktop/111di')
  pass