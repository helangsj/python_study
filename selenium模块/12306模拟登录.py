
import requests
from hashlib import md5


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

from selenium import  webdriver
from time import sleep
#导入图片裁剪模块
from PIL import Image
from selenium.webdriver import ActionChains
bro = webdriver.Chrome(executable_path='./chromedriver')
bro.get('https://kyfw.12306.cn/otn/login/init')
sleep(2)
#save_screenshot将当前页面进行截图并保存
bro.save_screenshot('./aa.png')

#确定验证码图片对应的左上角和右下角的坐标（确定裁剪的区域）
code_img_ele = bro.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img')
#验证码左上角的坐标x,y
location = code_img_ele.location
print('左上角的坐标',location)
#验证码图片的长和宽
size = code_img_ele.size
print('验证码图片的长和宽',size)

#左上角坐标和右下角坐标
# a = int (location['x'])+70
# b = int(location['y'])+70
# rangle = (a,b,a + int(size['width'])+70,b+int(size['height'])+50)
a = int (location['x'])
b = int(location['y'])
rangle = (a,b,a + int(size['width']),b+int(size['height']))
print('左上角坐标和右下角坐标',rangle)
#将截取的图片进行裁剪
i = Image.open('./aa.png')
code_img_name = './code.png'
#根据crop进行裁剪
frame = i.crop(rangle)
frame.save(code_img_name)
# #将截取的图片进行超级鹰验证码识别
chaojiying = Chaojiying_Client('helang', 'helang', '912208')  # 用户中心>>软件ID 生成一个替换 96001
im = open('./code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
print(chaojiying.PostPic(im, 9004)['pic_str'])

result = chaojiying.PostPic(im, 9004)['pic_str']
all_list = []
#要存储即将被点击的点的坐标[[x,y],[x1,y1]]
if '|' in result:
    list_1 = result.split('|')
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
print(all_list)

#遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行点击操作
for i in all_list:
    x = i[0]
    y = i[1]
    ActionChains(bro).move_to_element_with_offset(code_img_ele,x,y).click().perform()
    sleep(2)
bro.find_element_by_id('username').send_keys('helang9728')
bro.find_element_by_id('password').send_keys('helang9728')
bro.find_element_by_class_name('btn200s').click()
sleep(5)
bro.quit()