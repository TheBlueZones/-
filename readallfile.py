import os
import sys


def combine_files_content():
    # 获取当前脚本的绝对路径
    current_script = os.path.abspath(__file__)
    # 获取当前目录
    current_dir = os.path.dirname(current_script)
    # 输出文件名
    output_file = "combined_content.txt"

    # 要读取的文件扩展名
    valid_extensions = ['.py', '.txt', '.html', '.css', '.js', '.json', '.md']

    # 要排除的文件列表
    exclude_files = [
        output_file,
        os.path.basename(current_script),
        "__pycache__",
        ".git",
        ".idea"
    ]

    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 遍历当前目录及子目录下的所有文件
        for root, dirs, files in os.walk(current_dir):
            # 排除特定目录
            dirs[:] = [d for d in dirs if d not in exclude_files]

            for filename in files:
                # 检查文件是否需要被排除
                if any(exclude in filename for exclude in exclude_files):
                    continue

                # 检查文件扩展名
                if not any(filename.endswith(ext) for ext in valid_extensions):
                    continue

                # 获取完整的文件路径
                filepath = os.path.join(root, filename)
                try:
                    # 读取每个文件的内容
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        # 写入相对路径作为标识
                        rel_path = os.path.relpath(filepath, current_dir)
                        outfile.write(f"\n=== {rel_path} ===\n")
                        # 写入文件内容
                        outfile.write(infile.read())
                        outfile.write("\n")
                except Exception as e:
                    print(f"Error reading {filename}: {str(e)}")


if __name__ == "__main__":
    combine_files_content()
    print("文件合并完成，请查看 combined_content.txt")