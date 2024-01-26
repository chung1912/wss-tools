from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import configparser

config = configparser.RawConfigParser()
config.read('./config.cfg',encoding='utf-8')

user = config.get('wenshushu','user').replace('"', '') 
pwd = config.get('wenshushu','pwd').replace('"', '')

def wenshushu_qiandao():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36')
    web = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=chrome_options)
    with open('./stealth.min.js') as f:
        js = f.read()
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
        })
    web.maximize_window() 
    url = "https://www.wenshushu.cn/signin"
    web.get(url)

    web.implicitly_wait(10)
    web.find_element(by=By.XPATH, value='//*[contains(text(),"密码")]').click()
    web.find_element(by=By.XPATH, value='//*[@placeholder="手机号 / 邮箱"]').send_keys(f'{user}')
    web.find_element(by=By.XPATH, value='//*[@placeholder="密码"]').send_keys(f'{pwd}')
    web.find_element(by=By.XPATH, value='//*[@type="submit"]').click()
    time.sleep(1)

    web.implicitly_wait(10)
    web.refresh()
    time.sleep(1)

    web.implicitly_wait(10)
    web.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]/div[1]/div[3]/div[2]/i').click()
    time.sleep(1)

    web.implicitly_wait(10)

    html=web.page_source

    # print(web.page_source)


    if ('今日已打卡' in html or '打卡成功' in html):
        try:
            html = html.replace('\n','')
            checkin_status = re.compile('class="clockin-tit">(.*?)</div>').findall(html) 
            names = re.compile('class="m-title5">(.*?)</div>').findall(html) 
            values = re.compile('class="re-num m-text9">(.*?)</div>').findall(html) 
            for i in range(len(values)):  
                values[i] = values[i].replace(' ','')
            checkin_num = re.compile('class="clockin-num">(.*?)</div>').findall(html) 
            result = '' 
            for i in range(len(names)):  
                if(names[i]=='手气不好'):  
                    continue
                result += names[i]+'：'+values[i]+'\n' 
            message = '账号' + user[:3] + checkin_status[0] +'\n' + checkin_num[0] +'\n' + result
            print(message)
        except:
            print('账号'+ user[:3] + '打卡失败')
    else:
        print('账号'+ user[:3] + '打卡还是失败')

    web.close()

def main():
    wenshushu_qiandao() 

if __name__ == "__main__":
    main()
