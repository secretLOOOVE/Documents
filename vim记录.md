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
