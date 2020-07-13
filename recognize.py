import re

words = {
    'basic': {
        'if': 'ifsym',
        'begin': 'beginsym',
        'call': 'callsym',
        'const': 'constsym',
        'do': 'dosym',
        'odd': 'oddsym',
        'procedure': 'proceduresym',
        'read': 'readsym',
        'then': 'thensym',
        'var': 'varsym',
        'while': 'whilesym',
        'write': 'writesym',
        'end': 'endsym'
    },
    'ident': [],
    'number': [],
    'calcu': {
        '+': 'plus',
        '-': 'minus',
        '*': 'times',
        '/': 'salsh',
        '=': 'eql',
        '#': 'neq',
        '<': 'lss',
        '<=': 'leq',
        '>': 'gtr',
        '>=': 'geq',
        ':=': 'becomes'
    },
    'border': {
        '(': 'lparen',
        ')': 'rparen',
        ',': 'comma',
        ';': 'semicolon',
        '.': 'period'
    }
}


def recog_words(lines):
    basic = re.compile(
        r'begin|call|const|do|end|if|odd|procedure|read|then|var|while|write')
    ident = re.compile(r'[a-z][a-z1-9]*')
    number = re.compile(r'\d+')
    calcu = re.compile(r'\+|-|\*|/|=|#|<|<=|>|>=|:=')
    border = re.compile(r'\(|\)|,|;|\.')
    whatever = re.compile(r'.+?')
    words_list = []
    for line in lines:
        while line != '':
            if basic.match(line):
                #start=0 if m==None else m.end()
                # m_b=basic.search(line,start)
                m = basic.match(line)
                # words_list.append((line[m.start():m.end()],m.start(),'basic'))
                words_list.append((line[m.start():m.end()], 'basic'))
                line = line[m.end():]
            elif ident.match(line):
                m = ident.match(line)
                words_list.append((line[m.start():m.end()], 'ident'))
                line = line[m.end():]
            elif number.match(line):
                m = number.match(line)
                words_list.append((line[m.start():m.end()], 'number'))
                line = line[m.end():]
            elif calcu.match(line):
                m = calcu.match(line)
                words_list.append((line[m.start():m.end()], 'calcu'))
                line = line[m.end():]
            elif border.match(line):
                m = border.match(line)
                words_list.append((line[m.start():m.end()], 'border'))
                line = line[m.end():]
            else:
                m = whatever.match(line)
                line = line[m.end():]
            # if m_i.end()==len(line) or m_br.end()==len(line) or m_b.end()==len(line) or m_n.end()==len(line) or m_c.end()==len(line):
            #     break
    return words_list


def main():
    filenames = ('1.txt', '2.txt','3.txt')
                 #'3.txt', '4.txt', '5.txt','6.txt','7.txt','8.txt','9.txt','10.txt')
    lines = []
    words_list = []
    #idents_dict = {}

    for index in range(len(filenames)):
        with open('test/3/'+filenames[index], 'r', encoding='utf-8') as fr:

            for line in fr:
                lines.append(line.strip().lower())
            lines = [x for x in lines if x != '']
            # print(lines)

            words_list = recog_words(lines)
            # print(words_list)

            with open('result/3/'+filenames[index], 'w', encoding='utf-8') as fw:
                for elem in words_list:
                    if elem[1] == 'basic' or elem[1] == 'calcu' or elem[1] == 'border':
                        fw.write(
                            '('+str(words[elem[1]][elem[0]])+','+str(elem[0])+')\n')
                    else:
                        fw.write('('+elem[1]+','+elem[0]+')\n')

            lines.clear()
            words_list.clear()


if __name__ == "__main__":
    main()
