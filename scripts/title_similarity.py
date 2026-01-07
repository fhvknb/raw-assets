#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标题相似度匹配工具

该工具用于分析Excel表格中的标题数据，识别相似的标题，并可以：
1. 将相似标题分组显示在新的Excel表格中
2. 按相似标题组的大小对原始数据行进行排序并重写原始文件

功能特点：
1. 支持中文标题的相似度匹配
2. 使用增强版Jaccard相似度算法，特别优化了系列标题识别
3. 智能预处理文本：
   - 只移除书名号，保留内容
   - 保留有意义的数字（如日期、版本号）
   - 移除括号及内容、特殊字符
4. 可调节相似度阈值
5. 支持按组大小降序排序原始数据
6. 智能排序组内标题（结合相似度和数字顺序）
7. 优化了4000+条数据的处理性能

优化亮点：
- 专门处理系列标题（如《航海的日常 0322》、《航海的日常 0325》等）
- 自动识别只有数字不同的相似标题
- 提高了长文本和复杂标题的匹配准确率

推荐参数设置：
- 系列标题较多时：threshold=0.7
- 严格匹配时：threshold=0.8
- 宽松匹配时：threshold=0.6

使用方法：
1. 确保已安装必要的依赖库：pandas, openpyxl, jieba
2. 将需要处理的Excel文件放在同一目录下

分组功能：
python title_similarity.py -i 输入文件.xlsx -o 结果文件.xlsx -t 0.7

重写原始文件功能（按组大小排序）：
python title_similarity.py -i 输入文件.xlsx -t 0.7 --rewrite

