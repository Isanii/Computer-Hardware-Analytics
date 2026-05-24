# -*- coding: utf-8 -*-
"""
dump_project_full.py

Dump toàn bộ project:
- In cây thư mục
- Dump source code
- Xuất ra project_dump.txt
- Hỗ trợ nhiều loại project

Chạy:
    python dump_project_full.py "D:\\Project"

Hoặc:
    python dump_project_full.py
"""

import os
import sys
import ctypes


# =========================================================
# CONFIG
# =========================================================

IGNORE_DIRS = {
    '.git',
    '.vs',
    'bin',
    'obj',
    '__pycache__',
    'node_modules',
    'venv',
    '.idea',
    '.vscode',
    'dist',
    'build',
    '.next',
    '.nuxt',
    '.cache'
}

ALLOW_EXTENSIONS = {

    # Python
    '.py',

    # .NET
    '.cs',
    '.csproj',
    '.sln',
    '.config',
    '.xaml',

    # Web
    '.html',
    '.css',
    '.scss',
    '.js',
    '.ts',
    '.tsx',
    '.jsx',

    # Config
    '.json',
    '.xml',
    '.yml',
    '.yaml',
    '.ini',
    '.env',

    # Database
    '.sql',

    # Text
    '.txt',
    '.md',
    '.csv',

    # Other languages
    '.php',
    '.java',
    '.kt',
    '.go',
    '.rs',
    '.cpp',
    '.c',
    '.h',

    # Git
    '.gitignore',
    '.gitattributes'
}

MEDIA_EXTENSIONS = {
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.svg',
    '.ico',
    '.webp',
    '.bmp'
}

SPECIAL_FILES = {
    '.env',
    '.gitignore',
    '.gitattributes'
}

OUTPUT_FILE = "project_dump.txt"


# =========================================================
# ADMIN
# =========================================================

def is_running_as_admin():

    if os.name != "nt":
        return False

    try:
        return bool(
            ctypes.windll.shell32.IsUserAnAdmin()
        )

    except Exception:
        return False


def relaunch_as_admin():

    if os.name != "nt":
        return

    if is_running_as_admin():
        return

    script = os.path.abspath(sys.argv[0])

    params = ' '.join(
        f'"{x}"'
        for x in [script] + sys.argv[1:]
    )

    try:

        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            params,
            None,
            1
        )

        sys.exit(0)

    except Exception as e:

        print("Không thể nâng quyền admin.")
        print("Lỗi:", e)

        sys.exit(1)


# =========================================================
# UTILS
# =========================================================

def write_line(text, file_handle=None):

    print(text)

    if file_handle:
        file_handle.write(text + "\n")


def get_language(ext):

    mapping = {

        '.py': 'python',
        '.cs': 'csharp',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'tsx',
        '.jsx': 'jsx',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.json': 'json',
        '.xml': 'xml',
        '.sql': 'sql',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.php': 'php',
        '.go': 'go',
        '.rs': 'rust',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.md': 'markdown'
    }

    return mapping.get(ext, '')


# =========================================================
# TREE
# =========================================================

def build_tree(root_path, out_file):

    def walk(current_dir, prefix=""):

        try:
            items = os.listdir(current_dir)

        except PermissionError:

            write_line(
                f"{prefix}└── [ACCESS DENIED]",
                out_file
            )

            return

        items = sorted(items, key=str.lower)

        filtered = []

        for item in items:

            full = os.path.join(current_dir, item)

            if os.path.isdir(full) and item in IGNORE_DIRS:
                continue

            filtered.append(item)

        for index, item in enumerate(filtered):

            full_path = os.path.join(current_dir, item)

            is_last = index == len(filtered) - 1

            connector = "└── " if is_last else "├── "

            write_line(
                f"{prefix}{connector}{item}",
                out_file
            )

            if os.path.isdir(full_path):

                extension = "    " if is_last else "│   "

                walk(
                    full_path,
                    prefix + extension
                )

    write_line("# PROJECT TREE", out_file)

    write_line("", out_file)

    write_line(
        os.path.basename(root_path),
        out_file
    )

    walk(root_path)

    write_line("", out_file)


# =========================================================
# SOURCE DUMP
# =========================================================

def dump_source_code(root_path, out_file):

    write_line("\n# SOURCE CODE\n", out_file)

    for root, dirs, files in os.walk(root_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:

            ext = os.path.splitext(file)[1].lower()

            file_path = os.path.join(root, file)

            rel_path = os.path.relpath(
                file_path,
                root_path
            )

            # =========================================
            # MEDIA FILE
            # =========================================

            if ext in MEDIA_EXTENSIONS:

                write_line(
                    "\n" + "=" * 100,
                    out_file
                )

                write_line(
                    f"FILE: {rel_path}",
                    out_file
                )

                write_line(
                    "=" * 100,
                    out_file
                )

                write_line(
                    "[MEDIA FILE - SKIPPED]",
                    out_file
                )

                continue

            # =========================================
            # CHECK EXTENSION
            # =========================================

            if (
                ext not in ALLOW_EXTENSIONS
                and file not in SPECIAL_FILES
            ):
                continue

            # =========================================
            # READ FILE
            # =========================================

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                write_line(
                    "\n" + "=" * 100,
                    out_file
                )

                write_line(
                    f"FILE: {rel_path}",
                    out_file
                )

                write_line(
                    "=" * 100,
                    out_file
                )

                lang = get_language(ext)

                write_line(
                    f"[LANGUAGE: {lang}]",
                    out_file
                )

                write_line("", out_file)

                out_file.write(content)

                if not content.endswith("\n"):
                    out_file.write("\n")

                write_line("", out_file)

                print(f"[OK] {rel_path}")

            except Exception as e:

                print(
                    f"[ERROR] {rel_path} -> {e}"
                )


# =========================================================
# MAIN
# =========================================================

def main():

    relaunch_as_admin()

    # ==========================================
    # GET PATH
    # ==========================================

    if len(sys.argv) >= 2:

        root_path = sys.argv[1]

    else:

        print("Nhập đường dẫn project:")
        print("Enter = dùng thư mục hiện tại")

        user_input = input("Path: ").strip()

        if user_input:
            root_path = user_input
        else:
            root_path = os.getcwd()

    root_path = os.path.abspath(root_path)

    if not os.path.isdir(root_path):

        print(f"❌ Không tồn tại thư mục: {root_path}")

        sys.exit(1)

    # ==========================================
    # OUTPUT FILE
    # ==========================================

    output_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        OUTPUT_FILE
    )

    # ==========================================
    # START
    # ==========================================

    try:

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as out_file:

            build_tree(
                root_path,
                out_file
            )

            dump_source_code(
                root_path,
                out_file
            )

        print("\n✅ Dump hoàn tất.")

        print(
            f"📄 File output: {output_path}"
        )

    except Exception as e:

        print("❌ Có lỗi:", e)

        sys.exit(1)


if __name__ == "__main__":
    main()
