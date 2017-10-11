z## git介绍以及一些常用命令，加上vim编辑器的简单使用

**git的功能特性**

1. 从服务器上克隆完整的Git仓库（包括代码和版本信息）到单机上。
2. 在自己的机器上根据不同的开发目的，创建分支，修改代码。
3. 在单机上自己创建的分支上提交代码。
4. 在单机上合并分支。
5. 把服务器上最新版的代码fetch下来，然后跟自己的主分支合并。
6. 生成补丁（patch），把补丁发送给主开发者。
7. 看主开发者的反馈，如果主开发者发现两个一般开发者之间有冲突（他们之间可以合作解决的冲突），就会要求他们先解决冲突，然后再由其中一个人提交。如果主开发者可以自己解决，或者没有冲突，就通过。
8. 一般开发者之间解决冲突的方法，开发者之间可以使用pull 命令解决冲突，解决完冲突之后再向主开发者提交补丁。

**git的一些常用命令**
**git的一些简易命令（重点）**
1. pwd：查看当前所在目录；
2. ls（list命令）：显示当前目录下所有的文件；
3. ls -a（list-all命令）：显示当前目录下所有的文件，包括隐藏的目录；
4. cd：切换目录，后接要切换到的目录，例如从c盘切换到d盘；
5. mkdir（make directory）：创建一个目录，后接目录名，例如在桌面创建一个oxc目录；
6. touch：创建文件，例如在oxc目录下创建一个a.txt文件
7. rm（remove）：删除文件，例如删除oxc文件夹下的a.txt文件；
8. rm -r（remove recursively）：删除目录，例如删除oxc目录；
9. mv：重命名，格式：mv （空格） 原文件/目录名 （空格） 改的名，例子：修改oxc目录名为ooo；
10. cat：输出文件内容，例如输出a.txt文件的内容；
11. ！！（两个感叹号）：重复上一行命令（或者直接按↑键）
12. vim：进入vim编辑器，如果后接文件名，则进入该文件的编辑模式，看图：  
①. vim编辑器中，按i进入编辑模式；  
②. 按Esc回到锁定模式；  
③. 锁定模式下按：进入命令模式；  
④. 命令模式下输入quit不保存退出write保存不退出wq保存退出  

**vim编辑器的简单使用（本次课程作业1）**

	快速定位到当前段落开头：{；  
	快速定位到当前段落结尾：}；  
	复制一段文本，并粘贴：复制：y（yank）;粘贴：p（paster）；  
	删除几行：删除dd，删除N行：光标所处行输入Ndd，删除包括光标所处行以下的三行；  
	快速翻页：上翻页：ctrl+b，下翻页：ctrl+f，上翻半页：ctrl+u，下翻半页：ctrl+d；  
	查找某个字符串：查找第一个出现该字符串的地方：/ + 字符串，然后回车；  
查找最后一个该字符串出现的地方：? + 字符串，然后回车；  
  
**其他：** 
1. 移动光标：k：上；j：下；h：左；l：右；
2. 移动多行：nk：向上移动n行；nh：向左移动n列；j和l类似；
3. 到最开头：gg；
4. 到最后一行：shift+g；
5. 缩进和删除缩进：缩进：shift+>+> 删除缩进：shift+<+<；

### Linux下Git和GitHub环境的搭建

	第一步： 安装Git，使用命令 “sudo apt-get install git”

	第二步： 创建GitHub帐号

	第三步： 生成ssh key，使用命令 “ssh-keygen -t rsa -C "your_email@youremail.com"”，your_email是你的email

	第四步： 回到github，进入Account Settings，左边选择SSH Keys，Add SSH Key,title随便填，粘贴key。

	第五步： 测试ssh key是否成功，使用命令“ssh -T git@github.com”，如果出现You’ve successfully authenticated, but GitHub does not provide shell access 。这就表示已成功连上github。

	第六步： 配置Git的配置文件，username和email

	git config --global user.name "your name" //配置用户名

	git config --global user.email "your email" //配置email

	 
 
### 利用Git从本地上传到GitHub
 
	 第一步： 进入要所要上传文件的目录输入命令 “git init”
	 
	 第二步： 创建一个本地仓库origin，使用命令 “git remote add origin git@github.com:yourName/yourRepo.git”
	 youname是你的GitHub的用户名，yourRepo是你要上传到GitHub的仓库
	 
	 第三步： 比如你要添加一个文件xxx到本地仓库，使用命令 “git add xxx”，可以使用“git add .”自动判断添加哪些文件
	 
	 然后把这个添加提交到本地的仓库，使用命令 ”git commit -m ”说明这次的提交“ “
	 
	 最后把本地仓库origin提交到远程的GitHub仓库，使用命令 ”git push origin master“
	 
  
  
### 从GitHub克隆项目到本地
  
	  第一步： 到GitHub的某个仓库，然后复制右边的有个“HTTPS clone url”
	  
	  第二步： 回到要存放的目录下，使用命令 "git clone https://github.com/chenguolin/scrapy.git"，红色的url只是一个例子
	  
	  第三步： 如果本地的版本不是最新的，可以使用命令 “git fetch origin”，origin是本地仓库
	  
	  第四步： 把更新的内容合并到本地分支，可以使用命令 “git merge origin/master”
	  
   
   
   如果你不想手动去合并，那么你可以使用： git pull <本地仓库> master // 这个命令可以拉去最新版本并自动合并
   
    
	
### GitHub的分支管理
	
	**创建**
	
	1 创建一个本地分支： git branch <新分支名字>
	
	2 将本地分支同步到GitHub上面： git push <本地仓库名> <新分支名>
	
	3 切换到新建立的分支： git checkout <新分支名>
	
	4 为你的分支加入一个新的远程端： git remote add <远程端名字> <地址>
	
	5 查看当前仓库有几个分支: git branch
	
	**删除**
	
	1 从本地删除一个分支： git branch -d <分支名称>
	
	2 同步到GitHub上面删除这个分支： git push <本地仓库名> :<GitHub端分支>""""""""

### 修改git远程库push方式为ssh
	
	查看使用的传输协议：  
	git remote -v

	重新设置成ssh的方式：
	git remote rm origin
	git remote add origin git@github.com:username/repository.git
	git push -u origin master



