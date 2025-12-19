#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修改xlsx文件中指定列数据的工具
功能：
1. 批量处理一个或多个xlsx文件
2. 修改指定列中的数据
3. 保留指定前缀和文件路径名，删除其他字符串
4. 支持命令行参数配置
5. 提供预览功能
6. 记录修改日志
"""

import os
import argparse
import pandas as pd
import sys
import re

def modify_xlsx_column(file_path, column_name, prefix, dry_run=False, verbose=True):
    """
    修改xlsx文件中指定列的数据
    
    Args:
        file_path (str): xlsx文件路径
        column_name (str): 要修改的列名
        prefix (str): 要保留的前缀
        dry_run (bool): 模拟修改，不实际保存
        verbose (bool): 显示详细信息
    
    Returns:
        tuple: (是否成功, 原数据数量, 修改的数据数量)
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 检查指定列是否存在
        if column_name not in df.columns:
            print(f"错误: 文件 '{file_path}' 中不存在列 '{column_name}'", file=sys.stderr)
            return False, 0, 0
        
        original_count = len(df)
        modified_count = 0
        
        # 定义修改函数
        def modify_cell(cell_value):
            nonlocal modified_count
            
            # 如果单元格为空，直接返回
            if pd.isna(cell_value):
                return cell_value
            
            # 将单元格值转换为字符串
            cell_str = str(cell_value)
            
            # 查找指定前缀
            prefix_pos = cell_str.find(prefix)
            if prefix_pos == -1:
                # 没有找到前缀，保持原样
                return cell_value
            
            # 提取前缀后面的部分
            content_after_prefix = cell_str[prefix_pos + len(prefix):]
            
            # 找到最后一个斜杠，提取文件名
            last_slash_pos = content_after_prefix.rfind('/')
            if last_slash_pos == -1:
                # 如果没有斜杠，检查是否有反斜杠
                last_slash_pos = content_after_prefix.rfind('\\')
            
            if last_slash_pos != -1:
                # 提取最后一个斜杠后面的文件名
                filename = content_after_prefix[last_slash_pos + 1:]
                # 如果文件名不为空，拼接前缀和文件名
                if filename.strip():
                    new_value = f"{prefix}{filename}"
                else:
                    # 如果文件名为空，只保留前缀
                    new_value = prefix
            else:
                # 如果没有找到斜杠，检查是否包含文件名（有扩展名）
                if '.' in content_after_prefix:
                    new_value = f"{prefix}{content_after_prefix}"
                else:
                    # 如果没有扩展名，只保留前缀
                    new_value = prefix
            
            # 如果值发生了变化，计数加1
            if new_value != cell_str:
                modified_count += 1
                if verbose:
                    print(f"修改 '{cell_str}' -> '{new_value}'")
            
            return new_value
        
        # 应用修改函数到指定列
        df[column_name] = df[column_name].apply(modify_cell)
        
        # 保存修改后的文件
        if not dry_run:
            df.to_excel(file_path, index=False)
            if verbose:
                print(f"已保存修改后的文件: {file_path}")
        
        return True, original_count, modified_count
        
    except Exception as e:
        print(f"处理文件 '{file_path}' 时出错: {e}", file=sys.stderr)
        return False, 0, 0

def batch_process_files(input_path, column_name, prefix, dry_run=False, verbose=True):
    """
    批量处理文件或目录
    
    Args:
        input_path (str): 文件路径或目录
        column_name (str): 要修改的列名
        prefix (str): 要保留的前缀
        dry_run (bool): 模拟修改，不实际保存
        verbose (bool): 显示详细信息
    
    Returns:
        dict: 处理结果统计
    """
    results = {
        'total_files': 0,
        'success_files': 0,
        'failed_files': 0,
        'total_records': 0,
        'modified_records': 0
    }
    
    # 处理单个文件
    if os.path.isfile(input_path) and input_path.endswith('.xlsx'):
        results['total_files'] = 1
        if verbose:
            print(f"\n处理文件: {input_path}")
        
        success, original_count, modified_count = modify_xlsx_column(
            input_path, column_name, prefix, dry_run, verbose
        )
        
        if success:
            results['success_files'] = 1
            results['total_records'] = original_count
            results['modified_records'] = modified_count
        else:
            results['failed_files'] = 1
    
    # 处理目录
    elif os.path.isdir(input_path):
        # 获取目录下所有xlsx文件
        xlsx_files = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.xlsx'):
                    xlsx_files.append(os.path.join(root, file))
        
        results['total_files'] = len(xlsx_files)
        
        if verbose:
            print(f"\n在目录 '{input_path}' 中找到 {len(xlsx_files)} 个xlsx文件")
        
        # 逐个处理文件
        for file_path in xlsx_files:
            if verbose:
                print(f"\n处理文件: {file_path}")
            
            success, original_count, modified_count = modify_xlsx_column(
                file_path, column_name, prefix, dry_run, verbose
            )
            
            if success:
                results['success_files'] += 1
                results['total_records'] += original_count
                results['modified_records'] += modified_count
            else:
                results['failed_files'] += 1
    
    else:
        print(f"错误: '{input_path}' 不是有效的文件或目录", file=sys.stderr)
        return None
    
    return results

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='批量修改xlsx文件中指定列数据的工具')
    parser.add_argument('input_path', help='xlsx文件路径或包含xlsx文件的目录')
    parser.add_argument('column_name', help='要修改的列名')
    parser.add_argument('prefix', help='要保留的字符串前缀')
    parser.add_argument('-d', '--dry-run', action='store_true', help='模拟修改，不实际保存')
    parser.add_argument('-q', '--quiet', action='store_true', help='安静模式，不显示详细信息')
    
    args = parser.parse_args()
    
    # 验证输入路径
    if not os.path.exists(args.input_path):
        print(f"错误: 路径 '{args.input_path}' 不存在！", file=sys.stderr)
        sys.exit(1)
    
    # 执行批量处理
    results = batch_process_files(
        args.input_path, 
        args.column_name, 
        args.prefix, 
        dry_run=args.dry_run, 
        verbose=not args.quiet
    )
    
    # 输出结果统计
    if results:
        action = "模拟修改" if args.dry_run else "实际修改"
        print(f"\n{action}完成:")
        print(f"- 总文件数: {results['total_files']}")
        print(f"- 成功处理: {results['success_files']}")
        print(f"- 处理失败: {results['failed_files']}")
        print(f"- 总记录数: {results['total_records']}")
        print(f"- 修改记录数: {results['modified_records']}")
        
        if args.dry_run:
            print("\n注意: 这是模拟修改，实际文件未被保存")

if __name__ == "__main__":
    main()
