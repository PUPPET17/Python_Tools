import os

def list_files(startpath):
    output = []
    for root, dirs, files in os.walk(startpath):
        # Skip 'node_modules' and 'target' directories
        if 'node_modules' in root.split(os.sep) or 'target' in root.split(os.sep):
            continue
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        output.append(f"{indent}├── {os.path.basename(root)}/")
        subindent = '│   ' * (level + 1)
        
        for i, f in enumerate(files):
            if i == len(files) - 1:
                output.append(f"{subindent}└── {f}")
            else:
                output.append(f"{subindent}├── {f}")
    
    return output

if __name__ == "__main__":
    directory_path = input("请输入目录路径: ")
    result = list_files(directory_path)
    
    output_file = "./OS_tools/directory_structure/directory_structure.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"目录结构: {directory_path}\n")
        f.write("=" * 50 + "\n")
        for line in result:
            f.write(line + "\n")
    
    print(f"目录结构已保存到 {output_file}")
