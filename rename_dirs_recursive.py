#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

REPLACEMENTS = {
    "евро-вилка": "eu",
    "под-переходник": "adapter",
}

def rename_dir_path(path: str) -> str:
    dirname, name = os.path.split(path)
    new_name = name
    for old, new in REPLACEMENTS.items():
        if old in new_name:
            new_name = new_name.replace(old, new)
    if new_name == name:
        return path
    return os.path.join(dirname, new_name)

def walk_and_rename_dirs(root: str, dry_run: bool = True) -> None:
    # ВАЖНО: topdown=False, чтобы сначала обработать вложенные каталоги
    for current_root, dirs, _files in os.walk(root, topdown=False):
        for d in dirs:
            old_dir_path = os.path.join(current_root, d)
            new_dir_path = rename_dir_path(old_dir_path)
            if new_dir_path != old_dir_path:
                if dry_run:
                    print(f"[DRY-RUN] DIR: {old_dir_path}  ->  {new_dir_path}")
                else:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"[RENAMED] DIR: {old_dir_path}  ->  {new_dir_path}")

def main():
    if len(sys.argv) < 2:
        print("Использование: python rename_dirs_recursive.py /path/to/root [--apply]")
        print("По умолчанию выполняется dry-run (только вывод изменений).")
        sys.exit(1)

    root = sys.argv[1]
    dry_run = "--apply" not in sys.argv[2:]

    if not os.path.isdir(root):
        print(f"Ошибка: '{root}' не является каталогом")
        sys.exit(1)

    print(f"Старт из: {root}")
    print("Режим: DRY-RUN (ничего не меняет)" if dry_run else "Режим: APPLY (будут переименования)")
    walk_and_rename_dirs(root, dry_run=dry_run)

if __name__ == "__main__":
    main()

