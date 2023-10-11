# # Importing Libraries
# from directory_tree import display_tree

# DirectoryPath = (
# "0tR6N3pFDzpMhP9CVNJvH388JThDZVnjUvcVDzFvSBlXrxnNQ2RwA7vh"
# "WjqcG95VkiOazhpciKaRACDbej0QgA=="
# )
# # Main Method
# if __name__ == "__main__":
#     display_tree(DirectoryPath)

import os


def display_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in sorted(files):
            print(f"{subindent}{f}")
        # This ensures that we don't display all the nested content of '.git' directory
        if ".git" in dirs:
            dirs.remove(".git")


# Main Method
if __name__ == "__main__":
    DirectoryPath = (
        "0tR6N3pFDzpMhP9CVNJvH388JThDZVnjUvcVDzFvSBlXrxnNQ2RwA7vh"
        "WjqcG95VkiOazhpciKaRACDbej0QgA=="
    )
    print(f"{os.path.basename(DirectoryPath)}/")
    display_directory_structure(DirectoryPath)
