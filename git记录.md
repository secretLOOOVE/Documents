### git介绍以及一些常用命令，加上vim编辑器的简单使用

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

	git fetch origin  
	git diff master origin/master	# 比较本地和远程 

### Git 命令速查

	git branch 查看本地所有分支
	git status 查看当前状态 
	git commit 提交 
	git branch -a 查看所有的分支
	git branch -r 查看远程所有分支
	git commit -am "init" 提交并且加注释 
	git remote add origin git@192.168.1.119:ndshow
	git push origin master 将文件给推到服务器上 
	git remote show origin 显示远程库origin里的资源 
	git push origin master:develop
	git push origin master:hb-dev 将本地库与服务器上的库进行关联 
	git checkout --track origin/dev 切换到远程dev分支
	git branch -D master develop 删除本地库develop
	git checkout -b dev 建立一个新的本地分支dev
	git merge origin/dev 将分支dev与当前分支进行合并
	git checkout dev 切换到本地dev分支
	git remote show 查看远程库
	git add .
	git rm 文件名(包括路径) 从git中删除指定文件
	git clone git://github.com/schacon/grit.git 从服务器上将代码给拉下来
	git config --list 看所有用户
	git ls-files 看已经被提交的
	git rm [file name] 删除一个文件
	git commit -a 提交当前repos的所有的改变
	git add [file name] 添加一个文件到git index
	git commit -v 当你用－v参数的时候可以看commit的差异
	git commit -m "This is the message describing the commit" 添加commit信息
	git commit -a -a是代表add，把所有的change加到git index里然后再commit
	git commit -a -v 一般提交命令
	git log 看你commit的日志
	git diff 查看尚未暂存的更新
	git rm a.a 移除文件(从暂存区和工作区中删除)
	git rm --cached a.a 移除文件(只从暂存区中删除)
	git commit -m "remove" 移除文件(从Git中删除)
	git rm -f a.a 强行移除修改后文件(从暂存区和工作区中删除)
	git diff --cached 或 $ git diff --staged 查看尚未提交的更新
	git stash push 将文件给push到一个临时空间中
	git stash pop 将文件从临时空间pop下来
	---------------------------------------------------------
	git remote add origin git@github.com:username/Hello-World.git
	git push origin master 将本地项目给提交到服务器中
	-----------------------------------------------------------
	git pull 本地与服务器端同步
	-----------------------------------------------------------------
	git push (远程仓库名) (分支名) 将本地分支推送到服务器上去。
	git push origin serverfix:awesomebranch
	------------------------------------------------------------------
	git fetch 相当于是从远程获取最新版本到本地，不会自动merge
	git commit -a -m "log_message" (-a是提交所有改动，-m是加入log信息) 本地修改同步至服务器端 ：
	git branch branch_0.1 master 从主分支master创建branch_0.1分支
	git branch -m branch_0.1 branch_1.0 将branch_0.1重命名为branch_1.0
	git checkout branch_1.0/master 切换到branch_1.0/master分支
	du -hs
	git branch 删除远程branch
	git push origin :branch_remote_name
	git branch -r -d branch_remote_name
	-----------------------------------------------------------
	初始化版本库，并提交到远程服务器端
	mkdir WebApp
	cd WebApp
	git init 本地初始化
	touch README
	git add README 添加文件
	git commit -m 'first commit'
	git remote add origin git@github.com:daixu/WebApp.git
	增加一个远程服务器端
	上面的命令会增加URL地址为'git@github.com:daixu/WebApp.git'，名称为origin的远程服务器库，以后提交代码的时候只需要使用 origin别名即可
	二、 Git 命令速查表
	1、常用的Git命令
	命令
	简要说明
	git add
	添加至暂存区
	git add–interactive
	交互式添加
	git apply
	应用补丁
	git am
	应用邮件格式补丁
	git annotate
	同义词，等同于 git blame
	git archive
	文件归档打包
	git bisect
	二分查找
	git blame
	文件逐行追溯
	git branch
	分支管理
	git cat-file
	版本库对象研究工具
	git checkout
	检出到工作区、切换或创建分支
	git cherry-pick
	提交拣选
	git citool
	图形化提交，相当于 git gui 命令
	git clean
	清除工作区未跟踪文件
	git clone
	克隆版本库
	git commit
	提交
	git config
	查询和修改配置
	git describe
	通过里程碑直观地显示提交ID
	git diff
	差异比较
	git difftool
	调用图形化差异比较工具
	git fetch
	获取远程版本库的提交
	git format-patch
	创建邮件格式的补丁文件。参见 git am 命令
	git grep
	文件内容搜索定位工具
	git gui
	基于Tcl/Tk的图形化工具，侧重提交等操作
	git help
	帮助
	git init
	版本库初始化
	git init-db*
	同义词，等同于 git init
	git log
	显示提交日志
	git merge
	分支合并
	git mergetool
	图形化冲突解决
	git mv
	重命名
	git pull
	拉回远程版本库的提交
	git push
	推送至远程版本库
	git rebase
	分支变基
	git rebase–interactive
	交互式分支变基
	git reflog
	分支等引用变更记录管理
	git remote
	远程版本库管理
	git repo-config*
	同义词，等同于 git config
	git reset
	重置改变分支“游标”指向
	git rev-parse
	将各种引用表示法转换为哈希值等
	git revert
	反转提交
	git rm
	删除文件
	git show
	显示各种类型的对象
	git stage*
	同义词，等同于 git add
	git stash
	保存和恢复进度
	git status
	显示工作区文件状态
	git tag
	里程碑管理

	2、对象库操作相关命令
	命令
	简要说明
	git commit-tree
	从树对象创建提交
	git hash-object
	从标准输入或文件计算哈希值或创建对象
	git ls-files
	显示工作区和暂存区文件
	git ls-tree
	显示树对象包含的文件
	git mktag
	读取标准输入创建一个里程碑对象
	git mktree
	读取标准输入创建一个树对象
	git read-tree
	读取树对象到暂存区
	git update-index
	工作区内容注册到暂存区及暂存区管理
	git unpack-file
	创建临时文件包含指定 blob 的内容
	git write-tree
	从暂存区创建一个树对象

	3、引用操作相关命令
	命令
	简要说明
	git check-ref-format
	检查引用名称是否符合规范
	git for-each-ref
	引用迭代器，用于shell编程
	git ls-remote
	显示远程版本库的引用
	git name-rev
	将提交ID显示为友好名称
	git peek-remote*
	过时命令，请使用 git ls-remote
	git rev-list
	显示版本范围
	git show-branch
	显示分支列表及拓扑关系
	git show-ref
	显示本地引用
	git symbolic-ref
	显示或者设置符号引用
	git update-ref
	更新引用的指向
	git verify-tag
	校验 GPG 签名的Tag

	4、版本库管理相关命令
	命令
	简要说明
	git count-objects
	显示松散对象的数量和磁盘占用
	git filter-branch
	版本库重构
	git fsck
	对象库完整性检查
	git fsck-objects*
	同义词，等同于 git fsck
	git gc
	版本库存储优化
	git index-pack
	从打包文件创建对应的索引文件
	git lost-found*
	过时，请使用 git fsck –lost-found 命令
	git pack-objects
	从标准输入读入对象ID，打包到文件
	git pack-redundant
	查找多余的 pack 文件
	git pack-refs
	将引用打包到 .git/packed-refs 文件中
	git prune
	从对象库删除过期对象
	git prune-packed
	将已经打包的松散对象删除
	git relink
	为本地版本库中相同的对象建立硬连接
	git repack
	将版本库未打包的松散对象打包
	git show-index
	读取包的索引文件，显示打包文件中的内容
	git unpack-objects
	从打包文件释放文件
	git verify-pack
	校验对象库打包文件

	5、数据传输相关命令
	命令
	简要说明
	git fetch-pack
	执行 git fetch 或 git pull 命令时在本地执行此命令，用于从其他版本库获取缺失的对象
	git receive-pack
	执行 git push 命令时在远程执行的命令，用于接受推送的数据
	git send-pack
	执行 git push 命令时在本地执行的命令，用于向其他版本库推送数据
	git upload-archive
	执行 git archive –remote 命令基于远程版本库创建归档时，远程版本库执行此命令传送归档
	git upload-pack
	执行 git fetch 或 git pull 命令时在远程执行此命令，将对象打包、上传

	6、邮件相关命令
	命令
	简要说明
	git imap-send
	将补丁通过 IMAP 发送
	git mailinfo
	从邮件导出提交说明和补丁
	git mailsplit
	将 mbox 或 Maildir 格式邮箱中邮件逐一提取为文件
	git request-pull
	创建包含提交间差异和执行PULL操作地址的信息
	git send-email
	发送邮件

	7、协议相关命令
	命令
	简要说明
	git daemon
	实现Git协议
	git http-backend
	实现HTTP协议的CGI程序，支持智能HTTP协议
	git instaweb
	即时启动浏览器通过 gitweb 浏览当前版本库
	git shell
	受限制的shell，提供仅执行Git命令的SSH访问
	git update-server-info
	更新哑协议需要的辅助文件
	git http-fetch
	通过HTTP协议获取版本库
	git http-push
	通过HTTP/DAV协议推送
	git remote-ext
	由Git命令调用，通过外部命令提供扩展协议支持
	git remote-fd
	由Git命令调用，使用文件描述符作为协议接口
	git remote-ftp
	由Git命令调用，提供对FTP协议的支持
	git remote-ftps
	由Git命令调用，提供对FTPS协议的支持
	git remote-http
	由Git命令调用，提供对HTTP协议的支持
	git remote-https
	由Git命令调用，提供对HTTPS协议的支持
	git remote-testgit
	协议扩展示例脚本

	8、版本库转换和交互相关命令
	命令
	简要说明
	git archimport
	导入Arch版本库到Git
	git bundle
	提交打包和解包，以便在不同版本库间传递
	git cvsexportcommit
	将Git的一个提交作为一个CVS检出
	git cvsimport
	导入CVS版本库到Git。或者使用 cvs2git
	git cvsserver
	Git的CVS协议模拟器，可供CVS命令访问Git版本库
	git fast-export
	将提交导出为 git-fast-import 格式
	git fast-import
	其他版本库迁移至Git的通用工具
	git svn
	Git 作为前端操作 Subversion

	9、合并相关的辅助命令
	命令
	简要说明
	git merge-base
	供其他脚本调用，找到两个或多个提交最近的共同祖先
	git merge-file
	针对文件的两个不同版本执行三向文件合并
	git merge-index
	对index中的冲突文件调用指定的冲突解决工具
	git merge-octopus
	合并两个以上分支。参见 git merge 的octopus合并策略
	git merge-one-file
	由 git merge-index 调用的标准辅助程序
	git merge-ours
	合并使用本地版本，抛弃他人版本。参见 git merge 的ours合并策略
	git merge-recursive
	针对两个分支的三向合并。参见 git merge 的recursive合并策略
	git merge-resolve
	针对两个分支的三向合并。参见 git merge 的resolve合并策略
	git merge-subtree
	子树合并。参见 git merge 的 subtree 合并策略
	git merge-tree
	显式三向合并结果，不改变暂存区
	git fmt-merge-msg
	供执行合并操作的脚本调用，用于创建一个合并提交说明
	git rerere
	重用所记录的冲突解决方案

	10、 杂项
	命令
	简要说明
	git bisect–helper
	由 git bisect 命令调用，确认二分查找进度
	git check-attr
	显示某个文件是否设置了某个属性
	git checkout-index
	从暂存区拷贝文件至工作区
	git cherry
	查找没有合并到上游的提交
	git diff-files
	比较暂存区和工作区，相当于 git diff –raw
	git diff-index
	比较暂存区和版本库，相当于 git diff –cached –raw
	git diff-tree
	比较两个树对象，相当于 git diff –raw A B
	git difftool–helper
	由 git difftool 命令调用，默认要使用的差异比较工具
	git get-tar-commit-id
	从 git archive 创建的 tar 包中提取提交ID
	git gui–askpass
	命令 git gui 的获取用户口令输入界面
	git notes
	提交评论管理
	git patch-id
	补丁过滤行号和空白字符后生成补丁唯一ID
	git quiltimport
	将Quilt补丁列表应用到当前分支
	git replace
	提交替换
	git shortlog
	对 git log 的汇总输出，适合于产品发布说明
	git stripspace
	删除空行，供其他脚本调用
	git submodule
	子模组管理
	git tar-tree
	过时命令，请使用 git archive
	git var
	显示 Git 环境变量
	git web–browse
	启动浏览器以查看目录或文件
	git whatchanged
	显示提交历史及每次提交的改动
	git-mergetool–lib
	包含于其他脚本中，提供合并/差异比较工具的选择和执行
	git-parse-remote
	包含于其他脚本中，提供操作远程版本库的函数
	git-sh-setup
	包含于其他脚本中，提供 shell 编程的函数库
	下面脚本之家小编特为大家分享一个图片版的
	Git 常用命令速查表。点击查看大图。

	Git命令参考手册(文本版)
	git init                                                  # 初始化本地git仓库（创建新仓库） 
	git config --global user.name "xxx"                       # 配置用户名 
	git config --global user.email "xxx@xxx.com"              # 配置邮件 
	git config --global color.ui true                         # git status等命令自动着色 
	git config --global color.status auto 
	git config --global color.diff auto 
	git config --global color.branch auto 
	git config --global color.interactive auto 
	git clone git+ssh://git@192.168.53.168/VT.git             # clone远程仓库 
	git status                                                # 查看当前版本状态（是否修改） 
	git add xyz                                               # 添加xyz文件至index 
	git add .                                                 # 增加当前子目录下所有更改过的文件至index 
	git commit -m 'xxx'                                       # 提交 
	git commit --amend -m 'xxx'                               # 合并上一次提交（用于反复修改） 
	git commit -am 'xxx'                                      # 将add和commit合为一步 
	git rm xxx                                                # 删除index中的文件 
	git rm -r *                                               # 递归删除 
	git log                                                   # 显示提交日志 
	git log -1                                                # 显示1行日志 -n为n行 
	git log -5
	git log --stat                                            # 显示提交日志及相关变动文件 
	git log -p -m 
	git show dfb02e6e4f2f7b573337763e5c0013802e392818         # 显示某个提交的详细内容 
	git show dfb02                                            # 可只用commitid的前几位 
	git show HEAD                                             # 显示HEAD提交日志 
	git show HEAD^                                            # 显示HEAD的父（上一个版本）的提交日志 ^^为上两个版本 ^5为上5个版本 
	git tag                                                   # 显示已存在的tag 
	git tag -a v2.0 -m 'xxx'                                  # 增加v2.0的tag 
	git show v2.0                                             # 显示v2.0的日志及详细内容 
	git log v2.0                                              # 显示v2.0的日志 
	git diff                                                  # 显示所有未添加至index的变更 
	git diff --cached                                         # 显示所有已添加index但还未commit的变更 
	git diff HEAD^                                            # 比较与上一个版本的差异 
	git diff HEAD -- ./lib                                    # 比较与HEAD版本lib目录的差异 
	git diff origin/master..master                            # 比较远程分支master上有本地分支master上没有的 
	git diff origin/master..master --stat                     # 只显示差异的文件，不显示具体内容 
	git remote add origin git+ssh://git@192.168.53.168/VT.git # 增加远程定义（用于push/pull/fetch） 
	git branch                                                # 显示本地分支 
	git branch --contains 50089                               # 显示包含提交50089的分支 
	git branch -a                                             # 显示所有分支 
	git branch -r                                             # 显示所有原创分支 
	git branch --merged                                       # 显示所有已合并到当前分支的分支 
	git branch --no-merged                                    # 显示所有未合并到当前分支的分支 
	git branch -m master master_copy                          # 本地分支改名 
	git checkout -b master_copy                               # 从当前分支创建新分支master_copy并检出 
	git checkout -b master master_copy                        # 上面的完整版 
	git checkout features/performance                         # 检出已存在的features/performance分支 
	git checkout --track hotfixes/BJVEP933                    # 检出远程分支hotfixes/BJVEP933并创建本地跟踪分支 
	git checkout v2.0                                         # 检出版本v2.0
	git checkout -b devel origin/develop                      # 从远程分支develop创建新本地分支devel并检出 
	git checkout -- README                                    # 检出head版本的README文件（可用于修改错误回退） 
	git merge origin/master                                   # 合并远程master分支至当前分支 
	git cherry-pick ff44785404a8e                             # 合并提交ff44785404a8e的修改 
	git push origin master                                    # 将当前分支push到远程master分支 
	git push origin :hotfixes/BJVEP933                        # 删除远程仓库的hotfixes/BJVEP933分支 
	git push --tags                                           # 把所有tag推送到远程仓库 
	git fetch                                                 # 获取所有远程分支（不更新本地分支，另需merge） 
	git fetch --prune                                         # 获取所有原创分支并清除服务器上已删掉的分支 
	git pull origin master                                    # 获取远程分支master并merge到当前分支 
	git mv README README2                                     # 重命名文件README为README2 
	git reset --hard HEAD                                     # 将当前版本重置为HEAD（通常用于merge失败回退） 
	git rebase 
	git branch -d hotfixes/BJVEP933                           # 删除分支hotfixes/BJVEP933（本分支修改已合并到其他分支） 
	git branch -D hotfixes/BJVEP933                           # 强制删除分支hotfixes/BJVEP933 
	git ls-files                                              # 列出git index包含的文件 
	git show-branch                                           # 图示当前分支历史 
	git show-branch --all                                     # 图示所有分支历史 
	git whatchanged                                           # 显示提交历史对应的文件修改 
	git revert dfb02e6e4f2f7b573337763e5c0013802e392818       # 撤销提交dfb02e6e4f2f7b573337763e5c0013802e392818 
	git ls-tree HEAD                                          # 内部命令：显示某个git对象 
	git rev-parse v2.0                                        # 内部命令：显示某个ref对于的SHA1 HASH 
	git reflog                                                # 显示所有提交，包括孤立节点 
	git show HEAD@{5} 
	git show master@{yesterday}                               # 显示master分支昨天的状态 
	git log --pretty=format:'%h %s' --graph                   # 图示提交日志 
	git show HEAD~3
	git show -s --pretty=raw 2be7fcb476 
	git stash                                                 # 暂存当前修改，将所有至为HEAD状态 
	git stash list                                            # 查看所有暂存 
	git stash show -p stash@{0}                               # 参考第一次暂存 
	git stash apply stash@{0}                                 # 应用第一次暂存 
	git grep "delete from"                                    # 文件中搜索文本“delete from” 
	git grep -e '#define' --and -e SORT_DIRENT 
	git gc 
	git fsck
	如对本文有疑问，请提交到交流社区，广大热心网友会为你解答！！ 点击进入社区
