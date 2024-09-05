import sys
import string
import os
import fnmatch


def is_all_punctuation(s):
    punctuation_set = set(string.punctuation)
    if not s:
        return False
    return all(char in punctuation_set for char in s)


def process_file(input_file):
    j = 0
    flag = 0
    count = 0
    record = []
    sentence = []
    redflag = 0
    last_word = []

    total_words = 0  # n
    modified_words = 0  # m
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()

    with open(input_file, 'w', encoding='utf-8') as f_out:
        for i in range(len(lines)):
            line = lines[i].rstrip()

            if line:
                words = line.split()
                total_words += 1

                sentence.append(words[0])
                if words[0] in ['.', '!', '?', '...']:
                    if redflag == 1:
                        print(' '.join(sentence) + '\n' + '\n')
                    redflag = 0
                    sentence = []
                if len(words) >= 3 and words[4] in ['JJ', 'JJS', 'JJR']:
                    if i >= 2 and len(lines[i - 1].split()) > 4:
                        last_word = lines[i - 1].split()
                        if flag == 0 and last_word[4] != 'DT':
                            f_out.write(lines[i])
                            continue
                        flag = 0
                        if words[4] == 'RB':
                            flag = 1
                            f_out.write(lines[i])
                            continue

                    if (i + 1 < len(lines) and lines[i + 1].strip() and
                            lines[i + 1].split()[4][0] != 'N' and
                            lines[i + 1].split()[4] not in ['JJ', 'CD', 'CC', '$', '``', '-LRB-', '-RRB-', 'JJS', 'JJR', '\'\'', 'RB', '#', 'RBS', 'RBR'] and
                            lines[i + 1].split()[3] != 'half' and lines[i + 1].split()[3] != '-'):
                        if len(last_word) > 3 and last_word[3] == 'as' and lines[i + 1].split()[0]:
                            f_out.write(lines[i])
                            continue

                        if ((i + 2) < len(lines) and lines[i + 2].strip()):
                            if (lines[i + 2].split()[4] in ['JJ', 'JJS', 'JJR', 'RBR', 'RBS', '$'] and
                                    lines[i + 1].split()[3] == ','):
                                f_out.write(lines[i])
                                continue
                            if lines[i + 1].split()[4] in ['VBG', 'VBD', 'VBN']:
                                if lines[i + 2].split()[4][0] == 'N':
                                    f_out.write(lines[i])
                                    continue
                                if lines[i + 2].split()[3] == ',':
                                    f_out.write(lines[i])
                                    continue
                                if lines[i + 2].split()[4] == 'JJ':
                                    f_out.write(lines[i])
                                    continue

                        words[4] = 'NN'
                        modified_words += 1

                        formatted_line = "\t".join(words) + '\n'
                        f_out.write(formatted_line)
                        j += 1
                        record.append(i)
                        sentence.append(str(i))
                        redflag = 1

                    else:
                        f_out.write(lines[i])
                else:
                    f_out.write(lines[i])
            else:
                f_out.write('\n')

    #print(count)
    print(f"processed, results at {input_file}")
    #print(len(lines))
    #print(record)

    return total_words, modified_words


def process_directory(directory, file_suffix):
    nn = 0
    mm = 0
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, f'*{file_suffix}'):
            input_file = os.path.join(root, filename)
            tw, mw = process_file(input_file)
            nn += tw
            mm += mw
    print(f"Total words (n): {nn}")
    print(f"Modified words (m): {mm}")
    if nn > 0:
        print(f"Proportion (m/n): {mm / nn:.5f}")
    else:
        print("No words processed.")



if len(sys.argv) != 3:
    print("Usage: python script.py directory file_suffix")
    print(r"Example: python conll_pos_modify.py D:\conll-2011\v2\data\dev .v2_auto_conll")
    sys.exit(1)

directory = sys.argv[1]
file_suffix = sys.argv[2]
#directory = r"D:\conll2011\conll-2011-dev.v2.tar\conll-2011-dev.v2\conll-2011\v2\data\dev"
#file_suffix = r".v2_auto_conll"
process_directory(directory, file_suffix)