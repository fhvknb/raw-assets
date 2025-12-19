# 批量删除指定后缀文件工具

## 功能介绍

这是一个用Python编写的批量删除指定后缀文件的工具，具有以下功能：

1. **递归遍历**：深度遍历指定目录及其所有子目录
2. **批量删除**：同时删除多种文件类型
3. **命令行支持**：灵活的参数配置
4. **安全机制**：
   - 模拟删除功能（dry run）
   - 删除前确认机制
5. **日志记录**：自动保存删除的文件列表
6. **详细反馈**：显示删除进度和结果统计

## 使用方法

### 基本语法

```bash
python3 batch_remove_files.py <根目录> <文件后缀1> <文件后缀2> ... [选项]
```

### 参数说明

- `<根目录>`：要遍历的根目录路径
- `<文件后缀>`：要删除的文件类型，如 `.jpg`、`.png`、`txt`（可省略点）
- `--dry-run` 或 `-d`：模拟删除，不实际执行
- `--quiet` 或 `-q`：安静模式，不显示详细信息

### 使用示例

#### 1. 查看帮助信息
```bash
python3 batch_remove_files.py --help
```

#### 2. 模拟删除指定目录下的所有.jpg文件
```bash
python3 batch_remove_files.py /path/to/folder .jpg -d
```

#### 3. 实际删除指定目录下的.jpg和.png文件
```bash
python3 batch_remove_files.py /path/to/folder .jpg .png
```

#### 4. 安静模式删除.txt文件
```bash
python3 batch_remove_files.py /path/to/folder txt -q
```

#### 5. 使用相对路径
```bash
python3 batch_remove_files.py ../images jpg png gif
```

## 安全特性

1. **模拟删除**：使用 `-d` 参数可以先查看将要删除的文件列表，而不实际删除
2. **确认机制**：实际删除前会提示用户确认，防止误操作
3. **详细日志**：删除的文件列表会保存到 `deleted_files.log` 文件中

## 注意事项

1. 请谨慎使用此工具，尤其是在系统目录或重要数据目录中
2. 建议先使用 `-d` 参数进行模拟删除，确认要删除的文件列表
3. 支持同时删除多种文件类型，如 `jpg png txt`
4. 文件后缀不区分大小写，`.JPG` 和 `.jpg` 都会被识别
5. 可以使用相对路径或绝对路径

## 运行环境

- Python 3.6+
- 无需安装额外依赖

## 示例输出

```
模拟删除 目录 '/Users/user/images' 下的 .jpg、.png 文件
共找到 2 种文件类型需要删除
找到 156 个文件需要删除

模拟删除完成:
- 总文件数: 156
- 成功删除: 0
- 删除失败: 0

注意: 这是模拟删除，实际文件未被删除
```

```
实际删除 目录 '/Users/user/images' 下的 .tmp、.bak 文件
共找到 2 种文件类型需要删除
找到 23 个文件需要删除
确定要删除这些文件吗？(y/N): y
准备删除: /Users/user/images/file1.tmp
准备删除: /Users/user/images/sub/folder/file2.bak
...

实际删除完成:
- 总文件数: 23
- 成功删除: 22
- 删除失败: 1

删除记录已保存到: deleted_files.log
```
