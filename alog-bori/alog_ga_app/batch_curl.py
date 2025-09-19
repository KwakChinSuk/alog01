import sys
import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import cfg

def fn_home_html_capture_cache(purl):
    # 1. Chrome 설정
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + " START " + purl)
    options = Options()
    options.add_argument('--headless')  # 화면 표시 없이 실행
    #options.add_argument("--window-size=1920,20000")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # 리눅스 메모리 문제 회피
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=PushMessaging,UseGCMChannel,OnDeviceModel")
    # 2. 브라우저 열기
    driver = webdriver.Chrome(options=options)
    # 3. 웹페이지 열기
    driver.set_page_load_timeout(60*10)    
    driver.set_script_timeout(60*10)
    try:
        driver.get(purl)  # <- 원하는 URL로 변경
    except Exception as e:
        print(e)
        datetime.time.sleep(60*10)  # 필요에 따라 조정 10분
        driver.quit()
        sys.exit(1)

    driver.quit()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + " Complete " + purl)


strSQL = " select 'alog_bori' dbsname,url from alog_bori.tga_url where exec_dt is null group by url order by max(create_dt) desc "
result = cfg.fnSQLselect(strSQL)
if not (result is None) :
    for row in result:        
        strSQL =" update " +row[0]+".tga_url set exec_dt = current_timestamp where url = '" +row[1]+"' and exec_dt is null "
        cfg.fnSQLexe(strSQL)
        fn_home_html_capture_cache(row[1])
        print('60초 대기')
        time.sleep(60*1)  # 필요에 따라 조정 10분

    print('COMPLETE')

    #sys.exit()
 
