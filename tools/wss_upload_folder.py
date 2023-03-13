from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import configparser

config = configparser.RawConfigParser()
config.read('./config.cfg')

user = config.get('wenshushu','user').replace('"', '') 
pwd = config.get('wenshushu','pwd').replace('"', '')

def wenshushu_upload_folder(file_path:str,folder:str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    web = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=chrome_options)
    ac = ActionChains(web)
    url = "https://www.wenshushu.cn/drive/xxxxxxx/folder/xxxxxxxx" 
    web.get(url) 
    web.implicitly_wait(10)
    try:
        web.find_element(by=By.XPATH, value='//*[contains(text(),"密码")]').click()
        web.find_element(by=By.XPATH, value='//*[@placeholder="手机号 / 邮箱"]').send_keys(f'{user}')
        web.find_element(by=By.XPATH, value='//*[@placeholder="密码"]').send_keys(f'{pwd}')
        time.sleep(1)
        web.find_element(by=By.XPATH, value='//*[@type="submit"]').click()
        time.sleep(1)
        ac.move_to_element(web.find_element(by=By.XPATH, value='//*[contains(text(),"上传")]')).perform()
        web.find_element(by=By.XPATH, value='//*[contains(text(),"选择整个文件夹")]').click()
        time.sleep(1)
        web.implicitly_wait(10)
        upload = web.find_element(by=By.XPATH, value='//*[@type="file"]')
        upload.send_keys('/{0}/{1}'.format(file_path,folder)) 
        # print(upload.get_attribute('value') )
        wait = WebDriverWait(web,12)
        # print(web.page_source)
        if wait.until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"上传成功")]'))):
            time.sleep(1)
            msg = folder + ' 已上传'
        elif wait.until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"上传失败")]'))):
            time.sleep(1)
            msg = folder + ' 上传失败'
        elif wait.until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"网络错误")]'))):
            time.sleep(1)
            msg = folder + ' 网络错误'
        else:
            time.sleep(1)
            msg = folder + ' 失败了'
        # 隐性等待
        web.implicitly_wait(10)
        # html=web.page_source
        # print(web.page_source)
        print(msg)
        web.close()
        return msg
    except:
        time.sleep(1)
        msg = '上传错误，未找到文件夹:' + folder
        web.implicitly_wait(10)
        print(msg)      
        web.close()
        return msg

def main():
    wenshushu_upload_folder("filepath","folder")

if __name__ == "__main__":
    main()
