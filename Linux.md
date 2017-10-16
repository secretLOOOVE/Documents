****
#### Linux命令行连接wifi

```
iwconfig  
sudo ip link set wlan0 up
sudo iw dev wlan0 scan | less
sudo iw dev wlan0 connect [ssid] key 0:[wep密钥]
wpa wpa2情况如下：
修改/etc/wap_supplicant/wap_supplicant.conf
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
sudo dhcpcd wlan0

```
方法二：
```
sudo nano /etc/network/interfaces
修改内容如下：
auto lo
iface lo inet loopback
iface eth0 inet dhcp
auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-ssid "TP-LINK_10M"
wpa-psk "123qazQAZ"

sudo /etc/init.d/networking restart
sudo service networking restart 功能同上一句

```
****
### Linux GPIO

GPIO Sysfs Interface for Userspace
==================================

Paths in Sysfs
--------------
There are three kinds of entries in /sys/class/gpio:

   -	Control interfaces used to get userspace control over GPIOs;

   -	GPIOs themselves; and

   -	GPIO controllers ("gpio_chip" instances).

That's in addition to standard files including the "device" symlink.

The control interfaces are write-only:

    /sys/class/gpio/

    	"export" ... Userspace may ask the kernel to export control of
		a GPIO to userspace by writing its number to this file.

		Example:  "echo 19 > export" will create a "gpio19" node
		for GPIO #19, if that's not requested by kernel code.

    	"unexport" ... Reverses the effect of exporting to userspace.

		Example:  "echo 19 > unexport" will remove a "gpio19"
		node exported using the "export" file.

