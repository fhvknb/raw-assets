# 电子书图片提取工具使用说明

## 功能介绍
本工具用于从MOBI或EPUB格式的电子书文件中提取所有图片，并保持图片的原始尺寸和最佳分辨率。

### 支持的文件格式
- MOBI系列格式：`.mobi`, `.azw`, `.azw3`
- EPUB格式：`.epub`

## 安装依赖
由于`kindleunpack`库无法通过pip直接安装，需要从GitHub克隆仓库：

```bash
cd /Users/shawnxiang/Ethan/Codes/Personal/raw-assets/scripts/
git clone https://github.com/kevinhendricks/KindleUnpack.git
```

## 使用方法

### 基本用法
```bash
python get_img_from_mobi.py <input_file>
```

例如：
```bash
# 提取MOBI文件中的图片
python get_img_from_mobi.py book.mobi

# 提取EPUB文件中的图片  
python get_img_from_mobi.py book.epub
```

这将在当前目录创建一个`book_images`文件夹，并将所有提取的图片保存到该文件夹中。

### 指定输出目录
使用`-o`或`--output`参数可以指定图片的输出目录：

```bash
python get_img_from_mobi.py <input_file> -o <输出目录>
```

例如：
```bash
# 提取MOBI文件到指定目录
python get_img_from_mobi.py book.mobi -o ./mobi_images

# 提取EPUB文件到指定目录
python get_img_from_mobi.py book.epub -o ./epub_images
```

## 注意事项
1. 本工具仅支持未加密的MOBI和EPUB文件
2. 提取的图片将保持原始尺寸和分辨率
3. 图片将以`image_00001.jpg`、`image_00002.png`等格式命名
4. 支持的图片格式包括：JPG、JPEG、PNG、GIF、BMP

## 示例

```bash
# 提取MOBI文件中的图片到默认目录
python get_img_from_mobi.py book.mobi
# 图片将保存到 ./book_images 目录

# 提取EPUB文件中的图片到默认目录
python get_img_from_mobi.py book.epub
# 图片将保存到 ./book_images 目录

# 提取MOBI文件中的图片到指定目录
python get_img_from_mobi.py book.mobi -o ./mobi_images

# 提取EPUB文件中的图片到指定目录
python get_img_from_mobi.py book.epub -o ./epub_images
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
1. 文件是否完好无损
2. 文件是否未加密（本工具不支持加密的MOBI/EPUB文件）
3. 您是否有足够的权限读取输入文件和写入输出目录
4. 文件格式是否正确（请确认文件扩展名与实际格式一致）

## 工作原理

### MOBI文件提取流程
1. 检查KindleUnpack仓库是否存在
2. 创建临时目录用于解包
3. 使用subprocess调用kindleunpack脚本解包MOBI文件
4. 在解包后的文件中搜索图片文件
5. 将所有图片复制到指定的输出目录
6. 清理临时目录

### EPUB文件提取流程
1. 创建临时目录用于解压
2. 使用zipfile模块解压EPUB文件（EPUB本质是ZIP格式）
3. 在解压后的文件中搜索图片文件
4. 将所有图片复制到指定的输出目录
5. 清理临时目录

### 不支持的文件格式
如果遇到"不支持的文件格式"错误，请确保文件扩展名正确且是支持的格式：
- MOBI系列：.mobi, .azw, .azw3
- EPUB系列：.epub

如果解包过程中遇到其他错误，可能是因为文件已加密或格式不受支持。