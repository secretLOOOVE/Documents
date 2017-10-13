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
