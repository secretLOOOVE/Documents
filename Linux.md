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
					
					
### Linux: wget 使用技巧

	wget 是一个命令行的下载工具。对于我们这些 Linux 用户来说，几乎每天都在使用它。下面为大家介绍几个有用的 wget 小技巧，可以让你更加高效而灵活的使用 wget。
	 
	Java代码  收藏代码
	$ wget -r -np -nd http://example.com/packages/  
	这条命令可以下载 http://example.com 网站上 packages 目录中的所有文件。其中，-np 的作用是不遍历父目录，-nd 表示不在本机重新创建目录结构。
	 
	Java代码  收藏代码
	$ wget -r -np -nd --accept=iso http://example.com/centos-5/i386/  
	与上一条命令相似，但多加了一个 --accept=iso 选项，这指示 wget 仅下载 i386 目录中所有扩展名为 iso 的文件。你也可以指定多个扩展名，只需用逗号分隔即可。
	 
	Java代码  收藏代码
	$ wget -i filename.txt  
	此命令常用于批量下载的情形，把所有需要下载文件的地址放到 filename.txt 中，然后 wget 就会自动为你下载所有文件了。
	 
	Java代码  收藏代码
	$ wget -c http://example.com/really-big-file.iso  
	这里所指定的 -c 选项的作用为断点续传。
	 
	Java代码  收藏代码
	$ wget -m -k (-H) http://www.example.com/  
	该命令可用来镜像一个网站，wget 将对链接进行转换。如果网站中的图像是放在另外的站点，那么可以使用 -H 选项。
	 
	来源：http://linuxtoy.org/archives/wget-tips.html
	 
	更多命令：
	用法： wget [选项]... [URL]...

	长选项所必须的参数在使用短选项时也是必须的。

	启动：
	  -V,  --version           显示 Wget 的版本信息并退出。
	  -h,  --help              打印此帮助。
	  -b,  --background        启动后转入后台。
	  -e,  --execute=COMMAND   运行一个“.wgetrc”风格的命令。

	日志和输入文件：
	  -o,  --output-file=FILE    将日志信息写入 FILE。
	  -a,  --append-output=FILE  将信息添加至 FILE。
	  -d,  --debug               打印大量调试信息。
	  -q,  --quiet               安静模式 (无信息输出)。
	  -v,  --verbose             详尽的输出 (此为默认值)。
	  -nv, --no-verbose          关闭详尽输出，但不进入安静模式。
	  -i,  --input-file=FILE     下载本地或外部 FILE 中的 URLs。
	  -F,  --force-html          把输入文件当成 HTML 文件。
	  -B,  --base=URL            解析与 URL 相关的
								 HTML 输入文件 (由 -i -F 选项指定)。
		   --config=FILE         Specify config file to use.

	下载：
	  -t,  --tries=NUMBER            设置重试次数为 NUMBER (0 代表无限制)。
		   --retry-connrefused       即使拒绝连接也是重试。
	  -O,  --output-document=FILE    将文档写入 FILE。
	  -nc, --no-clobber              skip downloads that would download to
									 existing files (overwriting them).
	  -c,  --continue                断点续传下载文件。
		   --progress=TYPE           选择进度条类型。
	  -N,  --timestamping            只获取比本地文件新的文件。
	  --no-use-server-timestamps     不用服务器上的时间戳来设置本地文件。
	  -S,  --server-response         打印服务器响应。
		   --spider                  不下载任何文件。
	  -T,  --timeout=SECONDS         将所有超时设为 SECONDS 秒。
		   --dns-timeout=SECS        设置 DNS 查寻超时为 SECS 秒。
		   --connect-timeout=SECS    设置连接超时为 SECS 秒。
		   --read-timeout=SECS       设置读取超时为 SECS 秒。
	  -w,  --wait=SECONDS            等待间隔为 SECONDS 秒。
		   --waitretry=SECONDS       在获取文件的重试期间等待 1..SECONDS 秒。
		   --random-wait             获取多个文件时，每次随机等待间隔
									 0.5*WAIT...1.5*WAIT 秒。
		   --no-proxy                禁止使用代理。
	  -Q,  --quota=NUMBER            设置获取配额为 NUMBER 字节。
		   --bind-address=ADDRESS    绑定至本地主机上的 ADDRESS (主机名或是 IP)。
		   --limit-rate=RATE         限制下载速率为 RATE。
		   --no-dns-cache            关闭 DNS 查寻缓存。
		   --restrict-file-names=OS  限定文件名中的字符为 OS 允许的字符。
		   --ignore-case             匹配文件/目录时忽略大小写。
	  -4,  --inet4-only              仅连接至 IPv4 地址。
	  -6,  --inet6-only              仅连接至 IPv6 地址。
		   --prefer-family=FAMILY    首先连接至指定协议的地址
									 FAMILY 为 IPv6，IPv4 或是 none。
		   --user=USER               将 ftp 和 http 的用户名均设置为 USER。
		   --password=PASS           将 ftp 和 http 的密码均设置为 PASS。
		   --ask-password            提示输入密码。
		   --no-iri                  关闭 IRI 支持。
		   --local-encoding=ENC      IRI (国际化资源标识符) 使用 ENC 作为本地编码。
		   --remote-encoding=ENC     使用 ENC 作为默认远程编码。
		   --unlink                  remove file before clobber.

	目录：
	  -nd, --no-directories           不创建目录。
	  -x,  --force-directories        强制创建目录。
	  -nH, --no-host-directories      不要创建主目录。
		   --protocol-directories     在目录中使用协议名称。
	  -P,  --directory-prefix=PREFIX  以 PREFIX/... 保存文件
		   --cut-dirs=NUMBER          忽略远程目录中 NUMBER 个目录层。

	HTTP 选项：
		   --http-user=USER        设置 http 用户名为 USER。
		   --http-password=PASS    设置 http 密码为 PASS。
		   --no-cache              不在服务器上缓存数据。
		   --default-page=NAME     改变默认页
								   (默认页通常是“index.html”)。
	  -E,  --adjust-extension      以合适的扩展名保存 HTML/CSS 文档。
		   --ignore-length         忽略头部的‘Content-Length’区域。
		   --header=STRING         在头部插入 STRING。
		   --max-redirect          每页所允许的最大重定向。
		   --proxy-user=USER       使用 USER 作为代理用户名。
		   --proxy-password=PASS   使用 PASS 作为代理密码。
		   --referer=URL           在 HTTP 请求头包含‘Referer: URL’。
		   --save-headers          将 HTTP 头保存至文件。
	  -U,  --user-agent=AGENT      标识为 AGENT 而不是 Wget/VERSION。
		   --no-http-keep-alive    禁用 HTTP keep-alive (永久连接)。
		   --no-cookies            不使用 cookies。
		   --load-cookies=FILE     会话开始前从 FILE 中载入 cookies。
		   --save-cookies=FILE     会话结束后保存 cookies 至 FILE。
		   --keep-session-cookies  载入并保存会话 (非永久) cookies。
		   --post-data=STRING      使用 POST 方式；把 STRING 作为数据发送。
		   --post-file=FILE        使用 POST 方式；发送 FILE 内容。
		   --content-disposition   当选中本地文件名时
								   允许 Content-Disposition 头部 (尚在实验)。
		   --auth-no-challenge     发送不含服务器询问的首次等待
								   的基本 HTTP 验证信息。

	HTTPS (SSL/TLS) 选项：
		   --secure-protocol=PR     选择安全协议，可以是 auto、SSLv2、
									SSLv3 或是 TLSv1 中的一个。
		   --no-check-certificate   不要验证服务器的证书。
		   --certificate=FILE       客户端证书文件。
		   --certificate-type=TYPE  客户端证书类型，PEM 或 DER。
		   --private-key=FILE       私钥文件。
		   --private-key-type=TYPE  私钥文件类型，PEM 或 DER。
		   --ca-certificate=FILE    带有一组 CA 认证的文件。
		   --ca-directory=DIR       保存 CA 认证的哈希列表的目录。
		   --random-file=FILE       带有生成 SSL PRNG 的随机数据的文件。
		   --egd-file=FILE          用于命名带有随机数据的 EGD 套接字的文件。

	FTP 选项：
		   --ftp-user=USER         设置 ftp 用户名为 USER。
		   --ftp-password=PASS     设置 ftp 密码为 PASS。
		   --no-remove-listing     不要删除‘.listing’文件。
		   --no-glob               不在 FTP 文件名中使用通配符展开。
		   --no-passive-ftp        禁用“passive”传输模式。
		   --retr-symlinks         递归目录时，获取链接的文件 (而非目录)。

	递归下载：
	  -r,  --recursive          指定递归下载。
	  -l,  --level=NUMBER       最大递归深度 (inf 或 0 代表无限制，即全部下载)。
		   --delete-after       下载完成后删除本地文件。
	  -k,  --convert-links      让下载得到的 HTML 或 CSS 中的链接指向本地文件。
	  -K,  --backup-converted   在转换文件 X 前先将它备份为 X.orig。
	  -m,  --mirror             -N -r -l inf --no-remove-listing 的缩写形式。
	  -p,  --page-requisites    下载所有用于显示 HTML 页面的图片之类的元素。
		   --strict-comments    用严格方式 (SGML) 处理 HTML 注释。

	递归接受/拒绝：
	  -A,  --accept=LIST               逗号分隔的可接受的扩展名列表。
	  -R,  --reject=LIST               逗号分隔的要拒绝的扩展名列表。
	  -D,  --domains=LIST              逗号分隔的可接受的域列表。
		   --exclude-domains=LIST      逗号分隔的要拒绝的域列表。
		   --follow-ftp                跟踪 HTML 文档中的 FTP 链接。
		   --follow-tags=LIST          逗号分隔的跟踪的 HTML 标识列表。
		   --ignore-tags=LIST          逗号分隔的忽略的 HTML 标识列表。
	  -H,  --span-hosts                递归时转向外部主机。
	  -L,  --relative                  只跟踪有关系的链接。
	  -I,  --include-directories=LIST  允许目录的列表。
	  --trust-server-names             use the name specified by the redirection
									   url last component.
	  -X,  --exclude-directories=LIST  排除目录的列表。
	  -np, --no-parent                 不追溯至父目录。
	 
	Java代码  收藏代码
	[root@localhost ~]# wget http://tel.mirrors.163.com/centos/6.4/isos/x86_64/CentOS-6.4-x86_64-bin-DVD1.iso    #下载centos境像  
	  
	[root@localhost ~]# wget -c http://tel.mirrors.163.com/centos/6.4/isos/x86_64/CentOS-6.4-x86_64-bin-DVD1.iso    #断点下载  
	  
	[root@localhost ~]# wget -P /home/download http://tel.mirrors.163.com/centos/6.4/isos/x86_64/CentOS-6.4-x86_64-bin-DVD1.iso    #指定目录下载  
	  
	[root@localhost ~]# wget -Q 1M http://tel.mirrors.163.com/centos/6.4/isos/x86_64/CentOS-6.4-x86_64-bin-DVD1.iso    #限定最大下载速度  
	  
	[root@localhost ~]# wget -r -np -nd http://tel.mirrors.163.com/centos/6.4/os/x86_64/   #下载 http://tel.mirrors.163.com/centos/6.4/os/x86_64/ 目录中的所有文件  
	  
	wget -c -r --level=1 -k -p -np http://docs.Python.org/2/tutorial/index.html   #下载一个网站的本地镜像  
						

