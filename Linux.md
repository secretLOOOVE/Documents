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
