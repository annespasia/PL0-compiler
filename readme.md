## PL/0编译器

#### 实验一 识别标识符

1. 实验内容

   输入 PL/0 语言源程序，输出源程序中所有标识符的出现次数。 

2. 设计思路

- 用python写代码

- 主函数：用列表批量处理输入文件，测试不同例子只需要更改filenames列表。

- 主函数：将每行读取为字符串，用列表存放（之后需要做语法分析时更改）

- 识别函数：用正则表达式匹配标识符，并排除basic元组中的保留字

- 记数函数：用字典记录每个标识符的出现次数

- 最后，在主函数中批量将字典写入每个输出文件



#### 实验二 词法分析

1. 实验内容

   输入PL/0语言程序，输出程序中各个单词符号（关键字、专用符号以及其它标记）。

2. 设计思路

- 单词表：在words字典里分类型存放单词和编码

- 批量处理：分别逐行读取代码文件为字符串，清理缩进、换行符，放进列表

- 匹配思路：逐个处理列表元素，生成六个正则对象，用正则对象/`pattern.match(string)`方法尝试匹配五种单词和边界情况（空格、错误字符等）。保留字、标识符和数字的模式有重复，但如果按上述顺序去匹配，并且从上一次成功的匹配结束的地方开始下一次匹配，保留字就不会被识别为标识符，标志符中的数字不会被识别为数字。

- 实现：在`if-elif-else`结构中，写在前面的条件会被先处理，可以满足识别顺序的要求。使用`pattern.match(string)`方法时，只能匹配从一开始就符合正则式的字符串，匹配完后返回一个`match`对象，这个对象的`end()`方法会返回匹配串结束后的下一个位置；这时再用`end()`的返回值对字符串切片，删除前面匹配过的部分，就可以继续匹配，而且保证不重复了。这个匹配循环会不断执行，每一轮一定会找到一个匹配串（它的匹配串和类型会放进一个处理列表），直到字符串被删成空串，再看下一个元素。

- 输出二元组：对保留字、运算符和界符，`words`字典里存放了一一对应的单词和编码，可以从字典中读取并输出；对于标识符和数字，可以直接从处理列表里读取并输出。



#### 实验三 语法分析

1. 实验内容

   已给 PL/0 语言文法，构造表达式部分的语法分析器。分析对象〈算术表达式〉的 `BNF `定义如下：

   ```
   <表达式> ::= [+|-]<项>{<加法运算符> <项>}
   <项> ::= <因子>{<乘法运算符> <因子>}
   <因子> ::= <标识符>|<无符号整数>| ‘(’<表达式>‘)’
   <加法运算符> ::= +|-
   <乘法运算符> ::= *|/
   ```

2. 设计思路

   **数据结构：**

   函数参数：

   - `token_list`——输入符号串

   - `pos`——当前符号位置

   函数返回值：

   - `True/False`——语法是否正确

   - `pos`——当前符号位置

   **分析方式：**

   ① 递归下降分析，每个产生式都有一个分析函数，在各个分析函数中识别产生式右部的符号：

   - 先看当前符号是否符合当前分析函数代表的非终结符的select集，然后根据产生式右部应该遇到的符号进行分析
   - 得到返回值或得到修改过的元素后，查看新的当前符号是否符合follow集，如果符合就返回元素（接收结束了，或者符合是上层分析函数的follow集）或者进入下一个分析函数（follow集符合应该出现的非终结符的select集），不符合就返回错误

   ② 根据产生式右部应该遇到非终结符：进入非终结符的分析函数

   ③ 根据产生式右部应该遇到终结符：判断是否可以接收，如果可以，符号位置后移一位，得到一个新的元素



#### 实验四 语义分析

1. 实验内容

   已给 PL/0 语言文法，在表达式的语法分析程序里，添加语义处理部分。

2. 设计思路

   **数据结构：**

   函数参数：

   - `token_list`——输入符号串

   - `pos`——当前符号位置
   -  `value`——递归分析栈

   函数返回值：

   - `True/False`——语法是否正确

   - `pos`——当前符号位置
   - `value`——递归分析栈

   递归分析栈中元素：

   - `‘N’`——当前非终结符

   - `temp`——当前属性值,在实验中就是数值

   **分析方式：**

   ① 递归下降分析，详细思路可以见实验三报告；

   ② 当前位置不后移，也就是遇到非终结符的时候，分析栈栈顶出栈，所在函数所指，即当前产生式左部的非终结符和属性值一起入栈；

   ③ 当前位置后移，遇到终结符的时候，暂存属性值*（说明：由于**factor**函数处理标识符和无符号整数的方式与左括号不一样，在显示的时候也有区别，但将暂存的值放进递归分析栈却是一样的，所以把入栈写在显示后面了，显示递归分析栈的时候值还没进去，递归分析栈总是看起来很空，实际上值之后就进去了）*；当遇到运算符号的时候，递归分析栈顶端出栈并暂存属性值，右边运算完了再出栈后加上，最后入栈。



#### 实验五 中间代码生成

1. 实验内容

   已给 PL/0 语言文法，在实验三的表达式语法分析程序里，添加语义处理部分输出表达式的中间代码，用四元式序列表示。

2. 设计思路

   **数据结构：**

   函数参数：

   - `token_list`——输入符号串

   - `pos`——当前符号位置
   - `addr`——递归分析栈

   函数返回值：

   - `True/False`——语法是否正确

   - `pos`——当前符号位置
   - `addr`——递归分析栈

   递归分析栈中元素：

   - `‘N’`——当前非终结符

   - `temp`——当前属性值,在实验中就是数值

   **分析方式：**

   ① 递归下降分析，详细思路可以见实验三报告；

   ② 当前位置不后移，也就是遇到非终结符的时候，分析栈栈顶出栈，所在函数所指，即当前产生式左部的非终结符和属性值一起入栈；

   ③ 当前位置后移，遇到终结符的时候，暂存属性值；当遇到运算符号的时候，递归分析栈顶端出栈并暂存属性值，右边运算完了再出栈后放入中间代码生成函数，将生成函数的返回值入栈；

   ④ 中间代码生成函数收到当前运算符、参与运算的属性值后，生成新的地址，将四元组输出到对应例子编号的文本文件中，返回生成的地址。