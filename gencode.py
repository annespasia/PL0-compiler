import re
from stack import stack

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
        '/': 'slash',
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


'''
<表达式> ::= [+|-]<项>{<加法运算符> <项>}
<项> ::= <因子>{<乘法运算符> <因子>}
<因子> ::= <标识符>|<无符号整数>| ‘(’<表达式>‘)’
<加法运算符> ::= +|-
<乘法运算符> ::= *|/
'''
count=0
file=0

def gen_code(calc,addr1,addr2):
    '''
    生成四元式形式的中间代码
    '''
    global count
    global file
    count+=1
    tar='addr'+str(count)
    with open('result/5/'+str(file)+'.txt', 'a', encoding='utf-8') as fw:
        fw.write('('+calc+','+addr1+','+addr2+','+'tar'+')\n')
    #print(str((calc,addr1,addr2,tar)))
    return tar


def ts(token_list, pos, addr):
    '''
    识别为乘法运算符
    '''
    elem = token_list[pos]
    if elem[0] == 'times':
        pos += 1
        temp = addr.pop()[1]
        # print('times received.'+str((True, pos, addr)))
    elif elem[0] == 'slash':
        pos += 1
        temp = addr.pop()[1]
        # print('slash received.'+str((True, pos, addr)))
    else:
        print('select: plz enter times or slash.')
        return (False, pos, addr)
    if pos >= len(token_list):
        print('should not end: plz enter ident or number or lparen.')
        return (False, pos, addr)
    flag = elem[0]
    elem = token_list[pos]
    # follow
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = factor(token_list, pos, addr)
        if result[0]:
            addr = result[2]
            if flag == 'times':
                #temp *= addr.pop()[1]
                temp=gen_code('*',temp,addr.pop()[1])
            elif flag == 'slash':
                # temp /= addr.pop()[1]
                temp=gen_code('/',temp,addr.pop()[1])
            addr.push(('T', temp))
            # print(addr)
        return result
    else:
        print('follow: plz enter ident or number or lparen.')
        return (False, pos, addr)


def pm(token_list, pos, addr):
    '''
    识别为加法运算符
    '''
    elem = token_list[pos]
    if elem[0] == 'plus':
        pos += 1
        temp = addr.pop()[1]
        # print('plus received.'+str((True, pos, addr)))
    elif elem[0] == 'minus':
        pos += 1
        temp = addr.pop()[1]
        # print('minus received.'+str((True, pos, addr)))
    else:
        print('select: plz enter plus or minus.')
        return (False, pos, addr)
    if pos >= len(token_list):
        print('should not end: plz enter ident or number or lparen.')
        return (False, pos, addr)
    flag = elem[0]
    elem = token_list[pos]
    # follow
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = term(token_list, pos, addr)
        if result[0]:
            addr = result[2]
            if flag == 'plus':
                #temp += addr.pop()[1]
                temp=gen_code('+',temp,addr.pop()[1])
            elif flag == 'minus':
                #temp -= addr.pop()[1]
                temp=gen_code('-',temp,addr.pop()[1])
            addr.push(('E', temp))
            # print(addr)
        return result
    else:
        print('follow: plz enter ident or number or lparen.')
        return (False, pos, addr)


def factor(token_list, pos, addr):
    '''
    识别为因子
    '''
    elem = token_list[pos]
    # select集+接收
    # F::=ident
    if elem[0] == 'ident':
        # 接收ident/number
        pos += 1
        temp=elem[1]
        # print('factor received.'+str((True, pos, addr)))
    # F::=number
    elif elem[0] == 'number':
        # 接收number
        pos += 1
        temp = elem[1]
        # print('factor received.'+str((True, pos, addr)))
    # F::=(E)
    elif elem[0] == 'lparen':
        # 接收lparen
        pos += 1
        if pos >= len(token_list):
            print('receiving: plz enter ident or number or lparen.')
            return (False, pos, addr)
        else:
            result = expression(token_list, pos, addr)
            if result[0]:
                pos = result[1]
                addr = result[2]
                temp = addr.pop()[1]
                elem = token_list[pos]
                # 接收)
                if elem[0] == 'rparen':
                    pos += 1
                    # print('factor received'+str((True, pos, addr)))
            else:
                return result
    else:
        print('select: plz enter ident or number or lparen.')
        return (False, 0, addr)
    # follow
    # 产生式左部入栈,获得值
    addr.push(('F', temp))
    # print(addr)
    if pos >= len(token_list):
        # 接收结束,返回上一层
        return (True, pos, addr)
    else:
        # 接收尚未结束
        elem = token_list[pos]
        if elem[0] == 'plus' or elem[0] == 'minus':
            # T的follow集,返回上一层决定
            return (True, pos, addr)
        elif elem[0] == 'times' or elem[0] == 'slash':
            # F的follow集
            result = ts(token_list, pos, addr)
            return result
        elif elem[0] == 'rparen':
            # E的follow集,返回上一层决定
            return (True, pos, addr)
        else:
            print('follow: plz enter plus or minus or times or slash or none.')
            return (False, pos, addr)


