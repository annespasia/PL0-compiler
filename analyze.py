import re
import stack

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
<条件语句> → IF <条件> THEN <语句> 
<条件> → <表达式> <关系运算符> <表达式>
<关系运算符>  → > | < | =
<语句> → <id> := <表达式>
<表达式> ::= [+|-]<项>{<加法运算符> <项>}
<项> ::= <因子>{<乘法运算符> <因子>}
<因子> ::= <标识符>|<无符号整数>| ‘(’<表达式>‘)’
<加法运算符> ::= +|-
<乘法运算符> ::= *|/
'''


def ts(token_list, pos):
    '''
    识别为乘法运算符
    '''
    elem = token_list[pos]
    if elem[0] == 'times':
        pos += 1
        print('times received.'+str((True, pos)))
    elif elem[0] == 'slash':
        pos += 1
        print('slash received.'+str((True, pos)))
    else:
        print('select: plz enter times or slash.')
        return (False, pos)
    if pos >= len(token_list):
        return (False, pos)
    elem = token_list[pos]
    # follow
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = factor(token_list, pos)
        return result
    else:
        print('follow: plz enter ident or number or lparen.')
        return (False, pos)


def pm(token_list, pos):
    '''
    识别为加法运算符
    '''
    elem = token_list[pos]
    if elem[0] == 'plus':
        pos += 1
        print('plus received.'+str((True, pos)))
    elif elem[0] == 'minus':
        pos += 1
        print('minus received.'+str((True, pos)))
    else:
        print('select: plz enter plus or minus.')
        return (False, pos)
    if pos >= len(token_list):
        return (False, pos)
    elem = token_list[pos]
    # follow
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = term(token_list, pos)
        return result
    else:
        print('follow: plz enter ident or number or lparen.')
        return (False, pos)


def factor(token_list, pos):
    '''
    识别为因子
    '''
    elem = token_list[pos]
    # select集+接收
    # F::=ident|number
    if elem[0] == 'ident' or elem[0] == 'number':
        # 接收ident/number
        # token_list=token_list[1::]
        pos += 1
        print('factor received.'+str((True, pos)))
    # F::=(E)
    elif elem[0] == 'lparen':
        # 接收lparen
        # token_list=token_list[1::]
        pos += 1
        if pos >= len(token_list):
            print('receiving: plz enter ident or number or lparen.')
            return (False, pos)
        else:
            result = expression(token_list, pos)
            if result[0]:
                pos = result[1]
                elem = token_list[pos]
                # 接收)
                if elem[0] == 'rparen':
                    # token_list=token_list[1::]
                    pos += 1
                    print('factor received.'+str((True, pos)))
            else:
                return result
    else:
        print('receiving: plz enter ident or number or lparen.')
        return (False, 0)
    # follow
    if pos >= len(token_list):
        # 接收结束,返回上一层
        return (True, pos)
    else:
        # 接收尚未结束
        elem = token_list[pos]
        if elem[0] == 'plus' or elem[0] == 'minus':
            # T的follow集,返回上一层决定
            return (True, pos)
        elif elem[0] == 'times' or elem[0] == 'slash':
            # F的follow集
            result = ts(token_list, pos)
            return result
        elif elem[0] == 'rparen':
            # E的follow集,返回上一层决定
            return (True, pos)
        else:
            print('follow: plz enter plus or minus or times or slash or none.')
            return (False, pos)


def term(token_list, pos):
    '''
    识别为项
    '''
    elem = token_list[pos]
    # select集正确
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = factor(token_list, pos)
        # print(result)
        # follow
        if result[0]:
            # 接收成功
            pos = result[1]
            print('term received.'+str(result))
            if pos >= len(token_list):
                # 接收结束,返回上层
                return result
            else:
                # 接收尚未成功
                elem = token_list[pos]
                if elem[0] == 'plus' or elem[0] == 'minus':
                    # T的follow集
                    result = pm(token_list, pos)
                    return result
                elif elem[0] == 'rparen':
                    # E的follow集,返回上层决定
                    return result
                else:
                    print('follow: plz enter plus or minus or rparen or none.')
                    return (False, pos)
        else:
            return result
    # select集错误
    else:
        print('select: plz enter ident or number or lparen.')
        return (False, pos)


def expression(token_list, pos):
    '''
    识别为表达式
    '''
    elem = token_list[pos]
    # select集正确
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = term(token_list, pos)
        # follow集
        if result[0]:
            pos = result[1]
            print('expression received.'+str(result))
            if pos >= len(token_list):
                # 接收结束,返回上层
                return result
            else:
                # E的follow集
                elem = token_list[pos]
                if elem[0] == 'rparen':
                    return result
                elif elem[0]=='lss' or elem[0]=='gtr' or elem[0]=='eql':
                    return result
                else:
                    print('follow: plz enter rparen or none.')
                    return (False, pos)
        else:
            return result
    # select集错误
    else:
        print('select: plz enter ident or number or lparen.')
        return (False, pos)


'''
def recog_expression(token_list,pos):
    elem = token_list[pos]
    # 处理select集
    # 接收
    if elem[0] == 'plus' or elem[0] == 'minus':
        # token_list=token_list[1::]
        pos += 1
        print('pm received.'+str((True, pos)))
    elem = token_list[pos]
    # 处理select集
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = expression(token_list, pos)
        # follow集
        if result[0]:
            print('received.'+str(result))
            pos = result[1]
            if pos >= len(token_list):
                return result
            # elif elem[result[1]]==')':
            #     return (True,result[1])
            else:
                print('follow: plz enter none.')
                return (False, pos)
        else:
            return result
    # select集错误
    else:
        print('select: plz enter plus or minus or ident or number or lparen.')
        return (False, pos)
