import random
import time  #设置延时
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from lxml import etree

#设置浏览器头部
chrome_options = Options()   #实例化Options类
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--user-data-dir=/dev/null')
#接管浏览器
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(options=chrome_options)
#隐藏navigator.webdriver标志(浏览器打开后navigator的值为false或undefine)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})#driver.execute_cdp_cmd:执行Chrome Devtools Protocol命令
#设置user-agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
#注入js文件
with open(r"C:\Users\yangj\PycharmProjects\practice project2\stealth.min.js", mode='r') as f:
    js = f.read()
    print('注入js成功')
driver.execute_cdp_cmd(
    cmd_args={'source': js},
    cmd="Page.addScriptToEvaluateOnNewDocument",
)
#进入网址
def get_url():
    driver.get('https://www.xiaohongshu.com/explore')

def spider():
    try:
        print('开始爬取')
        #通过CLASS_NAME获取要进入的页面
        time.sleep(random.randint(10,15))
        #往下滚动

        print(driver.current_url)
        #获取元素(待点击的页面列表)
        input_first = driver.find_elements(By.CLASS_NAME,'note-item')
        time.sleep(random.randint(2,7))
        print(input_first)
        #等待页面加载
        for i in input_first:
            print('进入循环')
            button = i.find_element(By.CLASS_NAME,'cover')
            button.click()
            time.sleep(random.randint(1,3))
            #点击完后等待加载
            #time.sleep(random.randint(2,7))
            print(driver.current_url)
            #获取评论
            review = driver.find_elements(By.CLASS_NAME, 'content')
            for i in review:
                with open(r"D:\spiderdata\reviews.txt", mode='at', encoding='utf-8') as f:
                    f.write(i.text)
                    f.write('\n')
                    print('写入成功')
             # 返回原始页面
            driver.back()
            time.sleep(random.randint(2, 6))
            print('-----------翻页------------------------')

    except Exception as e:
        print(e)

#用XPATH匹配
def spider2():
    try:
        print('开始爬取')
        time.sleep(random.randint(10,15))
        for i in range(10):
            button = driver.find_element(By.XPATH,"//a[@class='cover ld mask']")
            button.click()
            time.sleep(random.randint(2,7))
            print(driver.current_url)
            review = driver.find_elements(By.CLASS_NAME, 'content')
            for i in review:
                with open(r"D:\spiderdata\reviews.txt", mode='at', encoding='utf-8') as f:
                    f.write(i.text)
                    f.write('\n')
                    print('写入成功')
                    time.sleep(random.randint(4,7))
            driver.back()

    except Exception as e:
        print(e)
if __name__ == '__main__':
    #get_url()
    spider()

