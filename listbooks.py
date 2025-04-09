import os
import urllib.parse
import re


def extract_sort_key(dirname):
    match = re.match(r"^(\d+)-", dirname)
    return int(match.group(1)) if match else float("inf")


def list_pdfs_in_markdown(base_path="."):
    dir_pdf_map = {}

    for root, _, files in os.walk(base_path):
        pdfs = [f for f in files if f.lower().endswith(".pdf")]
        if not pdfs:
            continue

        rel_dir = os.path.relpath(root, base_path)
        if rel_dir == ".":
            rel_dir = os.path.basename(os.getcwd())

        dir_pdf_map[rel_dir] = sorted(pdfs)

    # 排序目录（只排序第一层目录，子目录不影响排序）
    # sorted_dirs = sorted(dir_pdf_map.keys(), key=extract_sort_key)
    chinese_name_pairs = [
        ("01_programming", "编程"),
        ("02_algorithm", "算法"),
        ("03_operating_system", "操作系统"),
        ("04_network", "网络"),
        # ("05_database", "数据库"), # TODO:
        # ("06_ai", "人工智能"), # TODO:
        ("09_other", "其他"),
    ]

    markdown_lines = []
    for rel_dir, chinese_name in chinese_name_pairs:
        markdown_lines.append(f"### {chinese_name}")
        for pdf in dir_pdf_map[rel_dir]:
            pdf_path = os.path.join(rel_dir, pdf).replace("\\", "/")
            encoded_path = urllib.parse.quote(pdf_path)
            markdown_lines.append(f"  - [{pdf}]({encoded_path})")

    return "\n".join(markdown_lines)


if __name__ == "__main__":
    output = list_pdfs_in_markdown()
    print("# 计算机专业经典书籍")
    print("---")
    print(output)
