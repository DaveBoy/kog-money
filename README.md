脚本基于[tobyqin/kog-money](https://github.com/tobyqin/kog-money) 改动。

## 原理
使用adb模拟点击+图像识别（匹配的图片在maoxian文件夹下面） 刷冒险模式，具体哪个关卡不限制

最好选择高级别（普通、精英、大师）高等级（有个推荐等级）的地图，金币高一点
（**第一把先选好对应的关卡和阵容，进去开启自动战斗打一把**）

## 环境
运行环境：

**真机（推荐）>[腾讯手游助手](https://syzs.qq.com/) >其他模拟器**

1、真机无疑是最好的，模拟度最高（最好不要用root了的手机）

2、腾讯手游助手次之，一般模拟器玩游戏可能会被封号(见下面的链接)。

虽然腾讯手游助手作为模拟器能过腾讯对模拟器的检测这关（还不一定，网上也有人拿腾讯手游助手被封号），不过作为自己的模拟器，检测权限可能也比真机高，毕竟能拿到的数据更多更好检测。


之前我一直使用的腾讯手游助手，后来有一次拿小号打了一把人机拿首胜，懒得换手机，结果被封了一个月。**第一次申诉告诉我原因是使用了模拟器，第二次申诉我说我用的腾讯手游助手之后，理由又变成了使用脚本挂机。** 然后我抽空弄了一下其他分辨率的识别，转移阵地到真机上了。


3、一般模拟器:[有人用模拟器封号过](https://www.baidu.com/s?ie=UTF-8&wd=%E6%A8%A1%E6%8B%9F%E5%99%A8%20%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80%20%E8%A2%AB%E5%B0%81%E5%8F%B7) 

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
    
    不同分辨率就使用不同maoxian文件夹下面的截图来识别

## 其他分辨率

    1、需要截图的界面运行crop_screenshot.py文件，生成截图（小米miui12出现了奇怪的问题，截图生成到手机的文件名加了时间戳，需要更改crop_screenshot.py中调用方法screen_crop为screen_crop_fix）
    
    2、然后自己对生成的图片编辑-->裁剪指定区域生成maoxian文件夹下对应图标（具体图标参考maoxian_2248文件夹），不能直接截图，要用裁剪。
    
    3、**我自己用的2248的文件夹，其他分辨率的截图如果不对（可以通过test.py进行测试，查看每个图片的匹配度），可能需要大家自己制作（需要的文件参照2248目录）,制作方式参照根目录下的[制作截图.gif](https://github.com/DaveBoy/kog-money/blob/master/%E5%88%B6%E4%BD%9C%E6%88%AA%E5%9B%BE.gif)**

## ~~增加server酱微信通知~~
    
    即将弃用，因为server酱开始收费了
    
    在config.ini中配置SERVER_SCKEY = xxx
    
    [server酱](http://sc.ftqq.com/?c=code)


## 增加企业微信应用消息推送
[企业微信推送设置](https://note.youdao.com/ynoteshare1/index.html?id=351e08a72378206f9dd64d2281e9b83b&type=note)

1、创建企业（不需要认证）（https://work.weixin.qq.com/wework_admin/loginpage_wx）

    我的企业--》企业信息--》企业ID

2、创建应用（https://work.weixin.qq.com/wework_admin/frame#apps）

    应用管理-应用-自建-创建应用，自己创建完成后获取secret和AgentID

3、扫码
    我的企业--》微信插件--》邀请关注
    
4、配置参数

    在config.ini中配置
    
    corpid = 如：ww840aa3aa97123456 我的企业--》企业信息--》企业ID
    
    agentid = 如：1000002 应用管理--》应用--》自建--》应用名称--》AgentId
    
    corpsecret = 如：qqRXgScAQ_aCq_QIpmutuf7xY236caGfIi_PDaHD9eD 就在agentid下面一行



## 注意点
test.py:发现匹配出现问题时调试使用，可以生成识别结果裁剪到maoxian_crop文件夹，自己查看是否是正确的区域

crop_screenshot.py:用来多次截图，方便后续裁剪生成对应分辨率的target识别图标

constant.SCREEN_METHOD = 0 #0一般手机都行  1是0截图出问题的时候(看根目录下生成的screen.png是否正常)用，比如腾讯手游助手就需要设置为1
## 反馈 
有啥问题欢迎提issue

## 更新日志
2021年3月5日：Server酱即将收费，集成企业微信应用消息推送，具体方法见readme中'增加企业微信应用消息推送'

2021年2月20日：目前发现vx区和qq区的图对比后的相似度有区别，而原本设置的相似度为0.9，如果偶尔出现未识别问题，可以尝试调低相似度，建议区间0.8-0.9。也可以同一个图截图多个（如b_finish和b_finish_vx）


2021年1月25日：适配新版本，更改下一步的坐标（其实可以改为截图识别，下次一定。。），截图只更新了2248分辨率(剩余金币上限截图，等我金币上限了就更新)，其他分辨率自行运行test.py保存按照截图，再按照根目录‘制作截图.gif’进行相关界面的图片裁剪。

## 声明

本脚本纯属娱乐和探索的心得，如果你因为违反了游戏规则导致被封号，我概不负责。