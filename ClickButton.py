def NIMIKit(temp, driver):
    # from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    # import time
    # start_time = time.time()
    # start_time1 = time.clock()
    # from bs4 import BeautifulSoup
    # path = 'D:/CyKITv2-master/Web/CyKITv2.html'

    ### 爬虫抓取
    # htmlfile = open(path, 'r', encoding='utf-8')
    # htmlhandle = htmlfile.read()
    # soup = BeautifulSoup(htmlhandle, 'html5lib')

    # options = Options()
    # CHROMEDRIVER_PATH = 'D:\\Python\\Scripts\\chromedriver'
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.set_headless(True)
    ## 设定chrome UI界面不显示，定义了options用于使用--headless的Chrome，最后记得将options参数传递给driver
    # driver = webdriver.Chrome(chrome_options=options)
    # driver.get(path)
    # page = driver.page_source  ## source code
    # driver.maximize_window()
    # driver.implicitly_wait(8)
    if temp == 0:
        element = driver.find_element_by_id("cyConnect")
        # print(element.get_attribute('value'))

        element.click()
    # driver.close()
    # end_time = time.time()
    # end_time1 = time.clock()
    # print("start time: " + str(start_time)+ "  or:" + str(start_time1))
    # print("end time: " + str(end_time) + "  or:" + str(end_time1))
    # print("duration: " + str(end_time - start_time)+ "  or:" + str(end_time1 - start_time1))

    # driver.quit()
    # time.sleep(2)
    elif temp == 1:
        element2 = driver.find_element_by_id("cyDisconnect")
        element2.click()