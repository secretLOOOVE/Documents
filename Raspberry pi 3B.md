****
### 40PIN管脚对照表

![40PIN管脚对照表](http://bbs.elecfans.com/data/attachment/forum/201604/24/215906lbb5hv12b1q7fb5b.png)

****
### GPIO控制

1. python GPIO
2. wiringPi 包括UART I2C SPI等 
3. BCM2835 C Library 

python GPIO  

    1.sudo apt-get install python-dev  
    2.安装RPi.GPIO
        wget http://raspberry-gpio-python.googlecode.com/files/RPi.GPIO-0.5.3a.tar.gz
        tar xvzf RPi.GPIO-0.5.3a.tar.gz
        cd RPi.GPIO-0.5.3a
        sudo python setup.py install
    
    例子：
        
        ```
        # -*- coding utf-8 -*-
        import RPi.GPIO as GPIO
        import time
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        
        while True:
            GPIO.output(11,GPIO.HIGH)
            time.sleep(1)
            GPIO.OUTPUT(11,GPIO.LOW)
            time.sleep(1)
            
        ```
    执行
    
        susdo python led.py
        
wiringPi GPIO

    1、说明：
    WiringPi是应用于树莓派平台的GPIO控制库函数，WiringPi遵守GUN Lv3。wiringPi使用C或者C++开发并且可以被其他语言包转，例如python、ruby或者PHP等。
    2.wiringPi安装


    1)方案A——使用GIT工具
    通过GIT获得wiringPi的源代码
    git clone git://git.drogon.net/wiringPi
    cd wiringPi
    ./build
    build脚本会帮助你编译和安装wiringPi

    2)方案B——直接下载
    我们可以在https://git.drogon.net/?p=wiringPi;a=summary网站上直接下载最新版本编译使用
    tar xfz wiringPi-xx.tar.gz
    cd wiringPi-xx
    ./build

    3、测试：
    wiringPi包括一套gpio命令，使用gpio命令可以控制树莓派上的各种接口，通过以下指令可以测试wiringPi是否安装成功。
    $gpio -v
    $gpio readall
    即可出现上面的io图

    4、例子：
    ```
    #include <wiringPi.h>    
    int main(void)    
    {    
      wiringPiSetup() ;    
      pinMode (0, OUTPUT) ;    
      for(;;)     
      {    
        digitalWrite(0, HIGH) ; delay (500) ;    
        digitalWrite(0,  LOW) ; delay (500) ;    
      }    
    }   
    ```
    5、编译运行：
    在树莓派上:
    gcc -Wall -o test test.c -lwiringPi 
    sudo ./test

    在虚拟机中：
    am-linux-gcc -Wall -o test test.c -lwiringPi 
    sudo ./test

    6、注意事项：
    1）IO的编号方式略有不同，采用wiring编码方式。
    2）-lwiringPi表示动态加载wiringPi共享库。
    
    

BCM2835 C Library

    1、下载:               $ wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.35.tar.gz
    2、解压缩:             $tar xvzf bcm2835-1.35.tar.gz
    3、进入压缩之后的目录:$cd bcm2835-1.35
    4、 配置:              $./configure
    5、从源代码生成安装包:$make
    6、执行检查:           $sudo make check
    7、安装 bcm2835库:    $sudo make install

    8、例子

        #include <bcm2835.h>    
    
        // P1插座第11脚    
        #define PIN RPI_GPIO_P1_11    
            
        int main(int argc, char **argv)    
        {    
          if (!bcm2835_init())    
          return 1;    
            
          // 输出方式    
          bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);    
            
          while (1)    
          {    
            bcm2835_gpio_write(PIN, HIGH);    
            bcm2835_delay(100);    
                
            bcm2835_gpio_write(PIN, LOW);    
            bcm2835_delay(100);    
          }    
          bcm2835_close();    
          return 0;    
        }   
    
****
#### GPIO应用详解  

导入    
    
    import RPi.GPIO as GPIO
    
    try:
        import RPi.GPIO as GPIO
    except RuntimeError:
        print("引入错误")
        
针脚编号：  

    GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BCM)
    
    mode=GPIO.getmode()
    
警告  

    如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告：

    GPIO.setwarnings(False)
    
引脚设置：  

    GPIO.setup(channel,GPIO.IN)
    GPIO.setup(channel,GPIO.OUT)
    GPIO.setup(channel,GPIO.OUT,initial=GPIO.HIGH)
    
释放：

    GPIO.cleanup()
    
输出：  

    chan_list=[11,12]
    GPIO.output(chan_list,GPIO.LOW)
    GPIO.output(chan_liet,(GPIO.HIGH,GPIO.LOW))
    
    GPIO.output(12,not GPIO.input(12))
    
读取:  

    GPIO.input(channel)
    低电平返回0 / GPIO.LOW / False，高电平返回1 / GPIO.HIGH / True。
    
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      # or
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
轮询方式:  

    while GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things
