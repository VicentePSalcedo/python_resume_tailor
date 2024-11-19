def find_and_replace(text, find_str, replace_str):
    print(f"replaced '{find_str}' with '{replace_str}'")
    return text.replace(find_str, replace_str)

def remove_blank_lines(file_path):
    with open(file_path, 'r+') as f:
        lines = f .readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()
    print(f"removed blank lines from {file_path}")
