### .vimrc
	
	- set cursorline
	- set cursorcolumn
	- hi cursorcolumn
	- set ruler
	- set number
	- set tabstop=4
	- set softtabstop=4
	- set shiftwidth=4

### vim技巧之重复

**Vim重复的类型**

vim中有五种基本的重复类型，分别是：

重复类型|重复操作符|回退操作符
---|---|---
文本改变重复|.|u
行内查找重复|;|,
全文查找重复|n|N
文本替换重复|&|u
宏重复|@[寄存器]|u

### vim区域选择

块选择(Visual Block)  
一般模式下，块选择的按键意义  
a|b  
---|---  
v | 字符选择，将光标经过的字符选择  
V | 行选择，将光标经过的行选择  
[Ctrl]+v | 矩形选择，可以用矩形的方式选择数据  
y | 将选中地方复制起来  
d | 将选中地方删除  
 
比如现在想把161行到170行的两个函数定义注释掉。
这里我们结合vim的.命令和块选择，(vim的.命令会记住上一次的操作)
当前光标处在161行，I//<ESC>后将定位到该行头部，并且插入//注释，后退出插入模式。然后按下大写V，然后按下170G，将选中161到170行，接下来要对这些选中的行执行.命令(即I//<ESC>)，使用命令：normal对整个范围同时执行.命令。
:’<,’>normal.命令可以解读为对高亮区中的每一行，对其执行普通模式下的.命令。

最后光标处在170行。

(当然也可以直接:161,170 normal   I//，normal可以执行任意的普通模式的命令，I会自动切换到插入模式，但是修改完成之后，vim会自动返回普通模式)

### vim中执行shell命令小结
	vim中执行shell命令，有以下几种形式
	1):!command
	不退出vim，并执行shell命令command，将命令输出显示在vim的命令区域，不会改变当前编辑的文件的内容
	例如
	:!ls -l
	特别的可以运行:!bash来启动一个bash shell并执行命令，不需要退出vim
	2):r !command
	将shell命令command的结果插入到当前行的下一行
	例如
	:r !date，读取系统时间并插入到当前行的下一行。
	3):起始行号,结束行号 !command
	将起始行号和结束行号指定的范围中的内容输入到shell命令command处理，并将处理结果替换起始行号和结束行号指定的范围中的内容
	例如
	:62,72 !sort，将62行到72行的内容进行排序
	可以只指定起始行，例如:62 !tr [a-z] [A-Z]，将62行的小写字母转为大写字母
	当前光标所在行，除可以指定行号外，也可以用.表示，例如:. !tr [a-z] [A-Z]，将当前行的小写转为大写
	4):起始行号,结束行号 w !command
	将起始行号和结束行号所指定的范围的内容作为命令command的输入。不会改变当前编辑的文件的内容
	例如
	:62,72 w !sort，将62行到72行的内容进行排序，但排序的结果并不会直接输出到当前编辑的文件中，而是显示在vim敲命令的区域
	特殊的可以下面这么用
	:62 w !bash，将会把第62行的内容作为bash命令来执行并显示结果，而且不会改变当前编辑的文件的内容
	同样的:. w !bash，将当前行的内容作为bash命令来执行
	例如52行内容为ls -l
	那么输入:52 w !bash就跟执行!ls -l是一样的效果，如果你用的shell是bash shell

	如果输入的是:52 !bash，那么会把第52行的内容也就是ls -l作为命令执行，同时命令的输出结果会替换第52行的内容，注意其中的区别。vim中执行shell命令小结

