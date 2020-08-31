脚本基于[tobyqin/kog-money](https://github.com/tobyqin/kog-money) 改动。

## 原理
使用adb模拟点击+图像识别（匹配的图片在maoxian文件夹下面） 刷冒险模式，具体哪个关卡不限制

最好选择高级别（普通、精英、大师）高等级（有个推荐等级）的地图，金币高一点
（**第一把先选好对应的关卡和阵容，进去开启自动战斗打一把**）

## 环境
运行环境：[腾讯手游助手](https://syzs.qq.com/) （可替换为真机），其他模拟器应该也没问题，只不过腾讯手游助手安全性应该高点，毕竟腾讯自己的产品。

电脑环境:

    1. adb
    2. python运行环境（我用的3.8.0）
    3. 注意要配置到环境变量中
## 运行
先使用 pip install -r requirements.txt 安装运行所需的module（可能有多余的我没删除，不过影响不大），缺少的module自己对应安装一下

adb命令：
启动服务：adb start-server  
查找设备列表：adb devices (应该可以看到一个模拟器/手机设备)

停止服务(一般不需要使用)：adb kill-server

运行money.py

如果遇到问题就debug嘛。

分辨率设置的1280*720
如果是模拟器就把模拟器的分辨率调成这个分辨率，然后宽高也拉动成这么大（无实际影响，主要是如果要自己改模拟点击的坐标，不用计算了）

如果是手机，util里面调成对应的分辨率，或者自己算成对应分辨率的坐标点（主要我也没用过手机刷，后续再补上对应的说明吧）

## 反馈 
有啥问题欢迎提issue

## 声明

本脚本纯属娱乐和探索的心得，如果你因为违反了游戏规则导致被封号，我概不负责。