边缘检测:   

    wait_for_edge() 函数。
    wait_for_edge()被用于阻止程序的继续执行，直到检测到一个边沿。也就是说，上文中等待按钮按下的实例可以改写为：
    channel = GPIO.wait_for_edge(channel, GPIO_RISING, timeout=5000)
    if channel is None:
      print('Timeout occurred')
    else:
      print('Edge detected on channel', channel)
    add_event_detect() 函数
    该函数对一个引脚进行监听，一旦引脚输入状态发生了改变，调用event_detected()函数会返回true，如下代码：
    GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel
    do_something()
    // 下面的代码放在一个线程循环执行。
    if GPIO.event_detected(channel):
      print('Button pressed')
    上面的代码需要自己新建一个线程去循环检测event_detected()的值，还算是比较麻烦的。
    
    不过可采用另一种办法轻松检测状态，这种方式是直接传入一个回调函数：

    def my_callback(channel):
        print('This is a edge event callback function!')
        print('Edge detected on channel %s'%channel)
        print('This is run in a different thread to your main program')
    
    GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback)
    如果你想设置多个回调函数，可以这样：
    
    def my_callback_one(channel):
        print('Callback one')
    
    def my_callback_two(channel):
        print('Callback two')
    
    GPIO.add_event_detect(channel, GPIO.RISING)
    GPIO.add_event_callback(channel, my_callback_one)
    GPIO.add_event_callback(channel, my_callback_two)

使用PWM：  

    这个python函数库还支持PWM模式的输出，我们可以利用PWM来制作呼吸灯效果。详情看代码：
    
    import time
    import RPi.GPIO as GPIO   //引入库
    GPIO.setmode(GPIO.BOARD)  //设置编号方式
    GPIO.setup(12, GPIO.OUT)  //设置12号引脚为输出模式
    
    p = GPIO.PWM(12, 50)  //将12号引脚初始化为PWM实例 ，频率为50Hz
    p.start(0)    //开始脉宽调制，参数范围为： (0.0 <= dc <= 100.0)
    try:
        while 1:
            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc)   //修改占空比 参数范围为： (0.0 <= dc <= 100.0)
                time.sleep(0.1)
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    p.stop()    //停止输出PWM波
    GPIO.cleanup()    //清除
    
    
    
shell控制GPIO
-------------
    
    # 获得超级权限  
    sudo su  
    # 进入GPIO目录  
    cd /sys/class/gpio  
    # 使用ls查看gpio目录中的内容，可以查看到  
    # export gpiochip0 unexport   
    ls  
    # GPIO操作接口从内核空间暴露到用户空间  
    # 执行该操作之后，该目录下会增加一个gpio4文件  
    echo 4 > export  
    # 进入GPIO4目录，该目录由上一步操作产生  
    cd gpio4  
    #   查看gpio4目录中的内容，可查看到  
    #   active_low direction edge power subsystem uevent value  
    ls   
    # 设置GPIO4为输出方向  
    echo out > direction  
    # BCM_GPIO4输出逻辑高电平，LED点亮  
    echo 1 > value  
    #  BCM_GPIO4输出逻辑低电平，LED熄灭  
    echo 0 > value  
    # 返回上一级目录  
    cd ../  
    # 注销GPIO4接口  
    echo 4 > unexport  
    # 退出超级用户  
    exit  

    #!/bin/bash  
    #利用echo输出一些提示语句  
    echo export pin $1  
    echo $1 > /sys/class/gpio/export  
      
    echo setting direction to output  
    echo out > /sys/class/gpio/gpio$1/direction  
      
    echo setting pi high  
    echo 1 > /sys/class/gpio/gpio$1/value  

### 树莓派入门教程——开启SPI和I2C功能

	树莓派默认是将SPI和I2C功能关闭的，如果你编写SPI的程序，但是SPI模块没打开，可能会出现如下错误：
	ERROR: could not insert 'spi_bcm2708': No such device
	下面我们就针对如何开启SPI功能做下简单的说明，当然开启其他功能也是完全一样的。

	在终端输入
	sudo raspi-config
	命令，然后按照下图顺序依次操作即可，配置完成后重启树莓派即可生效。
	 

	若运行SPI程序出现如下错误
	Unable to open SPI device: No such file or directory
	则有可能是SPI模块并没有成功导入，用lsmod命令可以参看是否成功导入SPI模块

	若执行I2C相关程序出现如下错误
	Unable to open I2C device: No such file or directory
	用lsmod命令可以看到i2c_bmc2708字样，但是没i2c_dev字样，那么还需要做如下处理
	执行命令
	sudo nano /etc/modules                # 使用nano打开文件
	然后增加
	i2c_dev
	行，安Ctrl+X退出编辑，输入Y保存内容，然后重启即可。
	 


		

		
		
		
