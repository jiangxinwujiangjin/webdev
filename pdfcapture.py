import requests
import os
from bs4 import BeautifulSoup
import asyncio
import aiohttp
url = "http://www.power-mos.com/products.php"
params = {"id":"49","page":"1"}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie':'__51uvsct__3G5Pk0eEh7wEuiuP=1; __51vcke__3G5Pk0eEh7wEuiuP=ba0862ce-6173-5ff3-be64-8b089b715adc; __51vuft__3G5Pk0eEh7wEuiuP=1744770488111; __vtins__3G5Pk0eEh7wEuiuP=%7B%22sid%22%3A%20%22ea852a7e-43b5-50c5-9522-5409f45a8367%22%2C%20%22vd%22%3A%2018%2C%20%22stt%22%3A%20934551%2C%20%22dr%22%3A%20387772%2C%20%22expires%22%3A%201744773222659%2C%20%22ct%22%3A%201744771422659%7D',
           }
save_dir = r'G:\hfx\pdf2'
def download_pdf(pdf_url,save_dir,file_name):
    os.makedirs(save_dir,exist_ok=True)
    file_name = file_name
    file_path = os.path.join(save_dir,file_name)
    try:
        response = requests.get(pdf_url,headers=headers,stream=True,timeout=10)
        response.raise_for_status()
        with open(file_path,'ab') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f'PDF文件已经保存到{file_path}')
    except requests.exceptions.RequestException as e:
        print(f'下载时出错{e}')


def test(url,params,headers,save_dir=save_dir,*args,**kwargs):
    """爬取单页网页"""
    response = requests.get(url=url,params=params,headers=headers)
    pdf_links = []
    if response.status_code == 200:
        """拿到源代码"""
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table',class_='table product_table product_table_1')
        
        """获取到所有的pdf链接"""
        pdf_links = table.find_all('a')
        count = 0
        for pdf in pdf_links:
            """拿到pdf链接并请求pdf然后写入本地文件"""
            pdf_url = pdf.get('href')
            pdf_url = 'http://www.power-mos.com/'+ str(pdf_url)
            file_name = pdf.get_text(strip=True)
            file_name = file_name + '.pdf'
            print(file_name)
            download_pdf(pdf_url,save_dir=save_dir,file_name=file_name)
            count += 1
            print(f'第{count}页保存成功')
            
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return True

"""异步爬取"""
url_container = ['http://www.power-mos.com/products.php?id=55']
#异步爬取
async def fetch(url,session,headers=headers):
    async with session.get(url=url,headers=headers) as resp:
            print(resp.status)
            resp.raise_for_status()
            return await resp.text()

        
async def main(urls=url_container,headers=headers):
    urls = urls
    pdf_container = []
    file_name_list = []
    headers = headers
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url,session) for url in urls]
        results = await asyncio.gather(*tasks,return_exceptions=True)
        for result in results:
            soup = BeautifulSoup(result,'lxml')
            table = soup.find('table',class_='table product_table product_table_1')
            pdf_links = table.find_all('a')
            for pdf in pdf_links:
                pdf_url = pdf.get('href')
                pdf_name = pdf.get_text(strip=True)
                pdf_url = "http://www.power-mos.com/"+str(pdf_url)
                pdf_container.append(pdf_url)
                file_name = pdf_name + '.pdf'
                file_name_list.append(file_name)
        count = 0
        for pdf in pdf_container:
            download_pdf(pdf,save_dir=save_dir,file_name=file_name_list[count])
            count += 1
            print(f'第{count}页保存成功')
        
        

asyncio.run(main())