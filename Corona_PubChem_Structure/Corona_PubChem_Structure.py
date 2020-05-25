#-*- coding:utf-8 -*-

import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

f = open("Corona_drug_structure.txt", "w", encoding="utf-8")

f_in = open("bern_drug_cui_sorted.txt","r")

drug_data = f_in.readlines()

options_chrome = webdriver.ChromeOptions()
# options_chrome.add_argument('headless')
# options_chrome.add_argument('window-size=1920x1080')
# options_chrome.add_argument("disable-gpu")

# UserAgent값을 바꿔줍시다!
options_chrome.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

options_chrome.add_argument("download.default_directory=C:/Pubchem/Default")

driver = webdriver.Chrome('C:/Users/kms0845/Desktop/CoronaNet/Selenium/chromedriver_win32/chromedriver.exe', options=options_chrome)

driver.get("https://pubchem.ncbi.nlm.nih.gov/#query=3TC")

#/html/body/div[2]/form/div[1]/main/div[3]/table/tbody/tr[1]/td[2]/a
#/html/body/div[2]/form/div[1]/main/div[3]/table/tbody/tr[2]/td[3]/a
#/html/body/div[2]/form/div[1]/main/div[3]/table/tbody/tr[3]/td[3]/a

driver.implicitly_wait(10)
cnt = 0

time.sleep(3)



driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div[1]/a").click()

time.sleep(10)


pubchem_cid = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[1]/div[3]/div/table/tbody/tr[1]/td").text

print(pubchem_cid)

# driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div/ul/li[3]/div/ul/li[1]/div/div[2]/a").click()
# time.sleep(10)
#
# webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

time.sleep(3)


for drug_line in drug_data:
    time.sleep(3)
    for i in range(1,11):
        #/ html / body / div[2] / form / div[1] / main / div[3] / table / tbody / tr[1] / td[3] / a
        time.sleep(random.randint(10, 15))
        xpath = "/html/body/div[2]/form/div[1]/main/div[3]/table/tbody/tr["+str(i) + "]/td[2]/a"
        driver.find_element_by_xpath(xpath).click()

        time.sleep(random.randint(10,30))

        product_name = "aaa"
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')



        tables = soup.find_all('table')

        title_bool = False

        title_s_table = "##@@!!국내제품"
        cnt = cnt + 1
        #print(title_s_table)
        print(product_name+"&&&"+str(cnt))
        f.flush()
        f.write("^^^&&&$$$"+str(cnt)+"\n")
        f.write(title_s_table)
        f.write("\n")

        for T in tables:
            contents = T.select('table > tbody > tr')
            title_bool = False


            for content in contents:
                tds = content.find_all("td")
                out_temp = ""
                if(len(tds) >= 2):
                    if(title_bool == False) :
                        title_s_table = "##@@!!"
                        title_s_table = title_s_table + str(T.parent.contents[1].contents[0])
                        #print(title_s_table)

                        f.write(title_s_table)
                        f.write("\n")

                        title_bool = True
                    for td in tds:
                        out_temp = out_temp  + td.text + "@#$"

                    #print(out_temp)

                    f.write(out_temp)
                    f.write("\n")
                else:
                    #title_s_table = "##@@!!국내제품"
                    #print(title_s_table)
                    for td in tds:
                        try:
                            td_title = td.parent.select('th')[0].text
                        except:
                            continue
                        out_temp = str(td_title) + "@#$" + td.text
                        #print(td_title)
                        f.write(out_temp)
                        f.write("\n")

        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/main/div[3]/article/div[4]/button").click()
        time.sleep(random.randint(10,30))

    print("end of page")
    #/ html / body / div[2] / form / div[1] / main / div[3] / div[2] / div / ul / li[10] / a
    driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/main/div[3]/div[2]/div/ul/li[8]/a").click()
    time.sleep(random.randint(10,30))

time.sleep(30)

temp = 1

driver.close()