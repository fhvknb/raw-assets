#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量删除指定后缀的文件工具
功能：
1. 递归遍历指定文件夹
2. 批量删除符合条件的文件后缀
3. 提供命令行参数支持
4. 添加确认机制，防止误删
5. 记录删除的文件列表
"""

import os
import argparse
import sys

def batch_remove_files(root_dir, extensions, dry_run=False, verbose=True):
    """
    递归遍历文件夹并删除指定后缀的文件
    
    Args:
        root_dir (str): 要遍历的根目录
        extensions (list): 要删除的文件后缀列表，如 ['.jpg', '.png']
        dry_run (bool): 模拟删除，不实际执行
        verbose (bool): 显示详细信息
    
    Returns:
        tuple: (删除的文件数量, 删除的文件列表)
    """
    # 确保扩展名为小写且以点开头
    extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]
    
    deleted_count = 0
    deleted_files = []
    
    # 递归遍历文件夹
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # 获取文件扩展名
            _, ext = os.path.splitext(file)
            if ext.lower() in extensions:
                file_path = os.path.join(root, file)
                deleted_files.append(file_path)
                
                if verbose:
                    print(f"准备删除: {file_path}")
                
                if not dry_run:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"删除失败 {file_path}: {e}", file=sys.stderr)
    
    return deleted_count, deleted_files

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='批量删除指定后缀的文件工具')
    parser.add_argument('root_dir', help='要遍历的根目录路径')
    parser.add_argument('extensions', nargs='+', help='要删除的文件后缀，如 .jpg .png')
    parser.add_argument('-d', '--dry-run', action='store_true', help='模拟删除，不实际执行')
    parser.add_argument('-q', '--quiet', action='store_true', help='安静模式，不显示详细信息')
    
    args = parser.parse_args()
    
    # 验证根目录是否存在
    if not os.path.exists(args.root_dir):
        print(f"错误: 目录 '{args.root_dir}' 不存在！", file=sys.stderr)
        sys.exit(1)
    
    # 打印删除信息
    action = "模拟删除" if args.dry_run else "实际删除"
    print(f"{action} 目录 '{args.root_dir}' 下的 {'、'.join(args.extensions)} 文件")
    print(f"共找到 {len(args.extensions)} 种文件类型需要删除")
    
    # 获取要删除的文件列表（先执行dry run获取列表）
    _, files_to_delete = batch_remove_files(args.root_dir, args.extensions, dry_run=True, verbose=False)
    
    if not files_to_delete:
        print("没有找到符合条件的文件")
        sys.exit(0)
    
    print(f"找到 {len(files_to_delete)} 个文件需要删除")
    
    # 确认删除
    if not args.dry_run:
        confirm = input("确定要删除这些文件吗？(y/N): ")
        if confirm.lower() != 'y':
            print("取消删除操作")
            sys.exit(0)
    
    # 执行删除
    deleted_count, deleted_files = batch_remove_files(
        args.root_dir, 
        args.extensions, 
        dry_run=args.dry_run, 
        verbose=not args.quiet
    )
    
    # 输出结果
    print(f"\n{action}完成:")
    print(f"- 总文件数: {len(files_to_delete)}")
    print(f"- 成功删除: {deleted_count}")
    print(f"- 删除失败: {len(files_to_delete) - deleted_count}")
    
    if args.dry_run:
        print("\n注意: 这是模拟删除，实际文件未被删除")
    
    # 保存删除记录
    if deleted_files and not args.dry_run:
        log_file = 'deleted_files.log'
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                for file in deleted_files:
                    f.write(f"{file}\n")
            print(f"\n删除记录已保存到: {log_file}")
        except Exception as e:
            print(f"\n保存删除记录失败: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
