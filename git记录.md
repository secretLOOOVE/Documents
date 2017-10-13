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


### 检出仓库

	执行如下命令以创建一个本地仓库的克隆版本：
	git clone /path/to/repository 
	如果是远端服务器上的仓库，你的命令会是这个样子：
	git clone username@host:/path/to/repository

### 工作流

	你的本地仓库由 git 维护的三棵"树"组成。第一个是你的 工作目录，它持有实际文件；第二个是 暂存区（Index），它像个缓存区域，临时保存你的改动；最后是 HEAD，它指向你最后一次提交的结果。
	你可以提出更改（把它们添加到暂存区），使用如下命令：
	git add <filename>
	git add *
	这是 git 基本工作流程的第一步；使用如下命令以实际提交改动：
	git commit -m "代码提交信息"
	现在，你的改动已经提交到了 HEAD，但是还没到你的远端仓库。
	trees
	推送改动
	你的改动现在已经在本地仓库的 HEAD 中了。执行如下命令以将这些改动提交到远端仓库：
	git push origin master
	可以把 master 换成你想要推送的任何分支。 

	如果你还没有克隆现有仓库，并欲将你的仓库连接到某个远程服务器，你可以使用如下命令添加：
	git remote add origin <server>
	如此你就能够将你的改动推送到所添加的服务器上去了。

### 分支

	分支是用来将特性开发绝缘开来的。在你创建仓库的时候，master 是"默认的"分支。在其他分支上进行开发，完成后再将它们合并到主分支上。
	branches
	创建一个叫做"feature_x"的分支，并切换过去：
	git checkout -b feature_x
	切换回主分支：
	git checkout master
	再把新建的分支删掉：
	git branch -d feature_x
	除非你将分支推送到远端仓库，不然该分支就是 不为他人所见的：
	git push origin <branch>

### 更新与合并

	要更新你的本地仓库至最新改动，执行：
	git pull
	以在你的工作目录中 获取（fetch） 并 合并（merge） 远端的改动。
	要合并其他分支到你的当前分支（例如 master），执行：
	git merge <branch>
	在这两种情况下，git 都会尝试去自动合并改动。遗憾的是，这可能并非每次都成功，并可能出现冲突（conflicts）。 这时候就需要你修改这些文件来手动合并这些冲突（conflicts）。改完之后，你需要执行如下命令以将它们标记为合并成功：
	git add <filename>
	在合并改动之前，你可以使用如下命令预览差异：
	git diff <source_branch> <target_branch>

### 标签

	为软件发布创建标签是推荐的。这个概念早已存在，在 SVN 中也有。你可以执行如下命令创建一个叫做 1.0.0 的标签：
	git tag 1.0.0 1b2e1d63ff
	1b2e1d63ff 是你想要标记的提交 ID 的前 10 位字符。可以使用下列命令获取提交 ID：
	git log
	你也可以使用少一点的提交 ID 前几位，只要它的指向具有唯一性。
	替换本地改动
	假如你操作失误（当然，这最好永远不要发生），你可以使用如下命令替换掉本地改动：
	git checkout -- <filename>
	此命令会使用 HEAD 中的最新内容替换掉你的工作目录中的文件。已添加到暂存区的改动以及新文件都不会受到影响。
	假如你想丢弃你在本地的所有改动与提交，可以到服务器上获取最新的版本历史，并将你本地主分支指向它：
	git fetch origin
	git reset --hard origin/master

### 实用小贴士

	内建的图形化 git：
	gitk
	彩色的 git 输出：
	git config color.ui true
	显示历史记录时，每个提交的信息只显示一行：
	git config format.pretty oneline
	交互式添加文件到暂存区：
	git add -i
### git diff命令详解
	diff里面a表示前面那个变量，b表示第二个变量

	HEAD     commit版本
	Index     staged版本

	a、查看尚未暂存的文件更新了哪些部分，不加参数直接输入
		git diff
	此命令比较的是工作目录(Working tree)和暂存区域快照(index)之间的差异
	也就是修改之后还没有暂存起来的变化内容。

	b、查看已经暂存起来的文件(staged)和上次提交时的快照之间(HEAD)的差异
		git diff --cached
		git diff --staged
	显示的是下一次commit时会提交到HEAD的内容(不带-a情况下)


	c、显示工作版本(Working tree)和HEAD的差别
		git diff HEAD


	d、直接将两个分支上最新的提交做diff
		git diff topic master 或 git diff topic..master

	e、输出自topic和master分别开发以来，master分支上的changed。
		git diff topic...master
	Changes that occurred on the master branch since when the topic
	 branch was started off it
	f、查看简单的diff结果，可以加上--stat参数
		git diff --stat

	g、查看当前目录和另外一个分支的差别
		git diff test
	显示当前目录和另一个叫'test'分支的差别
		git diff HEAD -- ./lib
	显示当前目录下的lib目录和上次提交之间的差别（更准确的说是在当前分支下）

	h、比较上次提交commit和上上次提交
		git diff HEAD^ HEAD

	i、比较两个历史版本之间的差异
		git diff SHA1 SHA2

### git常用命令

	Local：
	git clone git@github.com:xiahouzuoxin/mp3-encode.git        # 在本地克隆一个github上仓库
	git status                    # 获得当前项目的一个状况
	git commit -a              # 将修改文件（不包括新创建的文件）添加到索引，并提交到仓库
	git add [file]                # 添加文件到本地索引
	git branch                  # 获得当前仓库中所有分支列表
	git branch zx-branch                # 新建本地一个名为zx-branch的分支，主分支名为master
	git branch -D branch_name     # 删除名称为branch-name的本地分支
	git checkout master                  # 切回主分支，切换到zx-branch只需要将master改成zx-branch
	git log                                        # 查看提交日志，有许多附加参数
		git log -p                               # 显示补丁
		git log --stat                          # 日志统计：那些文件修改了，修改了多少行内容
		git log --graph                       # 使日志看上去更漂亮
	git diff master..zx-branch           # 比较两个分支之间差异
	git remote rm origin                   #  删除origin变量地址

	git branch [name]                 # 创建本地分支，注意新分支创建后不会自动切换为当前分支
	git checkout [name]              # 切换到name分支
	git checkout -b [name]          # 创建name分支并切换到name分支

	git merge [name]                  # 将name分支与当前分支合并，name可以是远程分支，如origin/master

	Remote:
	git push origin [name]          # 创建远程name分支
	git push origin:zx-branch      # 删除远程origin仓库地址的zx-branch分支 
	git branch -r                         # 获得当前仓库中所有分支列表，即查看远程分支