### vim全局替换命令

	语法为 :[addr]s/源字符串/目的字符串/[option]
	全局替换命令为：:%s/源字符串/目的字符串/g

	[addr] 表示检索范围，省略时表示当前行。
	如：“1，20” ：表示从第1行到20行；
	“%” ：表示整个文件，同“1,$”；
	“. ,$” ：从当前行到文件尾；
	s : 表示替换操作

	[option] : 表示操作类型
	如：g 表示全局替换; 
	c 表示进行确认
	p 表示替代结果逐行显示（Ctrl + L恢复屏幕）；
	省略option时仅对每行第一个匹配串进行替换；
	如果在源字符串和目的字符串中出现特殊字符，需要用”\”转义

	下面是一些例子：
	#将That or this 换成 This or that
	:%s/\(That\) or \(this\)/\u\2 or \l\1/
	—- 
	#将句尾的child换成children
	:%s/child\([ ,.;!:?]\)/children\1/g
	—-
	#将mgi/r/abox换成mgi/r/asquare
	:g/mg\([ira]\)box/s//mg//my\1square/g    <=>  :g/mg[ira]box/s/box/square/g
	—-
	#将多个空格换成一个空格
	:%s/  */ /g
	—-
	#使用空格替换句号或者冒号后面的一个或者多个空格
	:%s/\([:.]\)  */\1 /g
	—-
	#删除所有空行
	:g/^$/d
	—-
	#删除所有的空白行和空行
	:g/^[  ][  ]*$/d
	—-
	#在每行的开始插入两个空白
	:%s/^/>  /
	—-
	#在接下来的6行末尾加入.
	:.,5/$/./
	—-
	#颠倒文件的行序
	:g/.*/m0O  <=> :g/^/m0O
	—-
	#寻找不是数字的开始行,并将其移到文件尾部
	:g!/^[0-9]/m$ <=> g/^[^0-9]/m$
	—-
	#将文件的第12到17行内容复制10词放到当前文件的尾部
	:1,10g/^/12,17t$
	~~~~重复次数的作用
	—-
	#将chapter开始行下面的第二行的内容写道begin文件中
	:g/^chapter/.+2w>>begin
	—-
	:/^part2/,/^part3/g/^chapter/.+2w>>begin
	—-
	:/^part2/,/^part3/g/^chapter/.+2w>>begin|+t$

###	[转]Vi/Vim查找替换使用方法

	vi/vim 中可以使用 ：s 命令来替换字符串。该命令有很多种不同细节使用方法，可以实现复杂的功能，记录几种在此，方便以后查询。 
	　 
	　　：s/vivian/sky/ 替换当前行第一个 vivian 为 sky 
	　 
	　　：s/vivian/sky/g 替换当前行所有 vivian 为 sky 
	　 
	　　：n，$s/vivian/sky/ 替换第 n 行开始到最后一行中每一行的第一个 vivian 为 sky 
	　 
	　　：n，$s/vivian/sky/g 替换第 n 行开始到最后一行中每一行所有 vivian 为 sky 
	　 
	　　n 为数字，若 n 为 .，表示从当前行开始到最后一行 
	　 
	　　：%s/vivian/sky/（等同于 ：g/vivian/s//sky/） 替换每一行的第一个 vivian 为 sky 
	　 
	　　：%s/vivian/sky/g（等同于 ：g/vivian/s//sky/g） 替换每一行中所有 vivian 为 sky 
	　 
	　　可以使用 # 作为分隔符，此时中间出现的 / 不会作为分隔符 
	　 
	　　：s#vivian/#sky/# 替换当前行第一个 vivian/ 为 sky/ 
	　 
	　　：%s+/oradata/apras/+/user01/apras1+ （使用+ 来 替换 / ）： /oradata/apras/替换成/user01/apras1/ 
	　 
	　　1.：s/vivian/sky/ 替换当前行第一个 vivian 为 sky 
	　 
	　　：s/vivian/sky/g 替换当前行所有 vivian 为 sky 
	　 
	　　2. ：n，$s/vivian/sky/ 替换第 n 行开始到最后一行中每一行的第一个 vivian 为 sky 
	　 
	　　：n，$s/vivian/sky/g 替换第 n 行开始到最后一行中每一行所有 vivian 为 sky 
	　 
	　　（n 为数字，若 n 为 .，表示从当前行开始到最后一行） 
	　 
	　　3. ：%s/vivian/sky/（等同于 ：g/vivian/s//sky/） 替换每一行的第一个 vivian 为 sky 
	　 
	　　：%s/vivian/sky/g（等同于 ：g/vivian/s//sky/g） 替换每一行中所有 vivian 为 sky 
	　 
	　　4. 可以使用 # 作为分隔符，此时中间出现的 / 不会作为分隔符 
	　 
	　　：s#vivian/#sky/# 替换当前行第一个 vivian/ 为 sky/ 
	　 
	　　5. 删除文本中的^M 
	　 
	　　问题描述：对于换行，window下用回车换行（0A0D）来表示，linux下是回车（0A）来表示。这样，将window上的文件拷到unix上用时，总会有个^M.请写个用在unix下的过滤windows文件的换行符（0D）的shell或c程序。 
	　 
	　　。 使用命令：cat filename1 | tr -d “^V^M” > newfile； 
	　 
	　　。 使用命令：sed -e “s/^V^M//” filename > outputfilename.需要注意的是在1、2两种方法中，^V和^M指的是Ctrl+V和Ctrl+M.你必须要手工进行输入，而不是粘贴。 
	　 
	　　。 在vi中处理：首先使用vi打开文件，然后按ESC键，接着输入命令：%s/^V^M//. 
	　 
	　　。 ：%s/^M$//g 
	　 
	　　如果上述方法无用，则正确的解决办法是： [Page]
	　 
	　　。 tr -d \"\\r\" < src >dest 
	　 
	　　。 tr -d \"\\015\" dest 
	　 
	　　。 strings A>B 
		  6. 替换确认
			 我们有很多时候会需要某个字符(串)在文章中某些位置出现时被替换，而其它位置不被替换的有选择的操作，这就需要用户来进行确认，vi的查找替换同样支持
		   例如
		  ：s/vivian/sky/g 替换当前行所有 vivian 为 sky 
		  在命令后面加上一个字母c就可以实现，即：s/vivian/sky/gc
		  顾名思意，c是confirm的缩写
	　 
	　　7. 其它 
	　 
	　　利用 ：s 命令可以实现字符串的替换。具体的用法包括： 
	　 
	　　：s/str1/str2/ 用字符串 str2 替换行中首次出现的字符串 str1 
	　 
	　　：s/str1/str2/g 用字符串 str2 替换行中所有出现的字符串 str1 
	　 
	　　：。，$ s/str1/str2/g 用字符串 str2 替换正文当前行到末尾所有出现的字符串 str1 
	　 
	　　：1，$ s/str1/str2/g 用字符串 str2 替换正文中所有出现的字符串 str1 
	　 
	　　：g/str1/s//str2/g 功能同上 
	　 
	　　从上述替换命令可以看到：g 放在命令末尾，表示对搜索字符串的每次出现进行替换；不加 g，表示只对搜索 
	　 
	　　字符串的首次出现进行替换；g 放在命令开头，表示对正文中所有包含搜索字符串的行进行替换操作

