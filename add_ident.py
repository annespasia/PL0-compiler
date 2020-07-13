import re

basic = ('if', 'begin', 'call', 'const', 'do', 'odd', 'procedure',
         'read', 'then', 'var', 'while', 'write', 'end')


def recog_adent(lines):
    idents = []
    idents1 = []
    for line in lines:
        idents.extend(re.findall(r'[a-z][a-z1-9]*', line))
    for item in idents:
        if item not in basic:
            idents1.append(item)
    return idents1


def count_ident(idents_list):
    idents_dict = {}
    for item in idents_list:
        if item in idents_dict:
            idents_dict[item] += 1
        else:
            idents_dict[item] = 1
    return idents_dict


def main():
    filenames = ('id_1.txt', 'case01.txt', 'case02.txt',
                 'case03.txt', 'case04.txt', 'case05.txt')
    fr_list = []
    lines = []
    idents_list = []
    idents_dict = {}

    for index in range(len(filenames)):
        with open('test/'+filenames[index], 'r', encoding='utf-8') as fr:
            print(fr)

            for line in fr:
                lines.append(line.strip().lower())
            idents_list = recog_adent(lines)
            # print(idents_list)
            idents_dict = count_ident(idents_list)
            # print(idents_dict)

            with open('result/1/'+filenames[index], 'w', encoding='utf-8') as fw:
                for key in idents_dict:
                    fw.write('('+str(key)+','+str(idents_dict[key])+')\n')

            lines.clear()
            idents_list.clear()
            idents_dict = {}


if __name__ == "__main__":
    main()
