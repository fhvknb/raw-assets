#!/usr/bin/env python3
"""
flatten_and_index.py

递归提取指定目录下所有子目录中的文件到最顶层目录，并把每个文件的文件名、原始路径、大小、创建时间和最后修改时间整理到一个 Excel 表中。

特性：
- 支持按扩展名过滤（可在命令行中自定义，例如: --exts jpg,png,txt）
- 支持复制（--copy）或移动（默认）操作
- 支持冲突重命名（自动加 _1/_2 等后缀）
- 支持删除空目录（--remove-empty）
- 支持 dry-run（不做实际移动/复制，只生成报表）

依赖：
- Python 3.8+
- openpyxl: `pip install openpyxl`

示例：
python3 scripts/flatten_and_index.py --root . --exts jpg,png --remove-empty
"""
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from datetime import datetime

try:
    from openpyxl import Workbook
except Exception as e:
    raise RuntimeError("Missing dependency 'openpyxl'. Install with: pip install openpyxl") from e


def parse_exts(exts: Optional[str]) -> Optional[set]:
    if not exts:
        return None
    parts = [p.strip().lower() for p in exts.split(",") if p.strip()]
    normalized = set()
    for p in parts:
        if p == "*":
            return None
        if not p.startswith("."):
            p = "." + p
        normalized.add(p)
    return normalized


def is_allowed(path: Path, allowed_exts: Optional[set]) -> bool:
    if allowed_exts is None:
        return True
    return path.suffix.lower() in allowed_exts


def get_times(p: Path) -> Tuple[str, str]:
    st = p.stat()
    # macOS: st_birthtime exists; fallback to st_ctime
    created = getattr(st, "st_birthtime", st.st_ctime)
    modified = st.st_mtime
    created_iso = datetime.fromtimestamp(created).isoformat(sep=" ", timespec="seconds")
    modified_iso = datetime.fromtimestamp(modified).isoformat(sep=" ", timespec="seconds")
    return created_iso, modified_iso


def unique_target(target_dir: Path, name: str) -> Path:
    target = target_dir / name
    if not target.exists():
        return target
    stem = Path(name).stem
    suffix = Path(name).suffix
    i = 1
    while True:
        new_name = f"{stem}_{i}{suffix}"
        candidate = target_dir / new_name
        if not candidate.exists():
            return candidate
        i += 1


def gather_files(root: Path, allowed_exts: Optional[set]) -> List[Path]:
    files = []
    for p in root.rglob("*"):
        if p.is_file():
            # skip files already in top-level root (don't reprocess if already flattened)
            if p.parent == root:
                continue
            if is_allowed(p, allowed_exts):
                files.append(p)
    return files


def write_excel(records: List[dict], out_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "file_index"
    headers = ["NewFilename", "OriginalPath", "SizeBytes", "Created", "Modified"]
    ws.append(headers)
    for r in records:
        ws.append([r["new_name"], r["orig_path"], r["size"], r["created"], r["modified"]])
    wb.save(out_path)


def remove_empty_dirs(root: Path) -> int:
    removed = 0
    # walk bottom-up
    for p in sorted(root.rglob("*"), key=lambda x: -len(str(x))):
        if p.is_dir():
            try:
                next(p.iterdir())
            except StopIteration:
                p.rmdir()
                removed += 1
    return removed


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Flatten subdirectories into root and generate Excel index")
    parser.add_argument("--root", "-r", default='.', help="Root directory to process")
    parser.add_argument("--exts", help="Comma-separated extensions to include (e.g. jpg,png). Use '*' or empty to include all")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving (default: move)")
    parser.add_argument("--dry-run", action="store_true", help="Do not perform move/copy, just generate report")
    parser.add_argument("--out", default="file_index.xlsx", help="Output Excel filename")
    parser.add_argument("--remove-empty", action="store_true", help="Remove empty directories after moving files")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Root not found or not a directory: {root}")
        return 2

    allowed_exts = parse_exts(args.exts)
    files = gather_files(root, allowed_exts)
    print(f"Found {len(files)} files to process")

    records = []
    for f in files:
        rel = f.relative_to(root)
        target = root / f.name
        if target.exists():
            target = unique_target(root, f.name)
        created, modified = get_times(f)
        size = f.stat().st_size
        records.append({
            "new_name": target.name,
            "orig_path": str(f),
            "size": size,
            "created": created,
            "modified": modified,
        })
        if args.dry_run:
            print(f"DRY: {f} -> {target.name}")
            continue

        # ensure target doesn't try to move file onto itself
        try:
            if args.copy:
                shutil.copy2(f, target)
            else:
                # move
                shutil.move(str(f), str(target))
        except Exception as e:
            print(f"Failed to move/copy {f} -> {target}: {e}")

    out_path = root / args.out
    write_excel(records, out_path)
    print(f"Wrote Excel report to {out_path}")

    removed = 0
    if args.remove_empty and not args.dry_run:
        removed = remove_empty_dirs(root)
        print(f"Removed {removed} empty directories")

    return 0



"""
使用说明

安装依赖：
pip install openpyxl

# 在仓库根目录运行：递归移动所有 jpg/png 文件到根目录并删除空目录
python3 scripts/flatten_and_index.py --root . --exts jpg,png --remove-empty

# 仅生成报告，不实际移动/复制
python3 scripts/flatten_and_index.py --root . --exts jpg,png --dry-run

# 复制而不是移动
python3 scripts/flatten_and_index.py --root . --exts jpg,png --copy

"""

if __name__ == "__main__":
    raise SystemExit(main())