更多参数：
-h, --help: 显示帮助信息
-i, --input: 输入Excel文件路径
-o, --output: 输出文件路径（分组功能时必填）
-t, --threshold: 相似度阈值(0-1之间)，推荐0.7
-s, --sheet: Excel工作表名称或索引
-c, --column: 标题所在列的名称
-r, --rewrite: 是否重写原始文件
"""

import pandas as pd
import numpy as np
import jieba
import re
from collections import defaultdict

class TitleSimilarityMatcher:
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.stopwords = set()
        self.vectorizer = None
        self.tfidf_matrix = None
        self.titles = None
        self.preprocessed_titles = None
        
    def load_stopwords(self):
        # 使用默认的停用词表
        self.stopwords = set(['的', '了', '和', '是', '在', '我', '有', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
    
    def preprocess_text(self, text):
        # 移除文件扩展名
        text = re.sub(r'\.pdf$', '', text, flags=re.IGNORECASE)
        
        # 只移除书名号，保留内容
        text = re.sub(r'《', '', text)
        text = re.sub(r'》', '', text)
        
        # 移除特殊字符和标点，但保留空格
        text = re.sub(r'[\-_—\|\/\\，。、；：！？…·～～（）【】「」『』]', '', text)
        
        # 保留有意义的数字上下文，不盲目移除所有数字
        # text = re.sub(r'\d+', '', text)
        
        # 分词
        words = jieba.cut(text)
        
        # 移除停用词
        filtered_words = [word for word in words if word not in self.stopwords and word.strip()]
        
        return ' '.join(filtered_words)
    
    def load_data(self, file_path, sheet_name=0, column_name='标题'):
        # 读取Excel文件，指定engine参数
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        self.titles = df[column_name].tolist()
        
        # 预处理标题
        self.load_stopwords()
        self.preprocessed_titles = [self.preprocess_text(title) for title in self.titles]
        
        return df
    
    def calculate_similarity(self):
        # 计算增强版Jaccard相似度矩阵
        n = len(self.preprocessed_titles)
        similarity_matrix = np.zeros((n, n))
        
        # 将预处理后的标题转换为词集合
        title_sets = []
        for title in self.preprocessed_titles:
            words = set(title.split()) if title.strip() else set()
            title_sets.append(words)
        
        # 计算每对标题之间的相似度
        for i in range(n):
            for j in range(n):
                if i == j:
                    similarity_matrix[i][j] = 1.0
                else:
                    set_i = title_sets[i]
                    set_j = title_sets[j]
                    
                    # 处理空集合情况
                    if not set_i and not set_j:
                        similarity_matrix[i][j] = 1.0
                    elif not set_i or not set_j:
                        similarity_matrix[i][j] = 0.0
                    else:
                        # 基础Jaccard相似度
                        intersection = len(set_i & set_j)
                        union = len(set_i | set_j)
                        jaccard_sim = intersection / union
                        
                        # 增强逻辑：如果大部分词相同，只有数字不同，提高相似度
                        # 检查是否有数字差异
                        title_i = self.preprocessed_titles[i]
                        title_j = self.preprocessed_titles[j]
                        
                        # 移除数字后的比较
                        title_i_no_num = re.sub(r'\d+', '', title_i)
                        title_j_no_num = re.sub(r'\d+', '', title_j)
                        
                        # 如果移除数字后内容相同，相似度提高到0.9
                        if title_i_no_num == title_j_no_num and title_i_no_num.strip():
                            enhanced_sim = 0.9
                        # 如果有大部分重叠词，提高相似度
                        elif jaccard_sim > 0.3:
                            # 计算重叠词比例
                            overlap_ratio = intersection / min(len(set_i), len(set_j))
                            # 根据重叠比例动态调整相似度
                            enhanced_sim = min(0.95, jaccard_sim + (overlap_ratio * 0.3))
                        else:
                            enhanced_sim = jaccard_sim
                        
                        similarity_matrix[i][j] = enhanced_sim
        
        return similarity_matrix
    
    def group_similar_titles(self):
        similarity_matrix = self.calculate_similarity()
        
        # 初始化分组
        groups = defaultdict(list)
        used = set()
        group_id = 0
        
        # 分组逻辑：优先处理相似度高的标题对
        n = len(self.titles)
        
        # 首先创建预处理结果到索引的映射，确保相同预处理结果的标题被分到同一组
        preprocess_map = defaultdict(list)
        for idx, preprocessed in enumerate(self.preprocessed_titles):
            preprocess_map[preprocessed].append(idx)
        
        # 先处理完全相同的预处理结果组
        for identical_group in preprocess_map.values():
            if len(identical_group) > 1:
                # 检查是否有未使用的索引
                unused = [idx for idx in identical_group if idx not in used]
                if unused:
                    groups[group_id] = unused
                    used.update(unused)
                    group_id += 1
        
        # 然后处理相似但不完全相同的标题
        for i in range(n):
            if i not in used:
                # 找到所有相似的标题，包括部分相似的
                similar_indices = np.where(similarity_matrix[i] >= self.threshold)[0]
                
                # 过滤掉已使用的索引
                similar_indices = [idx for idx in similar_indices if idx not in used]
                
                if similar_indices:
                    groups[group_id] = similar_indices
                    used.update(similar_indices)
                    group_id += 1
        
        # 最后处理剩余的单个标题
        for i in range(n):
            if i not in used:
                groups[group_id] = [i]
                used.add(i)
                group_id += 1
        
        # 对每组内的标题进行智能排序
        sorted_groups = []
        for group in groups.values():
            if len(group) == 1:
                # 单个标题直接添加
                sorted_groups.append(group)
            else:
                # 对组内标题进行排序：先按相似度，再按原始顺序
                # 以组内第一个标题为基准
                base_idx = group[0]
                
                # 计算组内其他标题与基准标题的相似度
                group_similarities = []
                for idx in group:
                    # 获取标题中的数字部分
                    title = self.preprocessed_titles[idx]
                    numbers = re.findall(r'\d+', title)
                    num_val = int(numbers[0]) if numbers else 0
                    
                    # 结合相似度和数字顺序进行排序
                    similarity = similarity_matrix[base_idx][idx]
                    group_similarities.append((-similarity, num_val, idx))
                
                # 排序：相似度降序，数字升序
                group_similarities.sort()
                sorted_group = [idx for _, _, idx in group_similarities]
                sorted_groups.append(sorted_group)
        
        return sorted_groups
    
    def get_group_sizes(self):
        """
        获取每个标题索引对应的组大小
        返回一个字典：{索引: 组大小}
        """
        groups = self.group_similar_titles()
        group_size_dict = {}
        
        for group in groups:
            group_size = len(group)
            for idx in group:
                group_size_dict[idx] = group_size
        
        return group_size_dict
    
    def sort_original_df_by_group_size(self, original_df):
        """
        按相似标题组的大小对原始数据行进行排序
        组大小相同的行保持原顺序
        """
        # 获取每个索引的组大小
        group_size_dict = self.get_group_sizes()
        
        # 创建一个临时列用于排序和保持原顺序
        original_df['_group_size'] = original_df.index.map(group_size_dict)
        original_df['_original_index'] = original_df.index
        
        # 按组大小降序排序，组大小相同时保持原顺序
        sorted_df = original_df.sort_values(
            by=['_group_size', '_original_index'],
            ascending=[False, True]
        )
        
        # 移除临时列
        sorted_df = sorted_df.drop(['_group_size', '_original_index'], axis=1)
        
        return sorted_df
    
    def create_result_df(self, original_df):
        """
        创建保留所有原始列的分组结果DataFrame
        """
        groups = self.group_similar_titles()
        
        # 收集所有分组的索引
        all_indices = []
        for group in groups:
            all_indices.extend(group)
        
        # 使用原始索引重新排序DataFrame
        result_df = original_df.iloc[all_indices].reset_index(drop=True)
        
        return result_df

    def process_file(self, input_file, output_file=None, sheet_name=0, column_name='标题', rewrite_original=False):
        """
        处理Excel文件，按组大小排序并保存结果
        
        参数：
        input_file: 输入文件路径
        output_file: 输出文件路径（rewrite_original=False时必填）
        sheet_name: 工作表名称或索引
        column_name: 标题所在列的名称
        rewrite_original: 是否重写原始文件
        """
        # 加载数据
        original_df = self.load_data(input_file, sheet_name, column_name)
        
        if rewrite_original:
            # 使用分组结果排序原始数据，确保相似标题排在一起
            sorted_df = self.create_result_df(original_df)
            
            # 保存排序后的结果到原始文件
            sorted_df.to_excel(input_file, index=False, engine='openpyxl')
            
            print(f"处理完成！已重写原始文件 {input_file}")
            print(f"共找到 {len(self.group_similar_titles())} 组标题")
            
            return sorted_df
        else:
            # 创建分组结果
            result_df = self.create_result_df(original_df)
            
            # 保存结果
            result_df.to_excel(output_file, index=False)
            
            print(f"处理完成！结果已保存到 {output_file}")
            print(f"共找到 {len(self.group_similar_titles())} 组标题")
            
            return result_df


def main():
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='标题相似度匹配工具')
    parser.add_argument('-i', '--input', type=str, default='test_titles.xlsx', help='输入Excel文件路径')
    parser.add_argument('-o', '--output', type=str, default='similar_titles_result.xlsx', help='输出Excel文件路径（rewrite_original=False时必填）')
    parser.add_argument('-t', '--threshold', type=float, default=0.8, help='相似度阈值(0-1之间)')
    parser.add_argument('-s', '--sheet', type=str, default=0, help='Excel工作表名称或索引')
    parser.add_argument('-c', '--column', type=str, default='标题', help='标题所在列的名称')
    parser.add_argument('-r', '--rewrite', action='store_true', help='是否重写原始文件（默认：False）')
    
    # 解析参数
    args = parser.parse_args()
    
    # 创建匹配器实例
    matcher = TitleSimilarityMatcher(threshold=args.threshold)
    
    # 处理文件
    if args.rewrite:
        result_df = matcher.process_file(args.input, None, args.sheet, args.column, rewrite_original=True)
    else:
        result_df = matcher.process_file(args.input, args.output, args.sheet, args.column, rewrite_original=False)
    
    # 打印结果 
    print("\n处理结果预览：")
    print(result_df.head())

if __name__ == "__main__":
    main()