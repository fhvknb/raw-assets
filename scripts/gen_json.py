#!/usr/bin/env python3
# coding=utf-8

"""
gen_json.py

改进版：
- 仅包含图片文件（默认扩展名集合，可由 `--exts` 覆盖）
- 支持批量生成：可以同时为多个目录生成 JSON，或使用关键字 `all` 处理根目录下的所有子目录
- 输出目录：`json/`（不存在则创建），每个目录输出一个 `<dirname>.json`

用法示例：
    python3 scripts/gen_json.py G_1024_A
    python3 scripts/gen_json.py G_1024_A G_1024_S
    python3 scripts/gen_json.py all
    python3 scripts/gen_json.py --exts jpg,png,webp --dry-run G_1024_A
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import List, Iterable, Set


DEFAULT_IMAGE_EXTS: Set[str] = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.svg', '.heic', '.heif'}


def parse_exts(exts: str | None) -> Set[str]:
    if not exts:
        return DEFAULT_IMAGE_EXTS
    parts = [p.strip().lower() for p in exts.split(',') if p.strip()]
    exts_set = set()
    for p in parts:
        if not p.startswith('.'):
            p = '.' + p
        exts_set.add(p)
    return exts_set


def gather_image_files(dirpath: Path, allowed_exts: Set[str]) -> List[str]:
    """递归收集目录下的图片文件，返回相对于仓库根的路径 (posix 风格)。"""
    out: List[str] = []
    for root, _, files in os.walk(dirpath):
        if Path(root).name.startswith('.'): 
            continue
        root_p = Path(root)
        for fn in files:
            p = root_p / fn
            if p.suffix.lower() in allowed_exts:
                # return path relative to repository root (one level above scripts)
                out.append(str(p.as_posix()))
    return out


def write_json(out_file: Path, paths: Iterable[str]) -> None:
    data = [{"imgSrc": p} for p in paths]
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='为指定目录生成图片列表 JSON 文件（仅图片，支持批量）')
    parser.add_argument('dirs', nargs='+', help='要处理的目录名，或使用关键字 `all` 表示根目录下的所有子目录')
    parser.add_argument('--exts', help='逗号分隔的扩展名列表，例如: jpg,png,webp （默认支持常见图片格式）')
    parser.add_argument('--dry-run', action='store_true', help='仅打印将要生成的文件，不实际写入')
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    json_dir = repo_root / 'json'

    allowed_exts = parse_exts(args.exts)

    # determine target directories
    requested = args.dirs
    dirs_to_process: List[Path] = []
    if len(requested) == 1 and requested[0].lower() == 'all':
        # all immediate subdirectories of repo_root (exclude 'json' and 'scripts')
        for p in sorted(repo_root.iterdir()):
            if p.is_dir() and p.name not in ('json', 'scripts'):
                dirs_to_process.append(p)
    else:
        for name in requested:
            p = repo_root / name
            if not p.exists() or not p.is_dir():
                print(f"跳过：找不到目录 {p}")
                continue
            dirs_to_process.append(p)

    if not dirs_to_process:
        print('未找到可处理的目录，退出。')
        return 2

    for d in dirs_to_process:
        rel_name = d.name
        print(f"处理目录: {rel_name} (允许扩展名: {sorted(allowed_exts)})")
        img_paths = gather_image_files(d, allowed_exts)
        if not img_paths:
            print(f"  未找到图片文件：{d}")
            continue
        out_file = json_dir / f"{rel_name}.json"
        if args.dry_run:
            print(f"  DRY-RUN -> 将写入 {out_file} (共 {len(img_paths)} 项)")
        else:
            write_json(out_file, img_paths)
            print(f"  已写入 {out_file} (共 {len(img_paths)} 项)")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

        
        
    