### vim正则表达式（转）

	Vim中的正则表达式功能很强大，如果能自由运用，则可以完成很多难以想象的操作。

	如果你比较熟悉Perl的正规表达式，可以直接参照与Perl正则表达式的区别一节。

	一、使用正则表达式的命令
	使用正则表达式的命令最常见的就是 / （搜索）命令。其格式如下：

	/正则表达式
	另一个很有用的命令就是 :s（替换）命令，将第一个//之间的正则表达式替换成第二个//之间的字符串。

	:s/正则表达式/替换字符串/选项
	在学习正则表达式时可以利用 / 命令来练习。

	二、元字符
	元字符是具有特殊意义的字符。使用元字符可以表达任意字符、行首、行 尾、某几个字符等意义。

	元字符一览

	元字符	说明
	.	匹配任意一个字符
	[abc]	匹配方括号中的任意一个字符。可以使用-表示字符范围，
	如[a-z0-9]匹 配小写字母和阿拉伯数字。
	[^abc]	在方括号内开头使用^符号，表示匹配除方括号中字符之外的任意字符。
	\d	匹配阿拉伯数字，等同于[0-9]。
	\D	匹配阿拉伯数字之外的任意字符，等同于[^0-9]。
	\x	匹配十六进制数字，等同于[0-9A-Fa-f]。
	\X	匹配十六进制数字之外的任意字符，等同于[^0-9A-Fa-f]。
	\w	匹配单词字母，等同于[0-9A-Za-z_]。
	\W	匹配单词字母之外的任意字符，等同于[^0-9A-Za-z_]。
	\t	匹配<TAB>字符。
	\s	匹配空白字符，等同于[ \t]。
	\S	匹配非空白字符，等同于[^ \t]。
	另外，如果要查找字符 *、.、/等，则需要在前面用 \ 符号，表示这不是元字符，而只是普通字符而已。

	元字符	说明
	\*	匹配 * 字符。
	\.	匹配 . 字符。
	\/	匹配 / 字符。
	\\	匹配 \ 字符。
	\[	匹配 [ 字符。
	表示数量的元字符

	元字符	说明
	*	匹配0-任意个
	\+	匹配1-任意个
	\?	匹配0-1个
	\{n,m}	匹配n-m个
	\{n}	匹配n个
	\{n,}	匹配n-任意个
	\{,m}	匹配0-m个
	表示位置的符号

	元字符	说明
	$	匹配行尾
	^	匹配行首
	\<	匹配单词词首
	\>	匹配单词词尾
	使用例

	/char\s\+[A-Za-z_]\w*;                 " 查找所有以char开头，之后是一个以上的空白，
												 " 最后是一个标识符和分号
	/\d\d:\d\d:\d\d                        " 查找如 17:37:01 格式的时间字符串
	:g/^\s*$/d                             " 删除只有空白的行
	:s/\<four\>/4/g                        " 将所有的four替换成4，但是fourteen中的four不替换
	三、替换变量
	在正规表达式中使用 \( 和 \) 符号括起正规表达式，即可在后面使用\1、\2 等变量来访问 \( 和 \) 中的内容。

	使用例

	/\(a\+\)[^a]\+\1                                          " 查找开头和结尾处a的个数相同的字符串，
																	  " 如 aabbbaa，aaacccaaa，但是不匹配 abbbaa
	:s/\(http:\/\/[-a-z\._~\+%\/]\+\)/<a href="\1">\1<\/a>/   " 将URL替换为<a href="http://url">http://url</a>的格式
	:s/\(\w\+\)\s\+\(\w\+\)/\2\t\1                            " 将 data1 data2 修改为 data2 data1
	四、函数式
	在替换命令 s/// 中可以使用函数表达式来书写替换内容，格式为

	:s/替换字符串/\=函数式
	在函数式中可以使用 submatch(1)、submatch(2) 等来引用 \1、\2 等的内容，而submatch(0)可以引用匹配的整个内容。

	使用例

	:%s/\<id\>/\=line(".")                              " 将各行的 id 字符串替换为行号
	:%s/^\<\w\+\>/\=(line(".")-10) .".". submatch(1)    " 将每行开头的单词替换为 (行号-10).单词 的格式，
															   " 如第11行的 word 替换成 1. word
	五、与Perl正则表达式的区别
	元字符的区别

	Vim语法	Perl语法	含义
	\+	+	1-任意个
	\?	?	0-1个
	\{n,m}	{n,m}	n-m个
	\(和\)	(和)	分组



	六、vi 正则表达式练习
	 

	闲言碎语不要讲…例子说明一切，比如下面这段我需要换成 ubb 标签

	 

	 

	vim 命令模式，输入

	:%s/.*src=”([^"]*)”[^>]*>/[img]1[/img]/g

	替换为

	[img ]gu.jpg[ /img]

	[img ]os.jpg[ /img]

	[img ]hu.jpg[ /img]

	[img ]ang.jpg[ /img]

	解释如下：

	:

	命令执行状态

	%s

	表示查找并替换

	%s/a/b/g

	a 被查找的字符串（正则匹配）；b 要替换成的文字；g 表示全局搜索替换（否则只处理找到的第一个结果）

	([^"]*)

	表示非引号的字符N个；外面 () 表示后面替换要用（用 1,…,9等引用）

	[/img]

	/ 需要被 转义

	与其它工具正则不一样的地方在于 () 也必须 ()，怪不得我老是弄不出来。

	相关资料：

	via http://net.pku.edu.cn/~yhf/tao_regexps_zh.html

	vi 命令 作用

	:%s/ */ /g 把一个或者多个空格替换为一个空格。

	:%s/ *$// 去掉行尾的所有空格。

	:%s/^/ / 在每一行头上加入一个空格。

	:%s/^[0-9][0-9]* // 去掉行首的所有数字字符。

	:%s/b[aeio]g/bug/g 将所有的bag、beg、big和bog改为bug。

	:%s/t([aou])g/h1t/g 将所有tag、tog和tug分别改为hat、hot和hug（注意用group的用法和使用1引用前面被匹配的字符）。

	Sed

	Sed是Stream EDitor的缩写，是Unix下常用的基于文件和管道的编辑工具，可以在手册中得到关于sed的详细信息。

	这里是一些有趣的sed脚本，假定我们正在处理一个叫做price.txt的文件。注意这些编辑并不会改变源文件，sed只是处理源文件的每一行并 把结果显示在标准输出中（当然很容易使用重定向来定制）：

	sed脚本 描述

	sed ’s/^$/d’ price.txt 删除所有空行

	sed ’s/^[ ]*$/d’ price.txt 删除所有只包含空格或者制表符的行

	sed ’s/”//g’ price.txt 删除所有引号


### vi / vim 删除以及其它命令

	删除一行：dd
	 
	删除一个单词/光标之后的单词剩余部分：dw
	 
	删除当前字符：x
	 
	光标之后的该行部分：d$
	 
	 
	文本删除
	dd 删除一行
	d$ 删除以当前字符开始的一行字符
	 
	ndd 删除以当前行开始的n行
	dw 删除以当前字符开始的一个字
	ndw 删除以当前字符开始的n个字
	 
	D 与d$同义
	 
	d) 删除到下一句的开始
	 
	d} 删除到下一段的开始
	d回车 删除2行
	ndw 或 ndW 删除光标处开始及其后的 n-1 个字符。
	d0 删至行首。
	d$ 删至行尾。
	ndd 删除当前行及其后 n-1 行。
	x 或 X 删除一个字符。
	Ctrl+u 删除输入方式下所输入的文本。
	^R 恢复u的操作
	J 把下一行合并到当前行尾
	V 选择一行
	^V 按下^V后即可进行矩形的选择了
	aw 选择单词
	iw 内部单词(无空格)
	as 选择句子
	is 选择句子(无空格)
	ap 选择段落
	ip 选择段落(无空格)
	D 删除到行尾
	x,y 删除与复制包含高亮区

	dl 删除当前字符（与x命令功能相同）
	d0 删除到某一行的开始位置
	d^ 删除到某一行的第一个字符位置（不包括空格或TAB字符）
	dw 删除到某个单词的结尾位置
	d3w 删除到第三个单词的结尾位置
	db 删除到某个单词的开始位置
	dW 删除到某个以空格作为分隔符的单词的结尾位置
	dB 删除到某个以空格作为分隔符的单词的开始位置
	d7B 删除到前面7个以空格作为分隔符的单词的开始位置
	d） 删除到某个语句的结尾位置
	d4） 删除到第四个语句的结尾位置
	d（ 删除到某个语句的开始位置
	d） 删除到某个段落的结尾位置
	d{ 删除到某个段落的开始位置
	d7{ 删除到当前段落起始位置之前的第7个段落位置
	dd 删除当前行
	d/text 删除从文本中出现“text”中所指定字样的位置，
	一直向前直到下一个该字样所出现的位置（但不包括该字样）之间的内容
	dfc 删除从文本中出现字符“c”的位置，一直向前直到下一个该字符所出现的位置（包括该字符）之间的内容
	dtc 删除当前行直到下一个字符“c”所出现位置之间的内容
	D 删除到某一行的结尾
	d$ 删除到某一行的结尾
	5dd 删除从当前行所开始的5行内容
	dL 删除直到屏幕上最后一行的内容
	dH 删除直到屏幕上第一行的内容
	dG 删除直到工作缓存区结尾的内容
	d1G 删除直到工作缓存区开始的内容
	 
	 
	在Vi 中移动光标

	  k        上
	h   l    左  右
	  j        下

	^        移动到该行第一个非空格的字符处
	w        向前移动一个单词，将符号或标点当作单词处理
	W        向前移动一个单词，不把符号或标点当作单词处理
	b        向后移动一个单词，把符号或标点当作单词处理
	B        向后移动一个单词，不把符号或标点当作单词处理
	(        光标移至句首
	)        光标移至句尾
	{        光标移至段落开头
	}        光标移至段落结尾
	H        光标移至屏幕顶行
	M        光标移至屏幕中间行
	L        光标移至屏幕最后行 
	0        到行首
	$        到行尾
	gg       到页首
	G        到页末
	行号+G   跳转到指定行
	n+       光标下移n行
	n-       光标上移n行 
	Ctrl+g   查询当前行信息和当前文件信息

	fx       向右跳到本行字符x处（x可以是任何字符）
	Fx       向左跳到本行字符x处（x可以是任何字符）

	tx       和fx相同，区别是跳到字符x前
	Tx       和Fx相同，区别是跳到字符x后

	C-b      向上滚动一屏
	C-f      向下滚动一屏
	C-u      向上滚动半屏
	C-d      向下滚动半屏
	C-y      向上滚动一行
	C-e      向下滚动一行

	nz       将第n行滚至屏幕顶部，不指定n时将当前行滚至屏幕顶部。 
	进入和退出Vi命令

	vi filename               打开或新建文件，并将光标置于第一行首
	vi +n filename            打开文件，并将光标置于第n行首
	vi + filename             打开文件，并将光标置于最后一行首
	vi +/pattern filename     打开文件，并将光标置于第一个与pattern匹配的串处
	vi -r filename            在上次正用vi编辑时发生系统崩溃，恢复filename
	vi filename ... filename  打开多个文件，依次进行编辑 

	ZZ                        退出vi并保存
	:q!                       退出vi，不保存
	:wq                       退出vi并保存
	重复操作

	.        重复上一次操作
	自动补齐

	C-n      匹配下一个关键字
	C-p      匹配上一个关键字
	插入

	o        在光标下方新开一行并将光标置于新行行首，进入插入模式。
	O        同上，在光标上方。

	a        在光标之后进入插入模式。
	A        同上，在光标之前。


	R        进入替换模式，直到按下Esc
	set xxx  设置XXX选项。
	行合并

	J        把下面一行合并到本行后面
	Vi中查找及替换命令

	/pattern         从光标开始处向文件尾搜索pattern
	?pattern         从光标开始处向文件首搜索pattern
	n                在同一方向重复上一次搜索命令
	N                在反方向上重复上一次搜索命令
	%                查找配对的括号
	:s/p1/p2/g       将当前行中所有p1均用p2替代，若要每个替换都向用户询问则应该用gc选项
	:n1,n2s/p1/p2/g  将第n1至n2行中所有p1均用p2替代
	:g/p1/s//p2/g    将文件中所有p1均用p2替换

	.*[]^%~$ 在Vi中具有特殊含义，若需要查找则应该加上转义字符"\"
	查找的一些选项
	设置高亮
	:set hlsearch    设置高亮
	:set nohlsearch  关闭高亮
	:nohlsearch      关闭当前已经设置的高亮
	增量查找
	:set incsearch   设置增量查找
	:set noincsearch 关闭增量查找
	在Vi中删除

	x        删除当前光标下的字符
	dw       删除光标之后的单词剩余部分。
	d$       删除光标之后的该行剩余部分。
	dd       删除当前行。

	c        功能和d相同，区别在于完成删除操作后进入INSERT MODE
	cc       也是删除当前行，然后进入INSERT MODE

	更改字符

	rx       将当前光标下的字符更改为x（x为任意字符） 
	~        更改当前光标下的字符的大小写 
	 
	键盘宏操作

	qcharacter  开始录制宏，character为a到z的任意字符
	q           终止录制宏
	@character  调用先前录制的宏

	恢复误操作

	u        撤销最后执行的命令
	U        修正之前对该行的操作
	Ctrl+R   Redo
	在Vi中操作Frame

	c-w c-n  增加frame
	c-w c-c  减少frame
	c-w c-w  切换frame
	c-w c-r  交换两个frame
	VIM中的块操作

	Vim支持多达26个剪贴板
	  选块   先用v，C-v，V选择一块，然后用y复制，再用p粘贴。
	  yy     复制当前整行
	  nyy    复制当前行开始的n行内容
	  ?nyy   将光标当前行及其下n行的内容保存到寄存器?中，其中?为一个字母，n为一个数字
	  ?nyw   将光标当前行及其下n个词保存到寄存器?中，其中?为一个字母，n为一个数字
	  ?nyl   将光标当前行及其下n个字符保存到寄存器?中，其中?为一个字母，n为一个数字
	  ?p     将寄存器?中的内容粘贴到光标位置之后。如果?是用yy复制的完整行，
			 则粘贴在光标所在行下面。这里?可以是一个字母，也可以是一个数字 
	  ?P     将寄存器a中的内容粘贴到光标位置之前。如果?是用yy复制的完整行，
			 则粘贴在光标所在行上面。这里?可以是一个字母，也可以是一个数字 
	  ay[motion]
				ay$    复制光标位置到行末并保存在寄存器a中
				ayft   复制光标位置到当前行第一个字母t并保存在寄存器a中
	以上指令皆可去掉a工作，则y,p对未命名寄存器工作（所有d,c,x,y的对象都被保存在这里）。
	剪切/复制/粘贴
	所有删除的内容自动被保存，可以用p键粘贴
	Vi的选项设置

	all         列出所有选项设置情况
	term        设置终端类型
	ignorance   在搜索中忽略大小写
	list        显示制表位(Ctrl+I)和行尾标志($)
	number      显示行号
	report      显示由面向行的命令修改过的数目
	terse       显示简短的警告信息
	warn        在转到别的文件时若没保存当前文件则显示NO write信息
	nomagic     允许在搜索模式中，使用前面不带“\”的特殊字符
	nowrapscan  禁止vi在搜索到达文件两端时，又从另一端开始
	mesg        允许vi显示其他用户用write写到自己终端上的信息 
	tips

	对代码自动格式化 gg=G
	 
	 
	在vi/vim中，跳到文件首尾快捷键:
	 
	文件开始:shift + g
	文件结束:g g

#### vim代码折叠功能

	:set fdm=marker
	5G
	zf10G 折叠第5行到第10行的代码
	zR 打开所有折叠
	zM 关闭所有折叠
	zE 删除所有折叠标签
	zf 创建折叠，可以按照前面方式折叠，也可以选中代码后折叠
	zF 在当前行创建折叠。当一开始就计划要折叠写代码的时候，创建然后往里添加内容
	:5,10fo，折叠5-10行代码
	zd 删除光标下的折叠
	zD 删除光标下的折叠以及嵌套的折叠
	zE 删除窗口内所有折叠

	zo 打开光标下的折叠
	zO 打开光标下的折叠以及嵌套的折叠
	zc 关闭光标下的折叠
	zC 关闭光标下的折叠，以及嵌套的折叠
	za 当光标在关闭折叠时，打开之。在打开折叠时，关闭之
	zA 和zA类似，不过对当折叠和嵌套折叠都有效
	zv 打开当前光标的折叠，仅打开足够的折叠使光标所在的行不被折叠
	zr和zm  一层一层打开和关闭折叠
	zR和zM 打开关闭所有折叠

	在折叠间移动：  
	[z 到当前折叠的开始。如果已在开始处，移到包含折叠的折叠开始处
	]z 到当前打开的折叠的结束。如果已在结束处，移到包含这个折叠的折叠结束处
	zj 把光标移到下一个折叠的开始处
	zk 把光标移到前一个折叠的开始处。

#### vimdiff比较两个文件

1. vimdiff file1 file2 终端下输入该命令进入vim，垂直分隔窗口进行比较。
2. vimdiff -o file1 file2 水平分隔窗口进行比较
3. ctrl+w(j,k,h,l) 上下左右移动光标所在窗口（按下ctrl+w，放开ctrl再按j,k,h,l）
4. ctrl+w（J,K,H,L) 上下左右移动光标所在窗口位置
5. zo和zc 打开折叠区和关闭折叠区
6. ]c和[c 将光标移动到下一个不同区和上一个不同区
7. do和dp 将光标所在不同区域同步为另一个文件该位置的内容和将光标所在不同区域内容同步到另一个文件位置
8. diffu[!] vim下更新当前比较窗口，比较状态下修改文件后，可调用该命令[中括号不为命令部分，如果加！表示如果外部修改了文件，则重新加载比较]
9. diffo[!] vim下关闭当前窗口比较状态，如果加！则关闭所有窗口比较状态 
10. diffs file1 vim下加入file1和当前光标所在窗口进行比较，水平分隔窗口
11. vert diffs file1 垂直分隔窗口
12. difft vim下将光标所在窗口变为比较窗口
13. diff -u file1 file2 >file3 终端下输入该命令，可以将file1和file2的比较结果输出到file3中，-u表示以合并格式比较，-c为上下文格式，不加为一般格式

	
