#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试批量修改XLSX文件工具的脚本
"""

import pandas as pd
import os
import sys

# 创建测试数据
data = {
    '文件路径': [
        '/Users/shawnxiang/Desktop/temp/zsxqscys/2023-2024生财有/0418-0422/风向标标王（3月），我的复盘与经验分享.pdf',
        'IMAGE:/path/to/image1.jpg (大小: 100KB)',
        '/data/documents/report_2023.pdf',
        '无前缀数据',
        'IMAGE:/another/path/photo2.png'
    ],
    '其他列': [
        '数据1',
        '数据2',
        '数据3',
        '数据4',
        '数据5'
    ]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为测试文件
test_file = 'test_data.xlsx'
df.to_excel(test_file, index=False)

print(f"创建测试文件: {test_file}")
print("测试数据:")
print(df)
print("\n")

# 导入我们的修改函数
from batch_modify_xlsx import modify_xlsx_column

# 测试1: 无固定前缀
print("=== 测试1: 无固定前缀 ===")
success, original_count, modified_count = modify_xlsx_column(
    test_file, 
    '文件路径', 
    '', 
    dry_run=True, 
    verbose=True
)

# 测试2: 有固定前缀
print("\n=== 测试2: 有固定前缀 'IMAGE:' ===")
success, original_count, modified_count = modify_xlsx_column(
    test_file, 
    '文件路径', 
    'IMAGE:', 
    dry_run=True, 
    verbose=True
)

# 删除测试文件
os.remove(test_file)
print(f"\n删除测试文件: {test_file}")
