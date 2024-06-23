# author:jiangxinwujiangjin
# enconding = 'UTF-8'
import random
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
driver = webdriver.Chrome()
import csv

#先把自动化的特征给稍微隐藏

#设置user-agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
#隐藏navigator.webdriver标志(浏览器打开后navigator的值为false或undefine)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})#driver.execute_cdp_cmd:执行Chrome Devtools Protocol命令
#设置user-agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
urls = ['https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-10-x-110000-2-x-x-x-x-x','https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-10-x-110000-3-x-x-x-x-x']
def get_url(url):
    for url in urls:
        driver.get(url)
        spider1()

#wait = WebDriverWait(driver, 10)


def spider1():
    print('开始爬取')
    time.sleep(random.randint(5,8))
    #滚动页面
    #driver.execute_script("window.scrollBy(0,1000000)")
    time.sleep(random.randint(5,8))
    elements = driver.find_elements(By.CLASS_NAME,'line-1')
    time.sleep(2)
    for message in elements:
        message.click()
        #获取窗口句柄
        all_windows = driver.window_handles
        #切换页面
        driver.switch_to.window(all_windows[1])
        #在打开页面要做的操作
        time.sleep(random.randint(2,5))


        new_messages = driver.find_elements(By.CLASS_NAME,'car-archives_value__3YXEW')
        message_list = []
        for new_message in new_messages:

            message_list.append(new_message.text)
        #去掉无用信息
        for i in range(0,3):
            message_list.pop(-1)
            print(message_list)
        elements1 = driver.find_elements(By.CLASS_NAME,'line-1')
        element_list = []
        for element in elements1:

            element_list.append(element.text)
        message_list.append(element_list[0])
        #开始往csv文件写入
        with open(r'E:\data.csv',mode='a',encoding='utf-8-sig') as csvfile:
            #初始化文件写入对象
            writer = csv.writer(csvfile,delimiter=',')
            print(message_list)
            writer.writerow(message_list)



        #关闭窗口回来原页面，再切换页面
        driver.close()
        driver.switch_to.window(all_windows[0])
        #等一会再点击，减弱自动化工具特征
        time.sleep(random.randint(1,3))


get_url('https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-10-x-110000-3-x-x-x-x-x')
spider1()