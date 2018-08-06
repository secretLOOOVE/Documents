### 使用pdb进行调试
##### 表1. pdb常用命令

完整命令|简写命令|描述
-------|:--------:|--------
args|a|打印当前函数的参数
break|b|设置断点
clear|cl|清除断点
condition|无|设置条件断点
continue|c|继续执行
disable|无|禁用断点
enable|无|启用断点
help|h|帮助
ignore|无|忽略断点
jump|j|跳转到指定行数运行
list|l|查看当前行的代码段
next|n|执行下条语句,遇到函数不进入其内部
print|p|打印变量值
quit|q|退出pdb
return|r|执行代码直到当前函数返回
tbreak|无|设置临时断点,断点只中断一次
step|s|执行下一条语句,遇到函数进入其内部
where|w|查看所在位置
!|无|在pdb中执行语句

```
import pdb
a = "aaa"
pdb.set_trace()
b = "bbb"
c = "ccc"
final = a + b + c
print final

```
##### 命令行进入pdb

```
python3.5 -m pdb *.py
```
##### pdb常用函数

* pdb.run(statement,globals=None,locals=None) statement要调试的语句块,字符串形式
* pdb.runeval(expression,globals=None,locals=None) expression 要调试的表达式
* pdb.runcall(*args,**kwds) 调试函数
* pdb.settrace() 脚本中设置硬断点

#### python中如何使输出不换行

python2.x版本中，使用“，”可使输出不换行：  
```
for i in range(0,5):
	for k in range(0,5):
		print('*'),
		k+=1
	i+=1
	print(" ")
```

python 3.x版本输出不换行格式如下：  
```
print(x,end="") end=""可使输出不换行
```
#### python str与bytes之间的转换  

```


 # bytes object
  b = b"example"
 
  # str object
  s = "example"
 
  # str to bytes
  bytes(s, encoding = "utf8")
 
  # bytes to str
  str(b, encoding = "utf-8")
 
  # an alternative method
  # str to bytes
  str.encode(s)
  # bytes to str
  bytes.decode(b)
```
