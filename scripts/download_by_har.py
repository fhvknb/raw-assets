import json
import requests
import os
import re
from urllib.parse import urlparse, unquote
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('download_har.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class HarDownloader:
    def __init__(self, har_file_path, output_dir):
        """初始化下载器"""
        self.har_file_path = har_file_path
        self.output_dir = output_dir
        self.download_count = 0
        self.skip_count = 0
        self.error_count = 0
        
    def clean_url_params(self, url):
        """移除URL中的版本参数等查询字符串"""
        # 使用正则表达式匹配URL中的查询参数部分
        base_url = re.sub(r'\?.*$', '', url)
        return base_url
        
    def get_file_path_from_url(self, url):
        """从URL中提取文件路径和文件名"""
        # 移除URL参数
        clean_url = self.clean_url_params(url)
        
        # 解析URL
        parsed_url = urlparse(clean_url)
        path = unquote(parsed_url.path)  # URL解码
        
        # 处理路径
        if path.endswith('/'):
            path += 'index.html'
            
        # 分离目录和文件名
        path_parts = path.lstrip('/').split('/')
        file_name = path_parts[-1]
        
        # 如果文件名为空或只包含特殊字符，生成默认名称
        if not file_name or not "".join(c for c in file_name if c.isalnum()):
            file_name = f"resource_{self.download_count}.bin"
            path_parts[-1] = file_name
            
        # 处理文件名中的特殊字符
        file_name = "".join(c for c in file_name if c.isalnum() or c in ('.', '_', '-'))
        path_parts[-1] = file_name
        
        # 构建相对路径
        relative_path = os.path.join(*path_parts)
        
        # 完整的保存路径
        full_path = os.path.join(self.output_dir, relative_path)
        
        return full_path
        
    def ensure_directory_exists(self, file_path):
        """确保文件目录存在"""
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        
    def download_file(self, url, file_path):
        """下载文件并保存到指定路径"""
        try:
            res = requests.get(url, stream=True, timeout=10)
            if res.status_code == 200:
                with open(file_path, 'wb') as out_file:
                    for chunk in res.iter_content(chunk_size=8192):
                        out_file.write(chunk)
                return True
            else:
                logger.error(f"下载失败（{res.status_code}）: {url}")
                self.error_count += 1
                return False
        except requests.RequestException as e:
            logger.error(f"请求错误: {e} - {url}")
            self.error_count += 1
            return False
        except Exception as e:
            logger.error(f"处理文件时出错: {e} - {url}")
            self.error_count += 1
            return False
            
    def process_har(self):
        """处理HAR文件并下载资源"""
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 解析HAR文件
        try:
            with open(self.har_file_path, 'r', encoding='utf-8') as f:
                har_data = json.load(f)
        except Exception as e:
            logger.error(f"解析HAR文件失败: {e}")
            return
            
        # 提取请求
        entries = har_data['log']['entries']
        logger.info(f"共找到 {len(entries)} 个请求")
        
        # 遍历请求并下载
        for entry in entries:
            request = entry['request']
            response = entry['response']
            
            url = request['url']
            status = response['status']
            
            # 只下载成功的请求
            if status == 200:
                try:
                    # 获取保存路径
                    file_path = self.get_file_path_from_url(url)
                    
                    # 检查是否已经下载过
                    if os.path.exists(file_path):
                        logger.info(f"文件已存在: {file_path}")
                        self.skip_count += 1
                        continue
                        
                    # 确保目录存在
                    self.ensure_directory_exists(file_path)
                    
                    # 下载文件
                    logger.info(f"正在下载: {url} -> {file_path}")
                    if self.download_file(url, file_path):
                        self.download_count += 1
                        
                except Exception as e:
                    logger.error(f"处理请求时出错: {e} - {url}")
                    self.error_count += 1
            else:
                logger.debug(f"跳过非200状态码请求: {url} (Status: {status})")
                
        # 打印统计信息
        logger.info(f"下载完成！成功: {self.download_count}, 跳过: {self.skip_count}, 错误: {self.error_count}")

def main():
    """主函数"""
    # 配置文件路径
    har_file_path = '/Users/shawnxiang/Ethan/Codes/Personal/raw-assets/scripts/t00y.com.har'
    output_dir = '/Users/shawnxiang/Ethan/Codes/Personal/raw-assets/scripts/t00y_source'
    
    # 创建下载器并执行
    downloader = HarDownloader(har_file_path, output_dir)
    downloader.process_har()

if __name__ == "__main__":
    main()