def term(token_list, pos, addr, flag=None):
    '''
    识别为项
    '''
    elem = token_list[pos]
    # select集正确
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = factor(token_list, pos, addr)
        # follow
        if result[0]:
            # 接收成功
            pos = result[1]
            # print('term received.'+str(result))
            addr = result[2]
            # 产生式右部内容出栈,传递值(加乘运算规约好了)
            temp = addr.pop()[1]
            # 产生式左部入栈,获得值
            if flag == 'minus':
                addr.push(('T', temp*(-1)))
            else:
                addr.push(('T', temp))
            # print(addr)
            if pos >= len(token_list):
                # 接收结束,返回上层
                return result
            else:
                # 接收尚未成功
                elem = token_list[pos]
                if elem[0] == 'plus' or elem[0] == 'minus':
                    # T的follow集
                    result = pm(token_list, pos, addr)
                    return result
                elif elem[0] == 'rparen':
                    # E的follow集,返回上层决定
                    return result
                else:
                    print('follow: plz enter plus or minus or rparen or none.')
                    return (False, pos, addr)
        else:
            return result
    # select集错误
    else:
        print('select: plz enter ident or number or lparen.')
        return (False, pos, addr)


def expression(token_list, pos, addr, flag=None):
    '''
    识别为表达式
    '''
    elem = token_list[pos]
    # select集正确
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        if flag == 'minus':
            result = term(token_list, pos, addr, flag)
        else:
            result = term(token_list, pos, addr)
        # follow集
        if result[0]:
            pos = result[1]
            # print('expression received.'+str(result))
            addr = result[2]
            # 产生式右部内容出栈,传递值(加乘运算规约好了)
            temp = addr.pop()[1]
            # 产生式左部入栈,获得值
            addr.push(('E', temp))
            # print(addr)
            if result[1] >= len(token_list):
                # 接收结束,返回上层
                return result
            else:
                elem = token_list[pos]
                if elem[0] == 'rparen':
                    # E的follow集
                    return result
                else:
                    print('follow: plz enter rparen or none.')
                    return (False, pos, addr)
        else:
            return result
    # select集错误
    else:
        print('select: plz enter ident or number or lparen.')
        return (False, pos, addr)


def gramma_analyze(token_list, pos, addr):
    '''
    试图识别表达式
    '''
    pos = 0
    flag = None
    elem = token_list[0]
    # 处理select集
    # 接收
    if elem[0] == 'plus' or elem[0] == 'minus':
        pos += 1
        flag = elem[0]
        # print('pm received.'+str((True, pos, addr)))
    elem = token_list[pos]
    # 处理select集
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        if flag == 'minus':
            result = expression(token_list, pos, addr, flag)
        else:
            result = expression(token_list, pos, addr)
        # follow集
        if result[0]:
            pos = result[1]
            # print('received.'+str(result))
            addr = result[2]
            # 产生式右部内容出栈,传递值
            temp = addr.pop()[1]
            # 产生式左部入栈,获得值
            addr.push(('S', temp))
            # print(addr)
            if pos >= len(token_list):
                return result
            else:
                print('follow: plz enter none.')
                return (False, pos, addr)
        else:
            return result
    # select集错误
    else:
        print('select: plz enter plus or minus or ident or number or lparen.')
        return (False, pos, addr)


def main():
    filenames = ('1.txt', '2.txt', '3.txt', '4.txt', '5.txt',
                 '6.txt', '7.txt', '8.txt', '9.txt', '10.txt')
    lines = []
    words_list = []
    token_list = []
    #idents_dict = {}
    result = (False, 0, 0)

    for index in range(len(filenames)):
        with open('test/5/'+filenames[index], 'r', encoding='utf-8') as fr:

            global file
            file+=1
            global count
            count=0

            for line in fr:
                lines.append(line.strip().lower())
            lines = [x for x in lines if x != '']
            # print(lines)

            words_list = recog_words(lines)
            # print(words_list)

            for elem in words_list:
                if elem[1] == 'basic' or elem[1] == 'calcu' or elem[1] == 'border':
                    token_list.append((words[elem[1]][elem[0]], elem[0]))
                else:
                    token_list.append((elem[1], elem[0]))
            print(token_list)
            addr = stack(len(token_list))

            result = gramma_analyze(token_list, 0, addr)
            if result[0]:
                print('语法正确,表达式的的位置在'+str(result[2].pop()[1]))
            else:
                print('语法错误,错误出自'+str(result[1])+'位置.')

            '''
            with open('result/2/'+filenames[index], 'w', encoding='utf-8') as fw:
                for elem in words_list:
                    if elem[1] == 'basic' or elem[1] == 'calcu' or elem[1] == 'border':
                        fw.write(
                            '('+str(words[elem[1]][elem[0]])+','+str(elem[0])+')\n')
                    else:
                        fw.write('('+elem[1]+','+elem[0]+')\n')
            '''

            lines.clear()
            token_list.clear()
            words_list.clear()
            addr.empty()


if __name__ == "__main__":
    main()