'''


def statement(token_list,pos):
    '''
    识别为语句
    '''
    elem=token_list[pos]
    #接收ident
    if elem[0]=='ident':
        pos+=1
        print('ident received.'+str((True,pos)))
    else:
        print('select: plz enter ident.')
        return (False,pos)
    elem=token_list[pos]
    #接收eql
    if elem[0]=='eql':
        pos+=1
        print('eql received.'+str((True,pos)))
    else:
        print('receiving: plz enter eql.')
        return (False,pos)
    elem=token_list[pos]
    #接收表达式
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result=expression(token_list,pos)
        if result[0]:
            pos=result[1]
            if pos>=len(token_list):
                print('statement received.'+str(result))
                return result
            else:
                print('follow: plz enter none.')
                return (False,pos)
        else:
            return result
    else:
        print('receiving: plz enter ident or number or lparen.')
        return result


def relational(token_list,pos):
    '''
    识别为关系运算符
    '''
    elem=token_list[pos]
    if elem[0]=='eql':
        pos+=1
        print('eql received.'+str((True,pos)))
    elif elem[0]=='lss':
        pos+=1
        print('lss received.'+str((True,pos)))
    elif elem[0]=='gtr':
        pos+=1
        print('gtr received.'+str((True,pos)))
    else:
        return (False,pos)
    elem=token_list[pos]
    #follow集
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        print('relational recieved.'+str((True,pos)))
        return (True,pos)
    else:
        print('follow: plz enter indent or number or lparen.')
        return (False,pos)


def condition(token_list,pos):
    '''
    识别为条件
    '''
    elem=token_list[pos]
    #select集正确,接收表达式
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result=expression(token_list,pos)
        if result[0]:
            pos=result[1]
            elem=token_list[pos]
            #继续接收：关系运算符
            if  elem[0]=='eql' or elem[0]=='lss' or elem[0]=='gtr':
                result=relational(token_list,pos)
                if result[0]:
                    pos=result[1]
                    elem=token_list[pos]
                    #继续接收：表达式
                    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
                        result=expression(token_list,pos)
                        if result[0]:
                        #成功接收
                            pos=result[1]
                            if pos>=len(token_list):
                            #follow集错误
                                print('follow: should not end.')
                                return (False,pos)
                            else:
                                elem=token_list[pos]
                                #follow集正确
                                if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
                                    print('condition received.'+str(result))
                                    return result
                                else:
                                    print('follow: plz enter ident or number or lparen.')
                                    return (False,pos)
                        else:
                            return result
                    else:
                        print('recieving: plz enter ident or number or lparen.')
                        return (False,pos)
                else:
                    return result
            else:
                print('receiving: plz enter eql or lss or gtr.')
                return (False,pos)
        else:
            return result
    else:
        print('select: plz enter ident or number or lparen.')
        return (False,pos)


def recog_if(token_list,pos):
    '''
    识别为条件语句
    '''
    elem = token_list[pos]
    # select集正确,接收if
    if elem[0] == 'ifsym':
        pos+=1
        print('if received.'+str((True,pos)))
    else:
        print('select: plz enter if.')
        return (False, pos)
    elem=token_list[pos]
    #继续接收：条件
    if elem[0] == 'ident' or elem[0] == 'number' or elem[0] == 'lparen':
        result = condition(token_list, pos)
        if result[0]:
            pos=result[1]
            elem=token_list[pos]
            #继续接收：then
            if elem[0]=='thensym':
                pos+=1
                print('then received.'+str((True,pos)))
            else:
                print('receiving: plz enter then.')
                return (False,pos)
            elem=token_list[pos]
            #继续接收：语句
            if elem[0]=='ident':
                result=statement(token_list,pos)
                if result[0]:
                    pos=result[1]
                    print('condition statement received.'+str(result))
                    #follow集
                    if pos>=len(token_list):
                    #接收结束,返回上层
                        return result
                    else:
                    #follow集错误
                        print('follow: plz enter none.')
                        return (False,pos)
                else:
                    return result
            else:
                print('receiving: plz enter ident.')
                return (False,pos)
        else:
            return result
    else:
        print('select: plz enter ident or number or lparen.')
        return (False,pos)


def main():
    filenames = ('1.txt', '2.txt', '3.txt', '4.txt', '5.txt',
                 '6.txt', '7.txt', '8.txt', '9.txt', '10.txt')
    lines = []
    words_list = []
    token_list = []
    #idents_dict = {}
    result = (False, 0)

    for index in range(len(filenames)):
        with open('test/3/'+filenames[index], 'r', encoding='utf-8') as fr:

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

            result = recog_if(token_list,0)
            if result[0]:
                print('语法正确.')
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


if __name__ == "__main__":
    main()
