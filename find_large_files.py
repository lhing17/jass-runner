import os

def find_large_python_files(root_dir, min_lines=300):
    print(f"Scanning directory: {root_dir}")
    print(f"Looking for Python files with more than {min_lines} lines...\n")
    
    large_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 忽略常见的虚拟环境和版本控制目录
        if 'venv' in dirnames:
            dirnames.remove('venv')
        if '.git' in dirnames:
            dirnames.remove('.git')
        if '__pycache__' in dirnames:
            dirnames.remove('__pycache__')
            
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        line_count = len(lines)
                        if line_count > min_lines:
                            large_files.append((file_path, line_count))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
    # 按行数降序排序
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    if large_files:
        print(f"{'Line Count':<12} | {'File Path'}")
        print("-" * 80)
        for file_path, line_count in large_files:
            # 简化路径显示，相对于 root_dir
            rel_path = os.path.relpath(file_path, root_dir)
            print(f"{line_count:<12} | {rel_path}")
    else:
        print("No Python files found exceeding the line limit.")

if __name__ == "__main__":
    # 使用脚本所在的目录作为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    find_large_python_files(current_dir)
