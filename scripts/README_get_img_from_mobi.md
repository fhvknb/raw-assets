# MOBI图片提取工具使用说明

## 功能介绍
本工具用于从MOBI格式的电子书文件中提取所有图片，并保持图片的原始尺寸和最佳分辨率。

## 安装依赖
由于`kindleunpack`库无法通过pip直接安装，需要从GitHub克隆仓库：

```bash
cd /Users/shawnxiang/Ethan/Codes/Personal/raw-assets/scripts/
git clone https://github.com/kevinhendricks/KindleUnpack.git
```

## 使用方法

### 基本用法
```bash
python get_img_from_mobi.py <mobi文件路径>
```

例如：
```bash
python get_img_from_mobi.py book.mobi
```

这将在当前目录创建一个`mobi_images`文件夹，并将所有提取的图片保存到该文件夹中。

### 指定输出目录
使用`-o`或`--output`参数可以指定图片的输出目录：

```bash
python get_img_from_mobi.py <mobi文件路径> -o <输出目录>
```

例如：
```bash
python get_img_from_mobi.py book.mobi -o ./extracted_images
```

## 注意事项
1. 本工具仅支持未加密的MOBI文件
2. 提取的图片将保持原始尺寸和分辨率
3. 图片将以`image_00001.jpg`、`image_00002.png`等格式命名
4. 支持的图片格式包括：JPG、JPEG、PNG、GIF、BMP

## 示例

```bash
# 提取book.mobi中的图片到默认目录
python get_img_from_mobi.py book.mobi

# 提取book.mobi中的图片到指定目录
python get_img_from_mobi.py book.mobi -o ./my_images
```

## 故障排除

### 找不到KindleUnpack脚本
如果遇到"未找到KindleUnpack脚本"错误，请确保已正确克隆KindleUnpack仓库：

```bash
cd /Users/shawnxiang/Ethan/Codes/Personal/raw-assets/scripts/
git clone https://github.com/kevinhendricks/KindleUnpack.git
```

### 解包过程中出错
如果在解包过程中遇到错误，请检查：
1. MOBI文件是否完好无损
2. MOBI文件是否未加密
3. 您是否有足够的权限读取MOBI文件和写入输出目录

## 工作原理
本工具使用以下步骤提取图片：
1. 检查KindleUnpack仓库是否存在
2. 创建临时目录用于解包
3. 使用subprocess调用kindleunpack脚本解包MOBI文件
4. 在解包后的文件中搜索图片文件
5. 将所有图片复制到指定的输出目录
6. 清理临时目录

如果解包过程中遇到其他错误，可能是因为MOBI文件已加密或格式不受支持。