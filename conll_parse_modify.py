import os
import sys
import re


def replace_phrases_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            parts = line.split()
            if len(parts) > 5:
                # Replace all phrase types with 'X', except for 'TOP', 'S'
                parts[5] = re.sub(r'\b(ADJP|ADVP|FRAG|INTJ|NML|PP|PRT|QP|SBAR|SBARQ|SINV|SQ|UCP|VP|WHADVP|WHNP|NP|X)\b', 'X', parts[5])
            file.write(" ".join(parts) + "\n")


def process_files_in_directory(directory, file_suffix):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_suffix):
                file_path = os.path.join(root, file)
                replace_phrases_in_file(file_path)
                print(f"Processed file: {file_path}")


if len(sys.argv) != 3:
    print("Usage: python script.py directory file_suffix")
    print(r"Example: python conll_parse_modify.py D:\conll-2011\v2\data\dev .v2_auto_conll")
    sys.exit(1)

directory = sys.argv[1]
file_suffix = sys.argv[2]
#directory_path = r'D:\conll2011\conll-2011-dev.v2.tar\conll-2011-dev.v2\conll-2011\v2\data\dev'  # Replace with your directory path
#file_suffix = ".v2_auto_conll"
process_files_in_directory(directory, file_suffix)