### RPM/DPKG 两大阵营简介

	在 GNU/Linux( 以下简称 Linux) 操作系统中，RPM 和 DPKG 为最常见的两类软件包管理工具，他们分别应用于基于 RPM 软件包的 Linux 发行版本和 DEB 软件包的 Linux 发行版本。软件包管理工具的作用是提供在操作系统中安装，升级，卸载需要的软件的方法，并提供对系统中所有软件状态信息的查询。
	RPM 全称为 Redhat Package Manager，最早由 Red Hat 公司制定实施，随后被 GNU 开源操作系统接受并成为很多 Linux 系统 (RHEL) 的既定软件标准。与 RPM 进行竞争的是基于 Debian 操作系统 (UBUNTU) 的 DEB 软件包管理工具－ DPKG，全称为 Debian Package，功能方面与 RPM 相似。二者之具体比较不在本文范围之内。
	回页首
	RPM 包的安装 / 升级 / 查询 / 卸载
	一个 RPM 包包含了已压缩的软件文件集以及该软件的内容信息（在头文件中保存），通常表现为以 .rpm 扩展名结尾的文件，例如 package.rpm 。对其操作，需要使用 rpm 命令。下面介绍 rpm 工具的参数和使用方法，并以 IBM Lotus Notes 在 RHEL 5.2 安装为例做具体说明。
	RPM 命令常用参数
	RPM 的常规使用方法为 rpm -? package.rpm，其中 -? 为操作参数 ( 更多信息，请查阅帮助 $man rpm)：
	-q 在系统中查询软件或查询指定 rpm 包的内容信息
	-i 在系统中安装软件
	-U 在系统中升级软件
	-e 在系统中卸载软件
	-h 用 #(hash) 符显示 rpm 安装过程
	-v 详述安装过程
	-p 表明对 RPM 包进行查询，通常和其它参数同时使用，如：
	-qlp 查询某个 RPM 包中的所有文件列表
	-qip 查询某个 RPM 包的内容信息
	RPM 命令参数使用方法
	以上参数有些需要组合使用，比如说 rpm -h package.rpm 是没有意义的，但 rpm -ih package.rpm 即表示安装 package 并用 # 符显示安装进度。
	安装 RPM 包
	# rpm -ivh package.rpm
	升级 RPM 包命令
	# rpm -Uvh package.rpm
	卸载 RPM 包命令
	# rpm -ev package
	查询 RPM 包中包含的文件列表命令
	# rpm -qlp package
	查询 RPM 包中包含的文件列表命令
	# rpm -qlp package
	查询 RPM 包中包含的内容信息命令
	# rpm -qip package
	查询系统中所有已安装 RPM 包
	# rpm -qa
	RPM 包管理示例
	以下步骤描述了一个普通用户安装 IBM Lotus Notes V85 ( 以下简称 Notes) 的典型操作过程。 Notes 的 RPM 包名为 ibm_lotus_notes-8.5.i586.rpm 。
	首先查询是否该软件是否已经在系统中存在
	# rpm -qa | grep ibm_lotus_notes
	如果返回信息为空那么说明该软件还未被安装。
	查询 Notes 软件包内容：
	# rpm -qip ibm_lotus_notes-8.5.i586.rpm 
				
	 Name        : ibm_lotus_notes           Relocations: /opt/ibm/lotus/notes 
	 Version     : 8.5                               Vendor: IBM 
	 Release     : 20081211.1925             Build Date: Sat 13 Dec 2008 09:38:55 AM CST 
	 Install Date: (not installed)               Build Host: dithers.notesdev.ibm.com 
	 Group       : Applications/Office           
	 Source RPM: ibm_lotus_notes-8.5-20081211.1925.src.rpm 
	 Size        : 603779427                        License: Commercial 
	 Signature   : DSA/SHA1, Sat 13 Dec 2008 09:43:02 AM CST, Key ID 314c8c6534f9ae75 
	 Summary     : IBM Lotus Notes 
	 Description : 
	 IBM Lotus Notes software provides a robust ...
	安装 Notes:
	# rpm -ivh ibm_lotus_notes-8.5.i586.rpm
	返回信息 :
	   Preparing...                ########################################### [100%] 
	   1:ibm_lotus_notes        ########################################### [100%]
	升级 Notes：
	若今后需要基于该版本升级至更高版本的 Notes( 缝 .0 - ibm_lotus_notes-9.0.i586.rpm)，则使用 -U 参数：
	# rpm -Uvh ibm_lotus_notes-8.5.i586.rpm
	在该步骤中如果使用 -i 则系统通常会报文件冲突错误，无法正常安装。
	卸载 Notes
	注意卸载软件使用软件名称，而不是包文件名：
	# rpm -ev ibm_lotus_notes
	回页首
	DEB 包的安装 / 升级 / 查询 / 卸载
	一个 DEB 包包含了已压缩的软件文件集以及该软件的内容信息（在头文件中保存），通常表现为以 .deb 扩展名结尾的文件，例如 package.deb 。对其操作，需要使用 dpkg 命令。下面介绍 dpkg 工具的参数和使用方法，并以 IBM Lotus Notes 在 UBUNTU 904 安装为例做具体说明。
	DPKG 命令常用参数
	DPKG 的常规使用方法为 dpkg -? Package(.rpm), 其中 -? 为安装参数 ( 更多信息，请查阅帮助 $man rpm)：
	-l 在系统中查询软件内容信息
	--info 在系统中查询软件或查询指定 rpm 包的内容信息
	-i 在系统中安装 / 升级软件
	-r 在系统中卸载软件 , 不删除配置文件
	-P 在系统中卸载软件以及其配置文件
	DPKG 命令参数使用方法
	安装 DEB 包命令
	$ sudo dpkg -i package.deb
	升级 DEB 包命令
	$ sudo dpkg -i package.deb ( 和安装命令相同）
	卸载 DEB 包命令
	$ sudo dpkg -r package.deb # 不卸载配置文件
	或
	 $ sudo dpkg -P package.deb # 卸载配置文件
	查询 DEB 包中包含的文件列表命令
	$ sudo dpkg-deb -c package.deb
	查询 DEB 包中包含的内容信息命令
	$ dpkg --info package.deb
	查询系统中所有已安装 DEB 包
	$ dpkg -l package
	DEB 包管理示例
	以下步骤描述了一个普通用户安装 IBM Lotus Notes V85 ( 以下简称 Notes) 的典型操作过程。 Notes 的 DEB 包名为 ibm_lotus_notes-8.5.i586.deb.
	首先查询是否该软件是否已经在系统中存在
	$ dpkg -l ibm-lotus-*
	如果系统中从未安装过 Lotus 产品，那么返回信息为 :
	No pakcages found matching ibm-lotus-*
	如果系统安装过 Lotus 产品，但已被删除，那么返回信息为 :
	pn ibm-lotus-notes none (no description available)
	查询 Notes 软件包内容：
	$ dpkg --info ibm_lotus_notes-8.5-i586.deb
	返回信息 :
	new debian package, version 2.0. 
	 size 335012296 bytes: control archive= 231821 bytes. 
	 ... 
	 Package: ibm-lotus-notes 
	 Version: 8.5-20081211.1925 
	 Section: IBM 
	 Priority: extra 
	 Architecture: i386 
	 Installed-Size: 619444 
	 Maintainer: IBM Lotus Product 
	 Description: IBM Lotus Notes 
	  IBM Lotus Notes software provides a robust ... ...
	安装 Notes:
	$ sudo dpkg -i ibm_lotus_notes-8.5.i586.deb
	返回信息 :
	(Reading database ... 151150 files and directories currently installed.) 
	 Preparing to replace ibm-lotus-notes 8.5-20081211.1925 
	 (using ibm-lotus-notes-higher-version.i586.deb) ... 
	 Unpacking replacement ibm-lotus-notes ... 

	 Setting up ibm-lotus-notes (higher-version) ...
	升级 Notes：
	$ sudo dpkg -i ibm_lotus_notes-8.5.i586.deb
	返回信息 :
	(Reading database ... 151150 files and directories currently installed.) 
	 Preparing to replace ibm-lotus-notes 8.5-20081211.1925 
	 (using ibm-lotus-notes-higher-version.i586.deb) ... 
	 Unpacking replacement ibm-lotus-notes ... 

	 Setting up ibm-lotus-notes (higher-version) ...
	卸载 Notes
	注意卸载软件使用软件名称，而不是包文件名：
	$ sudo dpkg -P ibm-lotus-notes
	回页首
	软件包依赖性关系
	由于开源的多态性，Linux 操作系统中的软件之间的依赖性关系处理一直令用户感到头疼。如果 package_a 依赖于 package_b，那么在一个没有安装 package_b 的系统中，package_a 是不被系统推荐安装的，强制安装很可能会导致软件无法正常工作。基于以上 package_a 和 package_b 的关系，在一个干净的系统中 ( 未安装 package_a 或 package_b)，欲安装 package_a，错误通常会表现为：
	RHEL 5.2
	# rpm -ivh package_a.rpm 

	 error: Failed dependencies: 
			pacakge_b = version info is needed by package_a
	Ubuntu 904
	$ sudo dpkg -i package_a.deb 

	 dpkg: regarding package_a.deb containing package, pre-dependency problm: 
	  package_a pre-depends on package_b (version info) 
	 dpkg: error processing package_a.deb (--install): 
	  pre-dependency problem - not installing package_a 
	 Errors were encountered while processing: 
	  package_a.deb
	查询软件包依赖关系
	查询 RPM 包的依赖关系，使用 rpm -qRp:
	# rpm -qRp package_a.rpm 

	 package_b = version_info 
	或
	 package_b >= version_info 
	或
	 package_b <= version_info
	表明 package_a.rpm 依赖于 version_info 版的 package_b，或者任何高于并包括 version_info 版的 package_b，亦或低于或包括 version_info 版的 package_b 。所以 package_b.rpm 必须在 package_a 之前安装于系统中。
	查询 DEB 包的依赖关系，可解读 dpkg --info 结果中的 Pre-Depends 字段：
	$ dpkg --info package_a.deb 

	 Pre-depends: package_b (= version_info) 
	 Depends: package_b (= version_info) 
	或
	 Pre-depends: package_b (>= version_info) 
	 Depends: package_b (>= version_info) 
	或
	 Pre-depends: package_b (<= version_info) 
	 Depends: package_b (<= version_info)
	表明 package_a.deb 依赖于 version_info 版的 package_b 或者任何高于并包括 version_info 版的 package_b 亦或低于或包括 version_info 版的 package_b. 所以 package_b.deb 必须在 package_a 之前安装于系统中。
	所以正确的安装方法如下节所示。
	安装方法
	对于 package_a，正确的安装方法应该是：
	##RPM 
	 # rpm -ivh package_b.rpm 
	 # rpm -ivh package_a.rpm 

	 ##DEB 
	 $ sudo dpkg -i package_b.deb 
	 $ sudo dpkg -i package_a.deb
	嵌套的依赖关系
	如上示例为最理想的依赖关系，实际应用中往往最令用户头疼的是 package_a 依赖于 package_b/c/d/e/f 等多个包 , 而 package_b/c/d/e/f 等包又依赖于 package_b1,b2,b3/c1,c2/d1,d2/e1,e2/f1,f2 等等 ... ... 为保证软件的正常使用，必须找到所有依赖包以及子依赖包并且安装。过多的依赖关系大大降低了 Linux 软件安装的用户友好性。所以针对此类问题，使用了更高级的包管理策略去解决 - Yum/APT 。
	回页首
	更友好的包管理软件 - YUM
	YUM
	YUM 基于 RPM 包管理工具，能够从指定的源空间（服务器，本地目录等）自动下载目标 RPM 包并且安装，可以自动处理依赖性关系并进行下载、安装，无须繁琐地手动下载、安装每一个需要的依赖包。此外，YUM 的另一个功能是进行系统中所有软件的升级。如上所述，YUM 的 RPM 包来源于源空间，在 RHEL 中由 /etc/yum.repos.d/ 目录中的 .repo 文件配置指定，如 rhel-debuginfo.repo 的内容：
	rhel-debuginfo.repo
	[rhel-debuginfo] 
	 name=Red Hat Enterprise Linux 5Client - i386 - Debug 
	 baseurl=ftp://ftp.redhat.com/pub/redhat/linux/enterprise/5Client/en/os/i386/Debuginfo/ 
	 enabled=0 
	 gpgcheck=1 
	 gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
	YUM 的系统配置文件位于 /etc/yum.conf，内容如：
	[main] 
	 cachedir=/var/cache/yum 
	 keepcache=1 
	 debuglevel=2 
	 pkgpolicy=newest 
	 logfile=/var/log/yum.log 
	 distroverpkg=redhat-release 
	 tolerant=1 
	 exactarch=1 
	 obsoletes=1 
	 gpgcheck=1 
	 plugins=1 
	 exclude= firefox gftp
	配置文件用来定义用户期望的 yum 行为，比如，gpgcheck 表明安装时不进行 gpg 验证，exclued=firefox gftp 表明进行系统全软件升级时不升级 firefox 和 gftp 。
	YUM 常用命令
	安装指定软件 :
	# yum -y install package-name
	列出系统中已安装软件
	# yum list
	列出系统中可升级的所有软件
	# yum check-update
	升级系统中可升级的所有软件
	# yum update
	升级指定软件
	# yum update package-name
	在升级过程中接受所有互动问答
	# yum -y update
	卸载指定软件
	# yum remove package-name
	更多有关 YUM 的信息，请查阅 http://fedoraproject.org/wiki/Tools/yum 。
	回页首
	更友好的包管理软件 - APT
	APT
	APT 的全称为 Advanced Packaging Tools 。与 YUM 对应，它最早被设计成 DPKG 的前端软件，现在通过 apt-rpm 也支持 rpm 管理。而本节本节将介绍 APT 作为 DPKG 前端的使用。 APT 的主要包管理工具为 APT-GET，通过此工具可满足和上述 YUM 相似的功能要求。
	APT 的软件源定义来自 /etc/apt/sources.list 文件：
	# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to 
	 # newer versions of the distribution. 

	 deb http://cn.archive.ubuntu.com/ubuntu/ hardy main restricted 
	 deb-src http://cn.archive.ubuntu.com/ubuntu/ hardy main restricted
	注意每次手动修改上述文件后，需要使用 sudo apt-get update 来更新系统的源使新的源数据被当前系统识别。
	UBUNTU 中 APT 的配置文件位于 /etc/apt/apt.conf.d，其中的多个配置文件依功能分类。
	APT 常用命令
	更新源索引
	$ sudo apt-get update
	安装指定软件
	$ sudo apt-get install package-name
	下载指定软件的源文件
	$ sudo apt-get source package-name
	将系统中所有软件升级到最新版本
	$ sudo apt-get upgrade
	将操作系统连同所有软件升级到最新版本
	$ sudo apt-get dist-upgrade
	卸载指定软件
	$ sudo apt-get remove package-name
	更多有关 APT 的信息，请查阅 http://www.debian.org/doc/manuals/apt-howto/index.en.html 。
	回页首
	RPM 与 DEB 的兼容 - Alien
	Alien 工具可以将 RPM 软件包转换成 DEB 软件包，或把 DEB 软件包转换成 RPM 软件包，以此适应兼容性的需要。注意首先请在系统中安装 alien 。
	在 UBUNTU 中使用 alien 将 rpm 转换为 deb 并安装 :
	$ sudo alien -d package.rpm 
	 $ sudo dpkg -i package.deb
	在 RHEL 中使用 alien 将 deb 转换为 rpm 并安装 :
	# alien -r package.deb 
	 # rpm -ivh package.rpm
	更多 alien 相关信息请查阅 http://linux.die.net/man/1/alien
	回页首
	总结
	本文以 RHEL 5.2 和 Ubuntu 904 为例，基于命令行操作，介绍了 Linux 系统中两大常用软件包管理工具－ RPM 与 DPKG 。首先从最底端的 rpm/dpkg 命令操作开始列举了它们的基本使用方法，随后指出了软件的依赖关系以及由此带来的问题，并对此问题的解决方案，也是最流行的 YUM 与 APT 前端软件管理系统进行了操作介绍。最后本文简要说明了当前 RPM/DEB 的兼容性问题的常规解决方法。
	回页首
	常见问题列表
	可以手动强制不进行 RPM/DEB 的依赖性关系检查吗？
	RPM
	可以。使用 --nodeps 辅助参数，则安装过程将不理会依赖性关系限制，强制安装目标包，如：
	# rpm -i --nodeps package_a.rpm
	DEB
	可以。使用— force-depends 辅助参数，如：
	$ sudo dpkg -i --force-depends package_a.deb
	RPM 中的 --force 是干什么用的？
	RPM 中的默认安装规则是不允许同一个包多次安装的，也不允许降级安装。使用 --force 辅助参数将不考虑以上因素，强制安装 RPM 包。但是，--force 无法强制安装一个不满足系统依赖性关系的包 ( 此时需要用到 --nodeps 参数 ) 。使用方法如：
	# rpm -i --force package_a.rpm
	RPM/DPKG 支持远程安装吗？
	RPM
	是。 RPM 支持 HTTP 和 FTP 协议，如：
	# rpm -Uvh ftp://user:pass@ftpserver/package.rpm
	DPKG
	最新的基于 DEB 包的系统中，远程安装通常被更先进的 APT 代替。
	可以从 RPM/DPKG 中抽取个别文件吗？
	RPM
	是。可以使用 rpm2cpio 工具来提取文件：http://www.rpm.org/max-rpm/s1-rpm-miscellania-rpm2cpio.html
	DPKG
	是。可以使用 dpkg-deb 工具来提取文件：
	$ dpkg-deb --extract ibm_lotus_notes-8.5.i586.deb $dir( 目标目录 )
	RPM/DPKG 提供包安装成功的验证机制吗？
	RPM
	是。可以使用 -V 参数进行验证。
	DPKG
	Debian 系统通常使用 debsums 工具参数进行验证。
	RPM/DPKG 提供包安全签名吗？
	RPM
	是。可以使用 --import 导入与软件同时发布的 GPG KEY, 接着使用 -K 命令来验证包的安全性，如：
	# rpm --import pub_ibm_lotus_notes.gpg # rpm -K ibm_lotus_notes-8.5.i586.rpm 返回信息 : ibm_lotus_notes-8.5.i586.rpm: (sha1) dsa sha1 md5 gpg OK
	DPKG
	DPKG 不提供原生的 Key 验证机制。可以使用 debsigs 和 debsigs-verify，详情请见：http://man.ddvip.com/os/debiansecuring-howto/ch7.zh-cn.html
	如果 RPM 的底层数据库损坏，RPM 还能使用吗？
	RPM
	如果底层数据库损坏，RPM 将无法正常使用。此时最常用的解决方法是重构数据库：
	# rm -f /var/lib/rpm/__* ; rpm -vv --rebuilddb
	RPM
	DPKG 本身不提供底层数据库恢复机制。它的数据库以文件形式保存在 /var/lib/dpkg 目录中。及时地备份这个目录是最好的预防数据库损坏措施。
	可以查询系统中已经安装的某个文件属于哪个 RPM 包吗？
	RPM
	可以。使用 -qf 参数 , 如在安装了 Notes8.5 的系统中：
	# rpm -qf /opt/ibm/lotus/notes/notes 返回信息 : Ibm_lotus_notes-8.5-20081211.1920
	DPKG
	可以。使用— search 参数 , 如在安装了 Notes8.5 的系统中：
	$ dpkg --search /opt/ibm/lotus/notes/notes 返回信息 : ibm-lotus-notes: /opt/ibm/lotus/notes/notes
	可以查询 RPM 包的安装时间吗？
	RPM
	可以。可使用 --last 查询。如：
	rpm -qa --last 返回信息 : 系统中所有软件的安装时间。
	DPKG
	DPKG 不提供直接的查询参数，但是可以用过查询 dpkg 的日志文件实现这个功能。如：
	cat /var/log/dpkg.log | grep "\ install\ "
	
### Linux文件系统剖析
	
	基本的文件系统体系结构
	Linux 文件系统体系结构是一个对复杂系统进行抽象化的有趣例子。通过使用一组通用的 API 函数，Linux 可以在许多种存储设备上支持许多种文件系统。例如，read 函数调用可以从指定的文件描述符读取一定数量的字节。read 函数不了解文件系统的类型，比如 ext3 或 NFS。它也不了解文件系统所在的存储媒体，比如 AT Attachment Packet Interface（ATAPI）磁盘、Serial-Attached SCSI（SAS）磁盘或 Serial Advanced Technology Attachment（SATA）磁盘。但是，当通过调用 read 函数读取一个文件时，数据会正常返回。本文讲解这个机制的实现方法并介绍 Linux 文件系统层的主要结构。

	什么是文件系统？
	首先回答最常见的问题，“什么是文件系统”。文件系统是对一个存储设备上的数据和元数据进行组织的机制。由于定义如此宽泛，支持它的代码会很有意思。正如前面提到的，有许多种文件系统和媒体。由于存在这么多类型，可以预料到 Linux 文件系统接口实现为分层的体系结构，从而将用户接口层、文件系统实现和操作存储设备的驱动程序分隔开。

	挂装
	在 Linux 中将一个文件系统与一个存储设备关联起来的过程称为挂装（mount）。使用 mount 命令将一个文件系统附着到当前文件系统层次结构中（根）。在执行挂装时，要提供文件系统类型、文件系统和一个挂装点。
	为了说明 Linux 文件系统层的功能（以及挂装的方法），我们在当前文件系统的一个文件中创建一个文件系统。实现的方法是，首先用 dd 命令创建一个指定大小的文件（使用 /dev/zero 作为源进行文件复制）—— 换句话说，一个用零进行初始化的文件，见清单 1。
	清单 1. 创建一个经过初始化的文件
	$ dd if=/dev/zero of=file.img bs=1k count=10000
	10000+0 records in
	10000+0 records out
	$
	现在有了一个 10MB 的 file.img 文件。使用 losetup 命令将一个循环设备与这个文件关联起来，让它看起来像一个块设备，而不是文件系统中的常规文件：
	$ losetup /dev/loop0 file.img
	$
	这个文件现在作为一个块设备出现（由 /dev/loop0 表示）。然后用 mke2fs 在这个设备上创建一个文件系统。这个命令创建一个指定大小的新的 ext2 文件系统，见清单 2。
	清单 2. 用循环设备创建 ext2 文件系统
	$ mke2fs -c /dev/loop0 10000
	mke2fs 1.35 (28-Feb-2004)
	max_blocks 1024000, rsv_groups = 1250, rsv_gdb = 39
	Filesystem label=
	OS type: Linux
	Block size=1024 (log=0)
	Fragment size=1024 (log=0)
	2512 inodes, 10000 blocks
	500 blocks (5.00%) reserved for the super user
	...
	$
	使用 mount 命令将循环设备（/dev/loop0）所表示的 file.img 文件挂装到挂装点 /mnt/point1。注意，文件系统类型指定为 ext2。挂装之后，就可以将这个挂装点当作一个新的文件系统，比如使用 ls 命令，见清单 3。
	清单 3. 创建挂装点并通过循环设备挂装文件系统
	$ mkdir /mnt/point1
	$ mount -t ext2 /dev/loop0 /mnt/point1
	$ ls /mnt/point1
	lost+found
	$
	如清单 4 所示，还可以继续这个过程：在刚才挂装的文件系统中创建一个新文件，将它与一个循环设备关联起来，再在上面创建另一个文件系统。
	清单 4. 在循环文件系统中创建一个新的循环文件系统
	$ dd if=/dev/zero of=/mnt/point1/file.img bs=1k count=1000
	1000+0 records in
	1000+0 records out
	$ losetup /dev/loop1 /mnt/point1/file.img
	$ mke2fs -c /dev/loop1 1000
	mke2fs 1.35 (28-Feb-2004)
	max_blocks 1024000, rsv_groups = 125, rsv_gdb = 3
	Filesystem label=
	...
	$ mkdir /mnt/point2
	$ mount -t ext2 /dev/loop1 /mnt/point2
	$ ls /mnt/point2
	lost+found
	$ ls /mnt/point1
	file.img lost+found
	$
	通过这个简单的演示很容易体会到 Linux 文件系统（和循环设备）是多么强大。可以按照相同的方法在文件上用循环设备创建加密的文件系统。可以在需要时使用循环设备临时挂装文件，这有助于保护数据。

	文件系统体系结构
	既然已经看到了文件系统的构造方法，现在就看看 Linux 文件系统层的体系结构。本文从两个角度考察 Linux 文件系统。首先采用高层体系结构的角度。然后进行深层次讨论，介绍实现文件系统层的主要结构。

	高层体系结构
	尽管大多数文件系统代码在内核中（后面讨论的用户空间文件系统除外），但是图 1 所示的体系结构显示了用户空间和内核中与文件系统相关的主要组件之间的关系。
	图 1. Linux 文件系统组件的体系结构
![Linux文件系统的体系结构](http://note.youdao.com/yws/public/resource/7367a37c5553527c8f90c965a47db08b/xmlnote/WEBRESOURCE8603f564e22cc4a5e679c91066824855/13754)  
	图 1. Linux 文件系统组件的体系结构  

	用户空间包含一些应用程序（例如，文件系统的使用者）和 GNU C 库（glibc），它们为文件系统调用（打开、读取、写和关闭）提供用户接口。系统调用接口的作用就像是交换器，它将系统调用从用户空间发送到内核空间中的适当端点。
	VFS 是底层文件系统的主要接口。这个组件导出一组接口，然后将它们抽象到各个文件系统，各个文件系统的行为可能差异很大。有两个针对文件系统对象的缓存（inode 和 dentry）。它们缓存最近使用过的文件系统对象。
	每个文件系统实现（比如 ext2、JFS 等等）导出一组通用接口，供 VFS 使用。缓冲区缓存会缓存文件系统和相关块设备之间的请求。例如，对底层设备驱动程序的读写请求会通过缓冲区缓存来传递。这就允许在其中缓存请求，减少访问物理设备的次数，加快访问速度。以最近使用（LRU）列表的形式管理缓冲区缓存。注意，可以使用 sync 命令将缓冲区缓存中的请求发送到存储媒体（迫使所有未写的数据发送到设备驱动程序，进而发送到存储设备）。
	这就是 VFS 和文件系统组件的高层情况。现在，讨论实现这个子系统的主要结构。
	主要结构
	Linux 以一组通用对象的角度看待所有文件系统。这些对象是超级块（superblock）、inode、dentry 和文件。超级块在每个文件系统的根上，超级块描述和维护文件系统的状态。文件系统中管理的每个对象（文件或目录）在 Linux 中表示为一个 inode。inode 包含管理文件系统中的对象所需的所有元数据（包括可以在对象上执行的操作）。另一组结构称为 dentry，它们用来实现名称和 inode 之间的映射，有一个目录缓存用来保存最近使用的 dentry。dentry 还维护目录和文件之间的关系，从而支持在文件系统中移动。最后，VFS 文件表示一个打开的文件（保存打开的文件的状态，比如写偏移量等等）。
	虚拟文件系统层
	VFS 作为文件系统接口的根层。VFS 记录当前支持的文件系统以及当前挂装的文件系统。
	可以使用一组注册函数在 Linux 中动态地添加或删除文件系统。内核保存当前支持的文件系统的列表，可以通过 /proc 文件系统在用户空间中查看这个列表。这个虚拟文件还显示当前与这些文件系统相关联的设备。在 Linux 中添加新文件系统的方法是调用 register_filesystem。这个函数的参数定义一个文件系统结构（file_system_type）的引用，这个结构定义文件系统的名称、一组属性和两个超级块函数。也可以注销文件系统。
	在注册新的文件系统时，会把这个文件系统和它的相关信息添加到 file_systems 列表中（见图 2 和 linux/include/linux/mount.h）。这个列表定义可以支持的文件系统。在命令行上输入 cat /proc/filesystems，就可以查看这个列表。  
	图 2. 向内核注册的文件系统  
![向内核注册的文件系统](http://note.youdao.com/yws/public/resource/7367a37c5553527c8f90c965a47db08b/xmlnote/WEBRESOURCEafce4b3c9a62933e11e8fda552aa347a/13756)  
	图 2. 向内核注册的文件系统  

	VFS 中维护的另一个结构是挂装的文件系统（见图 3）。这个结构提供当前挂装的文件系统（见 linux/include/linux/fs.h）。它链接下面讨论的超级块结构。  
	图 3. 挂装的文件系统列表  
![挂装的文件系统列表](http://note.youdao.com/yws/public/resource/7367a37c5553527c8f90c965a47db08b/xmlnote/WEBRESOURCE5f445362698e65828e32ef28b236297a/13758)  
	图 3. 挂装的文件系统列表  

	超级块
	超级块结构表示一个文件系统。它包含管理文件系统所需的信息，包括文件系统名称（比如 ext2）、文件系统的大小和状态、块设备的引用和元数据信息（比如空闲列表等等）。超级块通常存储在存储媒体上，但是如果超级块不存在，也可以实时创建它。可以在 ./linux/include/linux/fs.h 中找到超级块结构（见图 4）。  
	图 4. 超级块结构和 inode 操作  
![超级块结构和inode操作](http://note.youdao.com/yws/public/resource/7367a37c5553527c8f90c965a47db08b/xmlnote/WEBRESOURCEfa4ec33308a23effccc84a5d62ec2a1f/13760)  
	图 4. 超级块结构和 inode 操作  

	超级块中的一个重要元素是超级块操作的定义。这个结构定义一组用来管理这个文件系统中的 inode 的函数。例如，可以用 alloc_inode 分配 inode，用 destroy_inode 删除 inode。可以用 read_inode 和 write_inode 读写 inode，用 sync_fs 执行文件系统同步。可以在 ./linux/include/linux/fs.h 中找到 super_operations 结构。每个文件系统提供自己的 inode 方法，这些方法实现操作并向 VFS 层提供通用的抽象。
	inode 和 dentry
	inode 表示文件系统中的一个对象，它具有惟一标识符。各个文件系统提供将文件名映射为惟一 inode 标识符和 inode 引用的方法。图 5 显示 inode 结构的一部分以及两个相关结构。请特别注意 inode_operations 和 file_operations。这些结构表示可以在这个 inode 上执行的操作。inode_operations 定义直接在 inode 上执行的操作，而 file_operations 定义与文件和目录相关的方法（标准系统调用）。  
	图 5. inode 结构和相关联的操作  
![inode结构和相关联的操作](http://note.youdao.com/yws/public/resource/7367a37c5553527c8f90c965a47db08b/xmlnote/WEBRESOURCEa02436204c237cbcfef0b0c62a66f3c1/13762)   
	图 5. inode 结构和相关联的操作  

	inode 和目录缓存分别保存最近使用的 inode 和 dentry。注意，对于 inode 缓存中的每个 inode，在目录缓存中都有一个对应的 dentry。可以在 ./linux/include/linux/fs.h 中找到 inode 和 dentry 结构。
	缓冲区缓存
	除了各个文件系统实现（可以在 ./linux/fs 中找到）之外，文件系统层的底部是缓冲区缓存。这个组件跟踪来自文件系统实现和物理设备（通过设备驱动程序）的读写请求。为了提高效率，Linux 对请求进行缓存，避免将所有请求发送到物理设备。缓存中缓存最近使用的缓冲区（页面），这些缓冲区可以快速提供给各个文件系统。
	有趣的文件系统
	本文没有讨论 Linux 中可用的具体文件系统，但是值得在这里稍微提一下。Linux 支持许多种文件系统，包括 MINIX、MS-DOS 和 ext2 等老式文件系统。Linux 还支持 ext3、JFS 和 ReiserFS 等新的日志型文件系统。另外，Linux 支持加密文件系统（比如 CFS）和虚拟文件系统（比如 /proc）。
	最后一种值得注意的文件系统是 Filesystem in Userspace（FUSE）。这种文件系统可以将文件系统请求通过 VFS 发送回用户空间。所以，如果您有兴趣创建自己的文件系统，那么通过使用 FUSE 进行开发是一种不错的方法。
	结束语
	尽管文件系统的实现并不复杂，但它是可伸缩和可扩展的体系结构的好例子。文件系统体系结构已经发展了许多年，并成功地支持了许多不同类型的文件系统和许多目标存储设备类型。由于使用了基于插件的体系结构和多层的函数间接性，Linux 文件系统在近期的发展很值得关注。

### UBUNTU中/dev/loop0是什么意思

	回环文件，非物理设备中创建的文件系统，如iso,img... 
	mount -o loop  abc.iso /media
	等于
	losetup /dev/loop0 /abc.iso
	mount /dev/loop0 /media

### grep -q用于if逻辑判断

	grep -q用于if逻辑判断
	 
	突然发现grep -q 用于if 逻辑判断很好用。
	 
	-q 参数，本意是 Quiet; do not write anything to standard output.  Exit immediately with zero status if any match is found, even if an error was detected.   中文意思为，安静模式，不打印任何标准输出。如果有匹配的内容则立即返回状态值0。
	 
	小应用
	 
	# cat a.txt
	nihao 
	nihaooo
	hello

    #  if  grep -q hello a.txt ; then echo yes;else echo no; fi 
	yes
    # if grep -q word a.txt; then echo yes; else echo no; fi
	no

###	Linux中打开ISO文件的两种方法

	方法一、Linux下用mount挂载命令

	在网上下载的软件盘是iso格式的，不刻成光盘就可以读取里面的文件。不用解压。

	在终端用mount -o loop /mnt/*/1.iso /mnt/cdrom 命令，(其中*是你工具盘放置的路径)。

	输入命令后，打开我的电脑——〉打开CD-ROM就能看到里面的文件了。运行install或者 autorun。

	当提示charudi二张光盘时，键入命令umount /mnt/cdrom 。

	然后再键入mount -o loop /mnt/*/2.iso/mnt/cdrom(把第一条命令的文件名的1改成2，就是第二张光盘的名字了)。这样再回车。等待就可以了。

	取消挂载用umount /mnt/cdrom


	方法二、在Linux下使用虚拟光驱

	其实根本不需要什么虚拟光驱软件，用mount命令就可以完成。

	1. 把光盘制作成iso文件

	cp /dev/cdrom XXXXX.iso

	XXXXX.iso为你所命名的镜像文件。执行此命令之后就可以将整个光盘制作成iso文件。XXXXX.iso前你可以加上路径哦。

	2.将硬盘上的iso文件加载到光盘(或者说虚拟光驱)。

	mount -t iso9660 -o loop /*/XXXXX.iso /mnt/iso

	3.如果是安装系统盘所提供的文件，如添加删除程序，系统可能会提示你插入光盘，但我们没有光盘，只有镜像，怎么办？

	对于RedHat，先 mount iso,然后执行

	redhat-install-packages --isodir=/mnt/iso

	4.一般情况虚拟光驱

	rm -rf /dev/cdrom #删除光驱

	ln /dev/loop7 /dev/cdrom

	losetup /dev/loop7 /*/XXXXX.iso

	mount /mnt/cdrom

	然后你再看看iso文件，是不是变成了虚拟光驱？

	5.取消这个光驱：

	losetup -d /dev/loop7

	换盘的话：

	只需转移iso关联到/dev/loop

	losetup /dev/loop7 /*/XXXXX.iso

	注：/*为路径，可能要在/mnt/下先建个名为cdrom的文件夹

### linux shell 逻辑运算符、逻辑表达式详解

	shell的逻辑运算符 涉及有以下几种类型，因此只要适当选择，可以解决我们很多复杂的判断，达到事半功倍效果。

	一、逻辑运算符

	逻辑卷标	表示意思
	1.	关于档案与目录的侦测逻辑卷标！
	-f	常用！侦测『档案』是否存在 eg: if [ -f filename ]
	-d	常用！侦测『目录』是否存在
	-b	侦测是否为一个『 block 档案』
	-c	侦测是否为一个『 character 档案』
	-S	侦测是否为一个『 socket 标签档案』
	-L	侦测是否为一个『 symbolic link 的档案』
	-e	侦测『某个东西』是否存在！
	2.	关于程序的逻辑卷标！
	-G	侦测是否由 GID 所执行的程序所拥有
	-O	侦测是否由 UID 所执行的程序所拥有
	-p	侦测是否为程序间传送信息的 name pipe 或是 FIFO （老实说，这个不太懂！）
	3.	关于档案的属性侦测！
	-r	侦测是否为可读的属性
	-w	侦测是否为可以写入的属性
	-x	侦测是否为可执行的属性
	-s	侦测是否为『非空白档案』
	-u	侦测是否具有『 SUID 』的属性
	-g	侦测是否具有『 SGID 』的属性
	-k	侦测是否具有『 sticky bit 』的属性
	4.	两个档案之间的判断与比较 ；例如[ test file1 -nt file2 ]
	-nt	第一个档案比第二个档案新
	-ot	第一个档案比第二个档案旧
	-ef	第一个档案与第二个档案为同一个档案（ link 之类的档案）
	5.	逻辑的『和(and)』『或(or)』
	&&	逻辑的 AND 的意思
	||	逻辑的 OR 的意思
	  

	运算符号	代表意义
	=	等于 应用于：整型或字符串比较 如果在[] 中，只能是字符串
	!=	不等于 应用于：整型或字符串比较 如果在[] 中，只能是字符串
	<	小于 应用于：整型比较 在[] 中，不能使用 表示字符串
	>	大于 应用于：整型比较 在[] 中，不能使用 表示字符串
	-eq	等于 应用于：整型比较
	-ne	不等于 应用于：整型比较
	-lt	小于 应用于：整型比较
	-gt	大于 应用于：整型比较
	-le	小于或等于 应用于：整型比较
	-ge	大于或等于 应用于：整型比较
	-a	双方都成立（and） 逻辑表达式 –a 逻辑表达式
	-o	单方成立（or） 逻辑表达式 –o 逻辑表达式
	-z	空字符串
	-n	非空字符串
	 

	二、逻辑表达式

	test 命令
	使用方法：test EXPRESSION

	如：

	[root@localhost ~]# test 1 = 1 && echo 'ok'
	ok

	[root@localhost ~]# test -d /etc/ && echo 'ok' 
	ok

	[root@localhost ~]# test 1 -eq 1 && echo 'ok'
	ok

	 

	[root@localhost ~]# if test 1 = 1 ; then echo 'ok'; fi
	ok

	 

	注意：所有字符 与逻辑运算符直接用“空格”分开，不能连到一起。

	 

	精简表达式
	[] 表达式
	[root@localhost ~]# [ 1 -eq 1 ] && echo 'ok'           
	ok

	[root@localhost ~]# [ 2 < 1 ] && echo 'ok'                  
	-bash: 2: No such file or directory


	[root@localhost ~]# [ 2 \< 1 ] && echo 'ok'

	[root@localhost ~]# [ 2 -gt 1 -a 3 -lt 4 ] && echo 'ok'

	ok    

	[root@localhost ~]# [ 2 -gt 1 && 3 -lt 4 ] && echo 'ok'   
	-bash: [: missing `]'

	注意：在[] 表达式中，常见的>,<需要加转义字符，表示字符串大小比较，以acill码 位置作为比较。 不直接支持<>运算符，还有逻辑运算符|| && 它需要用-a[and] –o[or]表示


	ok
	[root@localhost ~]$ [[ 2 < 3 ]] && echo 'ok' 
	ok

	[root@localhost ~]$ [[ 2 < 3 && 4 > 5 ]] && echo 'ok' 
	ok
	注意：[[]] 运算符只是[]运算符的扩充。能够支持<,>符号运算不需要转义符，它还是以字符串比较大小。里面支持逻辑运算符：|| &&
	 

	三、性能比较

	bash的条件表达式中有三个几乎等效的符号和命令：test，[]和[[]]。通常，大家习惯用if [];then这样的形式。而[[]]的出现，根据ABS所说，是为了兼容><之类的运算符。以下是比较它们性能，发现[[]]是最快的。

	$ time (for m in {1..100000}; do test -d .;done;)
	real    0m0.658s
	user    0m0.558s
	sys     0m0.100s


	$ time (for m in {1..100000}; do [ -d . ];done;)
	real    0m0.609s
	user    0m0.524s
	sys     0m0.085s


	$ time (for m in {1..100000}; do [[ -d . ]];done;)
	real    0m0.311s
	user    0m0.275s
	sys     0m0.036s

### shell tr

	tr,用来从标准输入中通过替换/删除进行字符转换

	主要用于删除文件中的控制字符或进行字符转换

	使用时，提供两个字符串，串1：用于查询，串2：用于处理各种转换；串1的字符被映射到串2上，然后转换开始

	主要用途：1.大小写转换
			2.去除控制字符
			3.删除字符

	命令格式：
	tr –c –d –s [“str_from”] [“str_to”] file

	-c，用字符串1中字符集的补集替换此字符集，要求字符集为ASCII
	-d，删除字符串1中所有输入字符串
	-s，删除所有重复出现字符序列，只保留一个，即重复字符串压缩为一个

	字符范围——tr，可以指定字符串列表或范围作为形成字符串的模式，似正则，但不是正则。

	[a-z] [A-Z] [0-9]    /octal一个三位八进制数，对应有效ＡＳＣＩＩ字符

	[s*n]字符s出现n次

	tr 中特定字符的不同表达方式
	a|b|c
	-|-|-
	/a|	Ctrl-g铃声|	/007
	/b|	Ctrl-h退格|	/010
	/f|	Ctrl-l走纸模式|	/014
	/n|	Ctrl-J新行|	/012
	/r|	Ctrl-M回车|	/015 
	/t| Ctrl-I tab键| /011 
	/v| Ctrl-x| /030 

	1.       去除所有重复字符【只保留一个】

	$tr –s “[a-z]” < oops.txt

	2.       去除空行

	$tr –s “[/012]” <oops.txt

	$tr –s “[/n]” <oops.txt

	3.       小写转大写

	$echo “AbcdefG” | tr “[a-z]” “[A-Z]”

	$echo “AbcdefG” | tr “[:lower:]” “[:upper:]”

	4.       删除指定字符串

	$tr –cs “[a-z][A-Z]” “[/012*]” < data.txt

	将非字母字符转为新行  -s压缩重复的字符

	5.       转换控制字符

	$tr –s “[/136]” “[/011*]” < start.txt

	6.       快速转换

	$tr –s “[/r]” “[/n]” < input.txt

	7.       匹配多于一个字符

	$tr “[0*4]” “*”< input.txt


### Shell下常用字符 

	#--注释行
	;--命令分隔符，可以用来在一行中执行多个命令 echo hello; echo  good
	;; 终止"case"选项.
	   1 case "$variable" in
	   2 abc) echo "\$variable = abc" ;;
	   3 xyz) echo "\$variable = xyz" ;;
	   4 esac
	source . http://www.cnblogs.com/softwaretesting/archive/2012/02/13/2349550.html

	: 空命令,等价于"NOP"(no op,一个什么也不干的命令).也可以被认为与shell 的内建命令
	(true)作用相同.":"命令是一
	个 bash 的内建命令,它的返回值为0,就是shell 返回的true.
	如:
	1 :
	2 echo $? # 0

	${} 参数替换,见9.3 节.
	$*,$@ 位置参数
	$? 退出状态变量.$?保存一个命令/一个函数或者脚本本身的退出状态.
	$$ 进程ID 变量.这个$$变量保存运行脚本进程ID

### 非常详细的/etc/passwd解释

	Linux配置管理UnixBash工作 
	root:x:0:0:root:/root:/bin/bash 

	　　bin:x:1:1:bin:/bin:/sbin/nologin 

	　　daemon:x:2:2:daemon:/sbin:/sbin/nologin 

	　　desktop:x:80:80:desktop:/var/lib/menu/kde:/sbin/nologin 

	　　mengqc:x:500:500:mengqc:/home/mengqc:/bin/bash 

	　　在该文件中，每一行用户记录的各个数据段用“：”分隔，分别定义了用户的各方面属性。各个字段的顺序和含义如下： 

	　　注册名：口令：用户标识号：组标识号：用户名：用户主目录：命令解释程序 

	　　(1)注册名(login_name)：用于区分不同的用户。在同一系统中注册名是惟一的。在很多系统上，该字段被限制在8个字符(字母或数字)的长度之内；并且要注意，通常在Linux系统中对字母大小写是敏感的。这与MSDOS/Windows是不一样的。 

	　　(2)口令(passwd)：系统用口令来验证用户的合法性。超级用户root或某些高级用户可以使用系统命令passwd来更改系统中所有用户的口令，普通用户也可以在登录系统后使用passwd命令来更改自己的口令。 

	　　现在的Unix/Linux系统中，口令不再直接保存在passwd文件中，通常将passwd文件中的口令字段使用一个“x”来代替，将/etc /shadow作为真正的口令文件，用于保存包括个人口令在内的数据。当然shadow文件是不能被普通用户读取的，只有超级用户才有权读取。 

	　　此外，需要注意的是，如果passwd字段中的第一个字符是“*”的话，那么，就表示该账号被查封了，系统不允许持有该账号的用户登录。 

	　　(3)用户标识号(UID)：UID是一个数值，是Linux系统中惟一的用户标识，用于区别不同的用户。在系统内部管理进程和文件保护时使用 UID字段。在Linux系统中，注册名和UID都可以用于标识用户，只不过对于系统来说UID更为重要；而对于用户来说注册名使用起来更方便。在某些特 定目的下，系统中可以存在多个拥有不同注册名、但UID相同的用户，事实上，这些使用不同注册名的用户实际上是同一个用户。 

	　　(4)组标识号(GID)：这是当前用户的缺省工作组标识。具有相似属性的多个用户可以被分配到同一个组内，每个组都有自己的组名，且以自己的组标 识号相区分。像UID一样，用户的组标识号也存放在passwd文件中。在现代的Unix/Linux中，每个用户可以同时属于多个组。除了在 passwd文件中指定其归属的基本组之外，还在/etc/group文件中指明一个组所包含用户。 

	　　(5)用户名(user_name)：包含有关用户的一些信息，如用户的真实姓名、办公室地址、联系电话等。在Linux系统中，mail和finger等程序利用这些信息来标识系统的用户。 

	　　(6)用户主目录(home_directory)：该字段定义了个人用户的主目录，当用户登录后，他的Shell将把该目录作为用户的工作目录。 在Unix/Linux系统中，超级用户root的工作目录为/root；而其它个人用户在/home目录下均有自己独立的工作环境，系统在该目录下为每 个用户配置了自己的主目录。个人用户的文件都放置在各自的 

	　　主目录下。 

	　　(7)命令解释程序(Shell)：Shell是当用户登录系统时运行的程序名称，通常是一个Shell程序的全路径名， 

	　　如/bin/bash。 

	　　需要注意的是，系统管理员通常没有必要直接修改passwd文件，Linux提供一些账号管理工具帮助系统管理员来创建和维护用户账号。 

	　　Linux口令管理之/etc/passwd文件 

	　　/etc/passwd文件是Linux/UNIX安全的关键文件之一.该文件用于用户登录时校验 用户的口令,当然应当仅对root可写.文件中每行的一般格式为: 

	　　LOGNAME:PASSWORD:UID:GID:USERINFO:HOME:SHELL 

	　　每行的头两项是登录名和加密后的口令,后面的两个数是UID和GID,接着的 一项是系统管理员想写入的有关该用户的任何信息,最后两项是两个路径名: 一个是分配给用户的HOME目录,第二个是用户登录后将执行的shell(若为空格则 缺省为/bin/sh). 

	　　(1)口令时效 

	　　/etc/passwd文件的格式使系统管理员能要求用户定期地改变他们的口令. 在口令文件中可以看到,有些加密后的口令有逗号,逗号后有几个字符和一个 冒号.如: 

	　　steve:xyDfccTrt180x,M.y8:0:0:admin:/:/bin/sh 

	　　restrict:pomJk109Jky41,.1:0:0:admin:/:/bin/sh 

	　　pat:xmotTVoyumjls:0:0:admin:/:/bin/sh 

	　　可以看到,steve的口令逗号后有4个字符,restrict有2个,pat没有逗号. 

	　　逗号后第一个字符是口令有效期的最大周数,第二个字符决定了用户再次 修改口信之前,原口令应使用的最小周数(这就防止了用户改了新口令后立刻 又改回成老口令).其余字符表明口令最新修改时间. 

	　　要能读懂口令中逗号后的信息,必须首先知道如何用passwd_esc计数,计 数的方法是: 

	　　.=0 /=1 0-9=2-11 A-Z=12-37 a-z=38-63 

	　　系统管理员必须将前两个字符放进/etc/passwd文件,以要求用户定期的 修改口令,另外两个字符当用户修改口令时,由passwd命令填入. 

	　　注意:若想让用户修改口令,可在最后一次口令被修改时,放两个".",则下 一次用户登录时将被要求修改自己的口令. 

	　　有两种特殊情况: 

	　　. 最大周数(第一个字符)小于最小周数(第二个字符),则不允许用户修改 口令,仅超级用户可以修改用户的口令. 

	　　. 第一个字符和第二个字符都是".",这时用户下次登录时被要求修改口 令,修改口令后,passwd命令将"."删除,此后再不会要求用户修改口令. 

	　　(2)UID和GID 

	　　/etc/passwd中UID信息很重要,系统使用UID而不是登录名区别用户.一般 来说,用户的UID应当是独一无二的,其他用户不应当有相同的UID数值.根据惯 例,从0到99的UID保留用作系统用户的UID(root,bin,uucp等). 

	　　如果在/etc/passwd文件中有两个不同的入口项有相同的UID,则这两个用 户对相互的文件具有相同的存取权限.

	　　/etc /group文件含有关于小组的信息,/etc/passwd中的每个GID在本文件中 应当有相应的入口项,入口项中列出了小组名和小组中的用户.这样可方便地了 解每个小组的用户,否则必须根据GID在/etc/passwd文件中从头至尾地寻找同组 用户. 

	　　/etc/group文件对小组的许可权限的控制并不是必要的,因为系统用UID,GID (取自/etc/passwd)决定文件存取权限,即使/etc/group文件不存在于系统中,具 有相同的GID用户也可以小组的存取许可权限共享文件. 

	　　小组就像登录用户一样可以有口令.如果/etc/group文件入口项的第二个域 为非空,则将被认为是加密口令,newgrp命令将要求用户给出口令,然后将口令加 密,再与该域的加密口令比较. 

	　　给 小组建立口令一般不是个好作法.第一,如果小组内共享文件,若有某人猜 着小组口令,则该组的所有用户的文件就可能泄漏;其次,管理小组口令很费事, 因为对于小组没有类似的passwd命令.可用/usr/lib/makekey生成一个口令写入 /etc/group. 

	　　以下情况必须建立新组: 

	　　(1)可能要增加新用户,该用户不属于任何一个现有的小组. 

	　　(2)有的用户可能时常需要独自为一个小组. 

	　　(3)有的用户可能有一个SGID程序,需要独自为一个小组. 

	　　(4)有时可能要安装运行SGID的软件系统,该软件系统需要建立一个新组. 

	　　要 增加一个新组,必须编辑该文件,为新组加一个入口项. 由于用户登录时,系统从/etc/passwd文件中取GID,而不是从/etc/group中 取GID,所以group文件和口令文件应当具有一致性.对于一个用户的小组,UID和 GID应当是相同的.多用户小组的GID应当不同于任何用户的UID,一般为5位数,这 样在查看/etc/passwd文件时,就可根据5位数据的GID识别多用户小组,这将减少 增加新组,新用户时可能产生的混淆. 

### 关于/dev/null及用途

	把/dev/null看作"黑洞". 它非常等价于一个只写文件. 所有写入它的内容都会永远丢失. 而尝试从它那儿读取内容则什么也读不到. 然而, /dev/null对命令行和脚本都非常的有用.

	禁止标准输出.

	1 cat $filename >/dev/null
	   2 # 文件内容丢失，而不会输出到标准输出.
	禁止标准错误

	1 rm $badname 2>/dev/null
	   2 #           这样错误信息[标准错误]就被丢到太平洋去了.
	禁止标准输出和标准错误的输出.

	1 cat $filename 2>/dev/null >/dev/null
	   2 # 如果"$filename"不存在，将不会有任何错误信息提示.
	   3 # 如果"$filename"存在, 文件的内容不会打印到标准输出.
	   4 # 因此Therefore, 上面的代码根本不会输出任何信息.
	   5 # 当只想测试命令的退出码而不想有任何输出时非常有用。
	   6 #-----------测试命令的退出 begin ----------------------#
	   7 # ls dddd 2>/dev/null 8 
	   8 # echo $?    //输出命令退出代码：0为命令正常执行，1-255为有出错。  
	   9 #-----------测试命令的退出 end-----------#  
	   10 # cat $filename &>/dev/null 
	   11 #   也可以, 由 Baris Cicek 指出.
	清除日志文件内容

	1 cat /dev/null > /var/log/messages
	   2 #  : > /var/log/messages   有同样的效果, 但不会产生新的进程.（因为:是内建的）
	   3 
	   4 cat /dev/null > /var/log/wtmp
	例子 28-1. 隐藏cookie而不再使用

	1 if [ -f ~/.netscape/cookies ]  # 如果存在则删除.
	   2 then
	   3   rm -f ~/.netscape/cookies
	   4 fi
	   5 
	   6 ln -s /dev/null ~/.netscape/cookies
	   7 # 现在所有的cookies都会丢入黑洞而不会保存在磁盘上了.


### shell中$*与$@的区别

	shell中$*与$@的区别

	$*
	所有的位置参数,被作为一个单词.
	注意:"$*"必须被""引用.
	$@
	与$*同义,但是每个参数都是一个独立的""引用字串,这就意味着参数被完整地传递,
	并没有被解释和扩展.这也意味着,每个参数列表中的每个参数都被当成一个独立的
	单词.
	注意:"$@"必须被引用.
	$@ $* 只在被双引号包起来的时候才会有差异
	双引号括起来的情况：
	$*将所有的参数认为是一个字段
	$@以IFS（默认为空格）来划分字段，如果空格在“”里面，不划分。采用LS的脚本运行./test 1 "2 3" 4   来发现差异

	没有括起来的情况是$@和$*一样的，见到IFS就划分字段。还是采用LS的脚本运行./test 1 "2 3" 4   来发现差异
	一个小例子 ，仅供参考

	```
	:#!/bin/bash
	echo

	index=1

	echo "Listing args with\"\$*\":"
	for arg in "$*"

	do
	   echo "Arg #$index=$arg"
	   let "index+=1"

	done

	echo "所有的参数被认为是一个单词"

	echo

	index=1

	echo "Listing args with \"\$@\":"
	for arg in "$@"
	do
	echo "Arg #$index=$arg"
	let "index+=1"
	done

	echo "所有的参数被认为是各个独立的单词"

	echo

	index=1

	echo "Listing args with \$* (未被引用):"
	for arg in $*
	do
	echo "Arg #$index=$arg"
	let "index+=1"
	done
	echo "所有的参数被认为是各个独立的单词"

	exit 0
	```
	运行后输出为

	[Copy to clipboard] [ - ]CODE:[root@localhost ABS]# ./test 1 2 3 4

	Listing args with"$*":
	Arg #1=1 2 3 4
	所有的参数被认为是一个单词

	Listing args with "$@":
	Arg #1=1
	Arg #2=2
	Arg #3=3
	Arg #4=4
	所有的参数被认为是各个独立的单词

	Listing args with $* (未被引用):
	Arg #1=1
	Arg #2=2
	Arg #3=3
	Arg #4=4
	所有的参数被认为是各个独立的单词

### tar

	tar
	-c: 建立压缩档案
	-x：解压
	-t：查看内容
	-r：向压缩归档文件末尾追加文件
	-u：更新原压缩包中的文件
	这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。
	-z：有gzip属性的
	-j：有bz2属性的
	-Z：有compress属性的
	-v：显示所有过程
	-O：将文件解开到标准输出
	下面的参数-f是必须的
	-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。
	# tar -cf all.tar *.jpg 
	这条命令是将所有.jpg的文件打成一个名为all.tar的包。-c是表示产生新的包，-f指定包的文件名。
	# tar -rf all.tar *.gif 
	这条命令是将所有.gif的文件增加到all.tar的包里面去。-r是表示增加文件的意思。
	# tar -uf all.tar logo.gif 
	这条命令是更新原来tar包all.tar中logo.gif文件，-u是表示更新文件的意思。
	# tar -tf all.tar 
	这条命令是列出all.tar包中所有文件，-t是列出文件的意思
	# tar -xf all.tar 
	这条命令是解出all.tar包中所有文件，-x是解开的意思
	 

	压缩

	tar –cvf jpg.tar *.jpg //将目录里所有jpg文件打包成tar.jpg

	tar –czf jpg.tar.gz *.jpg   //将目录里所有jpg文件打包成jpg.tar后，并且将其用gzip压缩，生成一个gzip压缩过的包，命名为jpg.tar.gz

	tar –cjf jpg.tar.bz2 *.jpg //将目录里所有jpg文件打包成jpg.tar后，并且将其用bzip2压缩，生成一个bzip2压缩过的包，命名为jpg.tar.bz2

	tar –cZf jpg.tar.Z *.jpg   //将目录里所有jpg文件打包成jpg.tar后，并且将其用compress压缩，生成一个umcompress压缩过的包，命名为jpg.tar.Z

	rar a jpg.rar *.jpg //rar格式的压缩，需要先下载rar for linux

	zip jpg.zip *.jpg //zip格式的压缩，需要先下载zip for linux
	 
	解压

	tar –xvf file.tar //解压 tar包

	tar -xzvf file.tar.gz //解压tar.gz

	tar -xjvf file.tar.bz2   //解压 tar.bz2

	tar –xZvf file.tar.Z   //解压tar.Z
	unrar e file.rar //解压rar
	unzip file.zip //解压zip

	总结

	1、*.tar 用 tar –xvf 解压
	2、*.gz 用 gzip -d或者gunzip 解压
	3、*.tar.gz和*.tgz 用 tar –xzf 解压
	4、*.bz2 用 bzip2 -d或者用bunzip2 解压
	5、*.tar.bz2用tar –xjf 解压
	6、*.Z 用 uncompress 解压
	7、*.tar.Z 用tar –xZf 解压
	8、*.rar 用 unrar e解压
	9、*.zip 用 unzip 解压


### Linux DISPLAY作用

	在Linux/Unix类操作系统上, DISPLAY用来设置将图形显示到何处. 直接登陆图形界面或者登陆命令行界面后使用startx启动图形, DISPLAY环境变量将自动设置为:0:0, 此时可以打开终端, 输出图形程序的名称(比如xclock)来启动程序, 图形将显示在本地窗口上, 在终端上输入printenv查看当前环境变量, 输出结果中有如下内容:

	DISPLAY=:0.0

	使用xdpyinfo可以查看到当前显示的更详细的信息.

	DISPLAY 环境变量格式如下hostname: displaynumber.screennumber,我们需要知道，在某些机器上，可能有多个显示设备共享使用同一套输入设备，例如在一台PC上连接两台CRT显示器，但是它们只共享使用一个键盘和一个鼠标。这一组显示设备就拥有一个共同的displaynumber，而这组显示设备中的每个单独的设备则拥有自己单独的 screennumber。displaynumber和screennumber都是从零开始的数字。这样，对于我们普通用户来说， displaynumber、screennumber就都是0。 hostname指Xserver所在的主机主机名或者ip地址, 图形将显示在这一机器上, 可以是启动了图形界面的Linux/Unix机器, 也可以是安装了Exceed, X-Deep/32等Windows平台运行的Xserver的Windows机器. 如果Host为空, 则表示Xserver运行于本机, 并且图形程序(Xclient)使用unix socket方式连接到Xserver, 而不是TCP方式. 使用TCP方式连接时, displaynumber为连接的端口减去6000的值, 如果displaynumber为0, 则表示连接到6000端口; 使用unix socket方式连接时则表示连接的unix socket的路径, 如果displaynumber为0, 则表示连接到/tmp/.X11-unix/X0 . screennumber则几乎总是0.

	如果使用su username或者su - username切换到别的用户, 并且使用命令

	export DISPLAY=:0.0

	设置DISPLAY环境变量, 运行图形程序(如xclock)时会收到如下错误:

	Xlib: connection to ":0.0" refused by server
	Xlib: No protocol specified

	Error: Can't open display: :0.0

	这是因为Xserver默认情况下不允许别的用户的图形程序的图形显示在当前屏幕上. 如果需要别的用户的图形显示在当前屏幕上, 则应以当前登陆的用户, 也就是切换身份前的用户执行如下命令

	xhost +

	这个命令将允许别的用户启动的图形程序将图形显示在当前屏幕上.

	在2台Linux机器之间, 如果设置服务器端配置文件/etc/ssh/sshd_config中包含

	X11Forwarding no

	客户端配置文件/etc/ssh/ssh_config包含

	ForwardX11 yes

	则从客户端ssh到服务器端后会自动设置DISPLAY环境变量, 允许在服务器端执行的图形程序将图形显示在客户端上. 在服务器上查看环境变量显示如下(这个结果不同的时候并不相同)

	DISPLAY=localhost:10.0

	在客户机上用netstat -lnp可以看到有程序监听了6010端口

	tcp 0 0 127.0.0.1:6010 0.0.0.0:* LISTEN 4827/1

	如果希望允许远程机器上的图形程序将图形显示在本地机器的Xserver上, 除了要设置远端机器的DISPLAY环境变量以外, 还需要设置本地机器的Xserver监听相应的TCP端口. 而现在的Linux系统出于安全的考虑, 默认情况下不再监听TCP端口. 可通过修改/etc/X11/xinit/xserverrc文件, 将

	exec /usr/bin/X11/X -dpi 100 -nolisten tcp

	修改为

	exec /usr/bin/X11/X -dpi 100

	允许在直接使用startx启动图形时启动对TCP端口的监听.

	修改/etc/kde3/kdm/kdmrc, 将

	ServerArgsLocal=-nolisten tcp

	修改为

	ServerArgsLocal=

	允许kdm作为显示管理器时, 启动会话时监听相应的TCP端口.

	修改/etc/gdm/gdm.conf, 在[Security]一节增加

	DisallowTCP=false

	或者在登陆窗口选择"Options" -> "Configure Login Manager..."的Security页面, 取消"Deny TCP connections to Xserver", 允许gdm作为显示管理器时, 启动会话时监听相应的TCP端口.

	文章出处：http://www.diybl.com/course/6_system/linux/Linuxjs/2008825/137565.html

	附：

	有如下几种方法：
	1.rlogin、rsh等r系列命令。因为有较大的安全隐患，所以现在基本上废弃不用。 所以这里也不作详细介绍

	2.telnet。telnet在linux和windows下均可用，只要打开相应的服务即可。telnet 的所有数据在网络上都是明文传输，所以也有安全隐患，在实际的生产系统中也基本上废弃不用，而转用更安全的ssh。但是在某些场合，如内部局域网络，telnet 还是有用武之地的。telnet使用方法：例如想连接到主机foobar上
	telnet foobar
	也可以直接使用ip：
	telnet ip-of-foobar
	之后输入用户名和口令之后就连接到了foobar上

	3.ssh。ssh和telnet类似，但是数据在网络上是加密后再传输的。
	http: //www.linuxaid.com.cn/engineer/brimmer/html/ssh.htm
	这个链接的文章讲得很全面，比我写的好:)

	4.远程X。这利用了X Window窗口系统的网络透明性，即，图形程序的运行和显示 可以在不同的主机上。这里首先要澄清两个概念，即X Server和X Client。假设 xclock程序在主机A上运行，但是显示在主机B上，那么谁是X Server，谁又是X Client呢？A是X Server，B是X Client？错！正确的答案是，应用程序xclock是X Client，主机B是X Server。为什么呢？Server是提供“资源”的一方，而Client是使用“资源”的一方。对于窗口系统来说，“资源”就是显示资源和输入设备，如显示器，键盘，鼠标等。主机B提供了这些资源，而应用程序xclock请求使用这些资 源，所以说xclock是X Client，主机B是X Server（更确切的说，应该是主机B上的 某个应用程序，例如/usr/X11R6/bin/X，他控制着B上这些硬件资源的分配和管理）。搞清楚了X Client和X Server的概念后，再来看一个重要的环境变量： DISPLAY，它指定了一个显示设备，所有的图形程序都将把自己显示到这个设备上。DISPLAY的格式为：hostname:displaynumber.screennumber。hostname是一个主机名，或者是它的ip地址。为了理解后面的displaynumber和screennumber，我们需要知道，在某些机器上，可能有多个显示设备共享使用同一套输入设备，例如在一台PC上连接两台CRT显示器，但是它们只共享使用一个键盘和一个鼠标。这一组显示设备就拥有一个共同的displaynumber，而这组显示设备中的每个单独的设备则拥有自己单独的screennumber。displaynumber和screennumber都是从零开始的数字。这样，对于我们普通用户来说，displaynumber、screennumber就都是0。 hostname可以省略（但它后面的冒号不能省略），如果省略的话，则使用本机作为默认的hostname，即:m.n等价于localhost:m.n。现在我们已经掌握了所有使用远程X的必需知识，如果我们想在远程主机A上运行gimp程序，但是把它的显示输出到 本地主机B的屏幕上好供我操作的话，需要依次执行以下步骤：
	1).在B上启动一个X Server程序
	2).在A上设定适当的DISPLAY变量，例如：export DISPLAY=B:0.0
	3).在A上启动gimp
	PS：
	1).如果无法使用A的物理控制台的话，例如A、B的物理距离很遥远，可以使用 telnet、ssh等方法远程登录A来执行第2、3两步，没有任何区别。
	2).注意，因为gimp是在B上显示的，或者说它使用的是B上的X Server，所以A上完 全不需要运行着一个X Server，甚至根本不安装也没有任何关系。
	3).注意，并没有要求B一定使用Linux或者UNIX操作系统，只要在他上面运行一个X Server即可。Linux下使用的X Server一般为XFree86，是一个免费的开源X Server。微软的windows下也有可用的X Server，例如X-Win32,Hummingbird Exceed等，但它们多为商业软件。

	你可能注意到了一个问题，按照前面所述，似乎可以把一个X图形程序显示到网络 中任何一个X Server上，这样必将造成混乱。所以，X Window系统提供了权限控制 命令xhost，可以控制哪些机器能使用我这个X Server。xhost的使用很简单，如果允许主机foo使用我这个X Server，可以使用"xhost +foo"；如果不允许主机foo使 用我这个X Server，可以使用"xhost -foo"；如果允许任何主机使用我这个X Server，简单的"xhost +"即可；反之，"xhost -"将禁止任何主机使用我这个X Server。更进一步的使用可以参考xhost(1)。

	4.vnc（Virtual Network Computing）。VNC也是C/S架构的东东，但是有一个比较特殊的地方值得注意，如果你在会话A中打开一个vnc server，那么vnc client连接上来后也会使用会话A，换句话说，vnc不会开启新的会话。这样导致的最直接后 果是，如果你是在一个X会话中开启的vnc server，那么你会发现，你在本机上的 动作（例如移动鼠标、新开窗口等等）会如实的反映到vnc client那里，而同样 的，如果在vnc client中移动鼠标，你会发现本机屏幕上的鼠标也会相应的移动。
	linux下的vnc server程序叫做vncserver,client程序叫做vncviewer。首先启动 server：
	[leona@Ash]$ vncserver

	You will require a password to access your desktops.

	Password:
	Verify:

	New 'Ash:1 (leona)' desktop is Ash:1

	Creating default startup script /home/leona/.vnc/xstartup
	Starting applications specified in /home/leona/.vnc/xstartup
	Log file is /home/leona/.vnc/Ash:2.log

	vncserver会告诉你一个标志符，也就是
	New 'Ash:1 (leona)' desktop is Ash:1
	这一行中的"Ash:1","Ash"是运行vncserver的主机的主机名，换成相应的ip地址也没有问题；"1"可以认为是启动的vncserver的序号（实际上是X Window的 displaynumber）（可以同时启动多个vncserver）。如果是第一次启动 vncserver，他会要求你设置一个口令，vnc client在连接这个server时必须提供 这个口令。这个口令在将来可以使用vncpasswd命令来修改。server成功启动后就可以使用vnc client来连接了。连接时必须提供目标server的标志符，也就是前面 所说的"Ash:1":
	[leona@Ash]$ vncviewer Ash:1
	接着提供口令后就进入了会话。
	如果想关闭一个vncserver，可以用命令vncserver -kill :id，这里的id就是 vncserver的序号。

	windows下也有vnc server和vnc client（见附件）。在安装时可以把vnc server 注册为系统服务。他的使用和在linux下类似，这里就不赘述。只是有一个地方需 要注意，windows下vnc server的标志符序号字段为0，不会为其他值。

	5.rdesktop。这是linux下的一个工具包，可以连接Microsoft Windows NT, Windows 2000 的终端服务（Terminal Services）,以及Windows XP的远程桌面服 务（Remote Desktop）。它的使用很简单，这里以连接Windows XP的远程桌面服务为例。首先在XP下启用远程桌面服务（注意，XP的HomeEdition没有远程桌面服务）：右键点击我的电脑，选择属性，查看“远程”tab页，勾选“允许用户远程连接到这台计算机”，然后一路点击“确定”即可。现在在linux机器上执行rdesktop hostname（在此之前请确定已经启动X Window窗口系统），其中hostname为 windows机器的主机名或者ip地址。现在，你就可以登录使用windows机器了。

### shell中的通配符，特殊字符和正则表达式

	1. shell支持的通配符
			shell支持一组通配符用于处理数据，但是要和正则表达式区别开来。shell的通配符实现的功能比较简单，常用于文件名匹配，远不及正则表达式强大和广泛。不过对于日常使用linux还是有非常大的帮助的。下表取自《鸟哥的linux私房菜》
	符号|	意义
	---|---
	*|	代表『 0 个到无穷多个』任意字符
	?|	代表『一定有一个』任意字符
	[ ]|	同样代表『一定有一个在括号内』的字符(非任意字符)。例如 [abcd] 代表『一定有一个字符， 可能是 a, b, c, d 这四个任何一个』
	[ - ]|	若有减号在中括号内时，代表『在编码顺序内的所有字符』。例如 [0-9] 代表 0 到 9 之间的所有数字，因为数字的语系编码是连续的！
	[^ ]|	若中括号内的第一个字符为指数符号 (^) ，那表示『反向选择』，例如 [^abc] 代表 一定有一个字符，只要是非 a, b, c 的其他字符就接受的意思。

	2. shell中的特殊字符（以bash为例）
			通配符常用于文件名匹配，而特殊字符的则协助shell完成各种具体工作。下表取自《鸟哥的linux私房菜》
	符号	内容
	#	批注符号：这个最常被使用在 script 当中，视为说明！在后的数据均不运行
	\	跳脱符号：将『特殊字符或通配符』还原成一般字符
	|	管道 (pipe)：分隔两个管线命令的界定(后两节介绍)；
	;	连续命令下达分隔符：连续性命令的界定 (注意！与管线命令并不相同)
	~	用户的家目录
	$	取用变量前导符：亦即是变量之前需要加的变量取代值
	&	工作控制 (job control)：将命令变成背景下工作
	!	逻辑运算意义上的『非』 not 的意思！
	/	目录符号：路径分隔的符号
	>, >>	数据流重导向：输出导向，分别是『取代』与『累加』
	<, <<	数据流重导向：输入导向 (这两个留待下节介绍)
	' '	单引号，不具有变量置换的功能
	" "	具有变量置换的功能！
	` `	两个『 ` 』中间为可以先运行的命令，亦可使用 $( )
	( )	在中间为子 shell 的起始与结束
	{ }	在中间为命令区块的组合！

### Linux完整教程命令学习记录

	mount -t iso9660 -o loop /home/kris/somewhat.iso /mnt/cdrom  

	umount /mnt/cdrom

	管道符号> >>区别：前者创建一个新的filenames.txt，如果已经有了同名的文件就覆盖掉以前的内容；后者用来在已经存在的文件后面追加新的内容，如果没有这个文件就创建它。  


	GRUB 是一个很棒的boot loader。它有许多功能，可以使引导过程变得非常可靠。例如，它可以直接从 FAT、minix、FFS、ext2
	或 ReiserFS 分区读取 Linux 内核。这就意味着无论怎样它总能找到内核。另外，GRUB 有一个特殊的交互式控制台方式，可以让您手工装入内核并选择引导分区。这个功能是无价的：假设
	GRUB 菜单配置不正确，但仍可以引导系统。哦，对了 -- GRUB 还有一个彩色引导菜单。更令人惊讶的是，这是一个自由软件!


　　一、什么是INIT:
　　init是Linux系统操作中不可缺少的程序之一。
　　所谓的init进程，它是一个由内核启动的用户级进程。


　　内核自行启动（已经被载入内存，开始运行，并已初始化所有的设备驱动程序和数据结构等）之后，就通过启动一个用户级程序init的方式，完成引导进程。所以,init始终是第一个进程（其进程编号始终为1）。


　　内核会在过去曾使用过init的几个地方查找它，它的正确位置（对Linux系统来说）是/sbin/init。如果内核找不到init，它就会试着运行/bin/sh，如果运行失败，系统的启动也会失败。

　　二、运行级别
　　那么，到底什么是运行级呢？
　　简单的说，运行级就是操作系统当前正在运行的功能级别。这个级别从1到6 ，具有不同的功能。
　　不同的运行级定义如下：(可以参考Red Hat Linux 里面的/etc/inittab）
　　# 0 - 停机（千万不能把initdefault 设置为0 ）
　　# 1 - 单用户模式
　　# 2 - 多用户，没有 NFS
　　# 3 - 完全多用户模式(标准的运行级)
　　# 4 - 没有用到
　　# 5 - X11 （xwindow)
　　# 6 - 重新启动 （千万不要把initdefault 设置为6 ）
　　这些级别在/etc/inittab 文件里指定。这个文件是init 程序寻找的主要文件，最先运行的服务是放在/etc/rc.d
	目录下的文件。在大多数的Linux 发行版本中，启动脚本都是位于 /etc/rc.d/init.d中的。这些脚本被用ln 命令连接到 /etc/rc.d/rcn.d
	目录。(这里的n 就是运行级0-6)