GPIO signals have paths like /sys/class/gpio/gpio42/ (for GPIO #42)
and have the following read/write attributes:

    /sys/class/gpio/gpioN/

	"direction" ... reads as either "in" or "out". This value may
		normally be written. Writing as "out" defaults to
		initializing the value as low. To ensure glitch free
		operation, values "low" and "high" may be written to
		configure the GPIO as an output with that initial value.

		Note that this attribute *will not exist* if the kernel
		doesn't support changing the direction of a GPIO, or
		it was exported by kernel code that didn't explicitly
		allow userspace to reconfigure this GPIO's direction.

	"value" ... reads as either 0 (low) or 1 (high). If the GPIO
		is configured as an output, this value may be written;
		any nonzero value is treated as high.

		If the pin can be configured as interrupt-generating interrupt
		and if it has been configured to generate interrupts (see the
		description of "edge"), you can poll(2) on that file and
		poll(2) will return whenever the interrupt was triggered. If
		you use poll(2), set the events POLLPRI and POLLERR. If you
		use select(2), set the file descriptor in exceptfds. After
		poll(2) returns, either lseek(2) to the beginning of the sysfs
		file and read the new value or close the file and re-open it
		to read the value.

	"edge" ... reads as either "none", "rising", "falling", or
		"both". Write these strings to select the signal edge(s)
		that will make poll(2) on the "value" file return.

		This file exists only if the pin can be configured as an
		interrupt generating input pin.

	"active_low" ... reads as either 0 (false) or 1 (true). Write
		any nonzero value to invert the value attribute both
		for reading and writing. Existing and subsequent
		poll(2) support configuration via the edge attribute
		for "rising" and "falling" edges will follow this
		setting.

GPIO controllers have paths like /sys/class/gpio/gpiochip42/ (for the
controller implementing GPIOs starting at #42) and have the following
read-only attributes:

    /sys/class/gpio/gpiochipN/

    	"base" ... same as N, the first GPIO managed by this chip

    	"label" ... provided for diagnostics (not always unique)

        "ngpio" ... how many GPIOs this manages (N to N + ngpio - 1)

Board documentation should in most cases cover what GPIOs are used for
what purposes. However, those numbers are not always stable; GPIOs on
a daughtercard might be different depending on the base board being used,
or other cards in the stack. In such cases, you may need to use the
gpiochip nodes (possibly in conjunction with schematics) to determine
the correct GPIO number to use for a given signal.


Exporting from Kernel code
--------------------------
Kernel code can explicitly manage exports of GPIOs which have already been
requested using gpio_request():

	/* export the GPIO to userspace */
	int gpiod_export(struct gpio_desc *desc, bool direction_may_change);

	/* reverse gpio_export() */
	void gpiod_unexport(struct gpio_desc *desc);

	/* create a sysfs link to an exported GPIO node */
	int gpiod_export_link(struct device *dev, const char *name,
		      struct gpio_desc *desc);

After a kernel driver requests a GPIO, it may only be made available in
the sysfs interface by gpiod_export(). The driver can control whether the
signal direction may change. This helps drivers prevent userspace code
from accidentally clobbering important system state.

This explicit exporting can help with debugging (by making some kinds
of experiments easier), or can provide an always-there interface that's
suitable for documenting as part of a board support package.

After the GPIO has been exported, gpiod_export_link() allows creating
symlinks from elsewhere in sysfs to the GPIO sysfs node. Drivers can
use this to provide the interface under their own device in sysfs with
a descriptive name.

---
### linux之find命令详解
    
    查找文件
    find ./ -type f
    
    查找目录
    find ./ -type d
    
    查找名字为test的文件或目录
    find ./ -name test
    
    查找名字符合正则表达式的文件,注意前面的‘.*’(查找到的文件带有目录)
    find ./ -regex .*so.*\.gz
    
    查找目录并列出目录下的文件(为找到的每一个目录单独执行ls命令，没有选项-print时文件列表前一行不会显示目录名称)
    find ./ -type d -print -exec ls {} \;
    
    查找目录并列出目录下的文件(为找到的每一个目录单独执行ls命令,执行命令前需要确认)
    find ./ -type d -ok ls {} \;
    
    查找目录并列出目录下的文件(将找到的目录添加到ls命令后一次执行，参数过长时会分多次执行)
    find ./ -type d -exec ls {} +
    
    查找文件名匹配*.c的文件
    find ./ -name \*.c
    
    打印test文件名后，打印test文件的内容
    find ./ -name test -print -exec cat {} \;
    
    不打印test文件名，只打印test文件的内容
    find ./ -name test -exec cat {} \;
    
    查找文件更新日时在距现在时刻二天以内的文件
    find ./ -mtime -2
    
    查找文件更新日时在距现在时刻二天以上的文件
    find ./ -mtime +2
    
    查找文件更新日时在距现在时刻一天以上二天以内的文件
    find ./ -mtime 2
    
    查找文件更新日时在距现在时刻二分以内的文件
    find ./ -mmin -2
    
    查找文件更新日时在距现在时刻二分以上的文件
    find ./ -mmin +2
    
    查找文件更新日时在距现在时刻一分以上二分以内的文件
    find ./ -mmin 2
    
    查找文件更新时间比文件abc的内容更新时间新的文件
    find ./ -newer abc
    
    查找文件访问时间比文件abc的内容更新时间新的文件
    find ./ -anewer abc
    
    查找空文件或空目录
    find ./ -empty
    
    查找空文件并删除
    find ./ -empty -type f -print -delete
    
    查找权限为644的文件或目录(需完全符合)
    find ./ -perm 664
    
    查找用户/组权限为读写，其他用户权限为读(其他权限不限)的文件或目录
    find ./ -perm -664
    
    查找用户有写权限或者组用户有写权限的文件或目录
    find ./ -perm /220
    find ./ -perm /u+w,g+w
    find ./ -perm /u=w,g=w
    
    查找所有者权限有读权限的目录或文件
    find ./ -perm -u=r
    
    查找用户组权限有读权限的目录或文件
    find ./ -perm -g=r
    
    查找其它用户权限有读权限的目录或文件
    find ./ -perm -o=r
    
    查找所有者为lzj的文件或目录
    find ./ -user lzj
    
    查找组名为gname的文件或目录
    find ./ -group gname
    
    查找文件的用户ID不存在的文件
    find ./ -nouser
    
    查找文件的组ID不存在的文件
    find ./ -nogroup
    
    查找有执行权限但没有可读权限的文件
    find ./ -executable \! -readable
    
    查找文件size小于10个字节的文件或目录
    find ./ -size -10c
    
    查找文件size等于10个字节的文件或目录
    find ./ -size 10c
    
    查找文件size大于10个字节的文件或目录
    find ./ -size +10c
    
    查找文件size小于10k的文件或目录
    find ./ -size -10k
    
    查找文件size小于10M的文件或目录
    find ./ -size -10M
    
    查找文件size小于10G的文件或目录
    find ./ -size -10G
    
### cp命令的几个参数的意义:
- a 该选项通常在拷贝目录时使用。它保留链接、文件属性，并递归地拷贝目录，其作用等于dpR选项的组合。(复制的时候要保留文件属性用-a，不然会导致服务无法应用等问题，例如原文件拥有者为Oracle，直接cp后文件拥有者变为root，会导致数据库服务器无法使用，可以使用chown修改文件拥有者，或者复制的时候直接用cp -a命令)


- d 拷贝时保留链接。


- f 删除已经存在的目标文件而不提示。


- i 和f选项相反，在覆盖目标文件之前将给出提示要求用户确认。回答y时目标文件将被覆盖，是交互式拷贝。


- p 此时cp除复制源文件的内容外，还将把其修改时间和访问权限也复制到新文件中。


- r 若给出的源文件是一目录文件，此时cp将递归复制该目录下所有的子目录和文件。此时目标文件必须为一个目录名。


- l 不作拷贝，只是链接文件。
需要说明的是，为防止用户在不经意的情况下用cp命令破坏另一个文件，如用户指定的目标文件名已存在，用cp命令拷贝文件后，这个文件就会被新源文件覆盖，因此，建议用户在使用cp命令拷贝文件时，最好使用i选项。
    
    
###  Linux下怎样检查、如何查看某软件包是否已经安装？

	因为linux安装软件的方式比较多，所以没有一个通用的办法能查到某些软件是否安装了。总结起来就是这样几类：

	1、rpm包安装的，可以用rpm -qa看到，如果要查找某软件包是否安装，用 rpm -qa | grep “软件或者包的名字”。

	[root@hexuweb102 ~] rpm -qa | grep ruby

	2、以deb包安装的，可以用dpkg -l能看到。如果是查找指定软件包，用dpkg -l | grep “软件或者包的名字”；

	[root@hexuweb102 ~] dpkg -l | grep ruby

	3、yum方法安装的，可以用yum list installed查找，如果是查找指定包，命令后加 | grep “软件名或者包名”；

	[root@hexuweb102 ~] yum list installed | grep ruby

	4、如果是以源码包自己编译安装的，例如.tar.gz或者tar.bz2形式的，这个只能看可执行文件是否存在了，

	上面两种方法都看不到这种源码形式安装的包。如果是以root用户安装的，可执行程序通常都在/sbin:/usr/bin目录下。

	说明：

	其中rpm yum Redhat系linux的软件包管理命令，dpkg debian系列的软件包管理命令   
		
		
		
### Linux 查找已安装软件的方法

	1.rpm

	注意rpm区分大小写

	查询已安装的以mysql开头的包

	rpm  -qa mysql*

	查询已安装的mysql 包

	rpm -qa|grep mysql

	 

	rpm的方法有时候也所有已安装的包

	 

	2.yum

	列出指定包的所有情况

	yum list package

	 

	yum list | grep installed

	 

	3.whereis

	有时候可以借助查找文件的方式找到对应包的路径

	例如whereis mysql

	 

	4.find

	可以使用find查找文件的所在路径

	find 查找路径 查找参数

	在根目录下查找以.conf结尾的文件
	find / -name *.conf
	 

	5.locate

	locate的功能和find类似

	locate 查找的文件
	查找所有路径下的mysql文件

	locate mysql

	 

	6.ps

	可以通过查找进程的方法找到对应的包的路径

	ps -ef|grep mysql

	可以简写成

	pgrep mysql

		
### Linux查看系统信息的一些命令及查看已安装软件包的命令

	系统

	# uname -a               # 查看内核/操作系统/CPU信息
	# head -n 1 /etc/issue   # 查看操作系统版本
	# cat /proc/cpuinfo      # 查看CPU信息
	# hostname               # 查看计算机名
	# lspci -tv              # 列出所有PCI设备
	# lsusb -tv              # 列出所有USB设备
	# lsmod                  # 列出加载的内核模块
	# env                    # 查看环境变量

	资源

	# free -m                # 查看内存使用量和交换区使用量
	# df -h                  # 查看各分区使用情况
	# du -sh <目录名>        # 查看指定目录的大小
	# grep MemTotal /proc/meminfo   # 查看内存总量
	# grep MemFree /proc/meminfo    # 查看空闲内存量
	# uptime                 # 查看系统运行时间、用户数、负载
	# cat /proc/loadavg      # 查看系统负载

	磁盘和分区

	# mount | column -t      # 查看挂接的分区状态
	# fdisk -l               # 查看所有分区
	# swapon -s              # 查看所有交换分区
	# hdparm -i /dev/hda     # 查看磁盘参数(仅适用于IDE设备)
	# dmesg | grep IDE       # 查看启动时IDE设备检测状况

	网络
	
	# ifconfig               # 查看所有网络接口的属性
	# iptables -L            # 查看防火墙设置
	# route -n               # 查看路由表
	# netstat -lntp          # 查看所有监听端口
	# netstat -antp          # 查看所有已经建立的连接
	# netstat -s             # 查看网络统计信息

	进程
	
	# ps -ef                 # 查看所有进程
	# top                    # 实时显示进程状态

	用户
	
	# w                      # 查看活动用户
	# id <用户名>            # 查看指定用户信息
	# last                   # 查看用户登录日志
	# cut -d: -f1 /etc/passwd   # 查看系统所有用户
	# cut -d: -f1 /etc/group    # 查看系统所有组
	# crontab -l             # 查看当前用户的计划任务

	服务
	
	# chkconfig --list       # 列出所有系统服务
	# chkconfig --list | grep on    # 列出所有启动的系统服务

	程序
	
	# rpm -qa                # 查看所有安装的软件包
	 

	 

	RPM

		在Linux 操作系统中，有一个系统软件包，它的功能类似于Windows里面的“添加/删除程序”，但是功能又比“添加/删除程序”强很多，它就是 Red Hat Package Manager(简称RPM)。此工具包最先是由Red Hat公司推出的，后来被其他Linux开发商所借用。由于它为Linux使用者省去了很多时间，所以被广泛应用于在Linux下安装、删除软件。下面就 给大家介绍一下它的具体使用方法。

	1.我们得到一个新软件，在安装之前，一般都要先查看一下这个软件包里有什么内容，假设这个文件是：Linux-1.4-6.i368.rpm，我们可以用这条命令查看：

	rpm -qpi Linux-1.4-6.i368.rpm

	系统将会列出这个软件包的详细资料，包括含有多少个文件、各文件名称、文件大小、创建时间、编译日期等信息。

	2.上面列出的所有文件在安装时不一定全部安装，就像Windows下程序的安装方式分为典型、完全、自定义一样，Linux也会让你选择安装方式，此时我们可以用下面这条命令查看软件包将会在系统里安装哪些部分，以方便我们的选择：

	rpm -qpl Linux-1.4-6.i368.rpm

	3. 选择安装方式后，开始安装。我们可以用rpm-ivh Linux-1.4-6.i368.rpm命令安装此软件。在安装过程中，若系统提示此软件已安装过或因其他原因无法继续安装，但若我们确实想执行安装命 令，可以在 -ivh后加一参数“-replacepkgs”：

	rpm -ivh -replacepkgs Linux-1.4-6.i368.rpm

	4.有时我们卸载某个安装过的软件，只需执行rpm-e <文件名>;命令即可。

	5.对低版本软件进行升级是提高其功能的好办法，这样可以省去我们卸载后再安装新软件的麻烦，要升级某个软件，只须执行如下命令：rpm -uvh <文件名>;，注意：此时的文件名必须是要升级软件的升级补丁

	6. 另外一个安装软件的方法可谓是Linux的独到之处，同时也是RMP强大功能的一个表现：通过FTP站点直接在线安装软件。当找到含有你所需软件的站点并 与此网站连接后，执行下面的命令即可实现在线安装，譬如在线安装Linux-1.4-6.i368.rpm，可以用命令：

	rpm -i ftp://ftp.pht.com/pub/linux/redhat/...-1.4-6.i368.rpm

	7. 在我们使用电脑过程中，难免会有误操作，若我们误删了几个文件而影响了系统的性能时，怎样查找到底少了哪些文件呢?RPM软件包提供了一个查找损坏文件的 功能，执行此命令：rpm -Va即可，Linux将为你列出所有损坏的文件。你可以通过Linux的安装光盘进行修复。

	8.Linux系统中文件繁多，在使用过程中，难免会碰到我们不认识的文件，在Windows下我们可以用“开始/查找”菜单快速判断某个文件属于哪个文件夹，在Linux中，下面这条命令行可以帮助我们快速判定某个文件属于哪个软件包：

	rpm -qf <文件名>;

	9.当每个软件包安装在Linux系统后，安装文件都会到RPM数据库中“报到”，所以，我们要查询某个已安装软件的属性时，只需到此数据库中查找即可。注意：此时的查询命令不同于1和8介绍的查询，这种方法只适用于已安装过的软件包！命令格式：

	rpm -参数　<文件名>;

	 

	APT-GET

	apt-get update——在修改/etc/apt/sources.list或者/etc/apt/preferences之后运行该命令。此外您需要定期运行这一命令以确保您的软件包列表是最新的。 
	apt-get install packagename——安装一个新软件包（参见下文的aptitude） 
	apt-get remove packagename——卸载一个已安装的软件包（保留配置文件） 
	apt-get --purge remove packagename——卸载一个已安装的软件包（删除配置文件） 
	dpkg --force-all --purge packagename 有些软件很难卸载，而且还阻止了别的软件的应用，就可以用这个，不过有点冒险。 
	apt-get autoclean apt会把已装或已卸的软件都备份在硬盘上，所以如果需要空间的话，可以让这个命令来删除你已经删掉的软件 
	apt-get clean 这个命令会把安装的软件的备份也删除，不过这样不会影响软件的使用的。 
	apt-get upgrade——更新所有已安装的软件包 
	apt-get dist-upgrade——将系统升级到新版本 
	apt-cache search string——在软件包列表中搜索字符串 
	dpkg -l package-name-pattern——列出所有与模式相匹配的软件包。如果您不知道软件包的全名，您可以使用“*package-name-pattern*”。 
	aptitude——详细查看已安装或可用的软件包。与apt-get类似，aptitude可以通过命令行方式调用，但仅限于某些命令——最常见的有安装和卸载命令。由于aptitude比apt-get了解更多信息，可以说它更适合用来进行安装和卸载。 
	apt-cache showpkg pkgs——显示软件包信息。 
	apt-cache dumpavail——打印可用软件包列表。 
	apt-cache show pkgs——显示软件包记录，类似于dpkg –print-avail。 
	apt-cache pkgnames——打印软件包列表中所有软件包的名称。 
	dpkg -S file——这个文件属于哪个已安装软件包。 
	dpkg -L package——列出软件包中的所有文件。 
	apt-file search filename——查找包含特定文件的软件包（不一定是已安装的），这些文件的文件名中含有指定的字符串。apt-file是一个独立的软件包。您必须 先使用apt-get install来安装它，然后运行apt-file update。如果apt-file search filename输出的内容太多，您可以尝试使用apt-file search filename | grep -w filename（只显示指定字符串作为完整的单词出现在其中的那些文件名）或者类似方法，例如：apt-file search filename | grep /bin/（只显示位于诸如/bin或/usr/bin这些文件夹中的文件，如果您要查找的是某个特定的执行文件的话，这样做是有帮助的）。
				
### Linux软连接和硬链接
	1.Linux链接概念
	Linux链接分两种，一种被称为硬链接（Hard Link），另一种被称为符号链接（Symbolic Link）。默认情况下，ln命令产生硬链接。

	【硬连接】
	硬连接指通过索引节点来进行连接。在Linux的文件系统中，保存在磁盘分区中的文件不管是什么类型都给它分配一个编号，称为索引节点号(Inode Index)。在Linux中，多个文件名指向同一索引节点是存在的。一般这种连接就是硬连接。硬连接的作用是允许一个文件拥有多个有效路径名，这样用户就可以建立硬连接到重要文件，以防止“误删”的功能。其原因如上所述，因为对应该目录的索引节点有一个以上的连接。只删除一个连接并不影响索引节点本身和其它的连接，只有当最后一个连接被删除后，文件的数据块及目录的连接才会被释放。也就是说，文件真正删除的条件是与之相关的所有硬连接文件均被删除。

	注：使得同一个文件可以被不同的程序所使用，使用的名字可以不一样。比如源文件file1，创建2个硬链接file2、file3，修改file1，file2和file3的内容会同样变化。硬连接文件和源文件信息一模一样无法区分，连接数从ls -l命令的第二列可看出。

	【软连接】
	另外一种连接称之为符号连接（Symbolic Link），也叫软连接。软链接文件有类似于Windows的快捷方式。它实际上是一个特殊的文件。在符号连接中，文件实际上是一个文本文件，其中包含的有另一文件的位置信息。

	2.通过实验加深理解
	[oracle@Linux]$ touch f1          #创建一个测试文件f1
	[oracle@Linux]$ ln f1 f2          #创建f1的一个硬连接文件f2
	[oracle@Linux]$ ln -s f1 f3       #创建f1的一个符号连接文件f3
	[oracle@Linux]$ ls -li            # -i参数显示文件的inode节点信息
	total 0
	9797648 -rw-r--r--  2 oracle oinstall 0 Apr 21 08:11 f1
	9797648 -rw-r--r--  2 oracle oinstall 0 Apr 21 08:11 f2
	9797649 lrwxrwxrwx  1 oracle oinstall 2 Apr 21 08:11 f3 -> f1

	从上面的结果中可以看出，硬连接文件f2与原文件f1的inode节点相同，均为9797648，然而符号连接文件的inode节点不同。

	[oracle@Linux]$ echo "I am f1 file" >>f1
	[oracle@Linux]$ cat f1
	I am f1 file
	[oracle@Linux]$ cat f2
	I am f1 file
	[oracle@Linux]$ cat f3
	I am f1 file
	[oracle@Linux]$ rm -f f1
	[oracle@Linux]$ cat f2
	I am f1 file
	[oracle@Linux]$ cat f3
	cat: f3: No such file or directory

	通过上面的测试可以看出：当删除原始文件f1后，硬连接f2不受影响，但是符号连接f1文件无效

	3.总结
	依此您可以做一些相关的测试，可以得到以下全部结论：
	1).删除符号连接f3,对f1,f2无影响；
	2).删除硬连接f2，对f1,f3也无影响；
	3).删除原文件f1，对硬连接f2没有影响，导致符号连接f3失效；
	4).同时删除原文件f1,硬连接f2，整个文件会真正的被删除。

	注：硬链接不可以跨文件系统建立，软连接可以跨文件系统建立，即可以跨主机建立软连接。
					
					
					
					
					
					
