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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
