import os

def print_directory_tree(root_dir, prefix=""):
    contents = os.listdir(root_dir)
    pointers = [ '├── '] * (len(contents) - 1) + [ '└── ']
    for pointer, path in zip(pointers, contents):
        print(prefix + pointer + path)
        full_path = os.path.join(root_dir, path)
        if os.path.isdir(full_path):
            extension = '│   ' if pointer == '├── ' else '    '
            print_directory_tree(full_path, prefix + extension)

if __name__ == "__main__":
    root_directory = '.'  # Укажите здесь корневую папку вашего проекта
    print(root_directory)
    print_directory_tree(root_directory)
