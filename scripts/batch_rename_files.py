import os
import re

def batch_rename_files(folder_path, chars_to_remove, dry_run=True, process_subfolders=True):
    """
    批量重命名文件夹中的文件，删除文件名中的特定字符，可选择是否递归处理子文件夹
    
    参数:
    folder_path (str): 文件夹路径
    chars_to_remove (str or list): 需要删除的字符或字符列表
    dry_run (bool): 如果为True，只打印将要进行的更改而不实际执行
    process_subfolders (bool): 是否处理子文件夹中的文件
    
    返回:
    dict: 包含原文件名和新文件名的映射
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"提供的路径 '{folder_path}' 不是一个有效的文件夹")
    
    # 如果传入的是字符串，将其转换为列表
    if isinstance(chars_to_remove, str):
        chars_to_remove = list(chars_to_remove)
    
    # 创建正则表达式模式，用于删除指定字符
    pattern = '[' + re.escape(''.join(chars_to_remove)) + ']'
    
    renamed_files = {}
    
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # print(f"正在处理文件夹: {root}")

        # 处理当前文件夹中的文件
        for filename in files:
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            
            # 删除指定字符
            new_name = re.sub(pattern, '', name) + ext
            
            # 如果文件名没有变化，跳过
            if new_name == filename:
                continue
            
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_name)
            
            # 记录相对路径，方便查看
            rel_old_path = os.path.relpath(old_path, folder_path)
            rel_new_path = os.path.relpath(new_path, folder_path)
            renamed_files[rel_old_path] = rel_new_path
            
            if not dry_run:
                try:
                    # 检查新文件名是否已存在
                    if os.path.exists(new_path):
                        print(f"警告: 无法重命名 '{rel_old_path}' 为 '{rel_new_path}'，目标文件已存在")
                        continue
                    
                    # 重命名文件
                    os.rename(old_path, new_path)
                    print(f"已重命名: '{rel_old_path}' -> '{rel_new_path}'")
                except Exception as e:
                    print(f"重命名 '{rel_old_path}' 时出错: {str(e)}")
            else:
                print(f"将重命名: '{rel_old_path}' -> '{rel_new_path}'")
        
        # 如果不处理子文件夹，则跳出循环
        if not process_subfolders:
            break
    
    if dry_run:
        print(f"\n预览模式: 找到 {len(renamed_files)} 个文件需要重命名。设置 dry_run=False 以执行实际重命名操作。")
    else:
        print(f"\n完成: 已重命名 {len(renamed_files)} 个文件。")
    
    return renamed_files

# 使用示例
if __name__ == "__main__":
    folder_path = "/Users/shawnxiang/Downloads/157_web3"  # 替换为您的文件夹路径
    chars_to_remove = [' ', '【萌萌家】']
    # 先进行预览，包括子文件夹
    # batch_rename_files(folder_path, chars_to_remove, dry_run=True, process_subfolders=True)
    
    # 确认后执行实际重命名
    batch_rename_files(folder_path, chars_to_remove, dry_run=False, process_subfolders=True)
