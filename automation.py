from splinter import Browser
from bs4 import BeautifulSoup
from selenium.common.exceptions import UnexpectedAlertPresentException
import csv
import time
Grade2Point={'A+':10,'A':9,'B+':8,'B':7,'C+':6,'C':5,'D':4,'F':0,'I':0,'W':0}
url="http://ims.mitsgwalior.in/Result/Result_BE.aspx"
def Strcount(num):
    if(num<10):
        return '00'+str(num)
    elif(num<100):
        return '0'+str(num)
    else:
        return str(num)

browser = Browser('chrome')
browser.visit(url)
a,LAST=44,129
sem=browser.find_by_name('ctl00$ContentPlaceHolder1$drpSemester')
sem.select('4')
fieldmy=['Name','Roll No.','Branch','Sem','BCSL-401- [T]','BCSL-402- [T]','BCSL-403- [T]','BCSL-404- [T]','BCSL-405- [T]','BCSL-402- [P]','BCSL-403- [P]','BCSL-404- [P]' ,'BCSP-406- [P]','BCSS-407- [P]','BCSS-408- [P]','Result','SGPA']
with open('NewG.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fieldmy)
    while(a<=LAST):
        browser.fill('ctl00$ContentPlaceHolder1$txtrollno', '0901CS161'+Strcount(a))
        try:
        
            while(not browser.find_by_name('ctl00$ContentPlaceHolder1$btnReset')):#wait till captcha is filled
                print("wait")
            soup=BeautifulSoup(browser.html,'lxml')
            name=soup.find(id="ContentPlaceHolder1_lblNameGrading").text
            roll_no='0901CS161'+Strcount(a)
            html_grade=soup.find_all(attrs= {"id":"ContentPlaceHolder1_pnlGrading"})
            html_grade_list=BeautifulSoup(str(BeautifulSoup(str(html_grade),'lxml').find('tbody')),'lxml').find_all('tr')
            grade_list=[None]*11
            for i in range(9,9+11):
                final=BeautifulSoup(str(html_grade_list[i]),'lxml').find_all('td')
                grade_list[i-9]=BeautifulSoup(str(final[3]),'lxml').text
                print(final[3])
                print(grade_list[i-9])
            print(grade_list)
            result=soup.find(id="ContentPlaceHolder1_lblResultNewGrading").text
            SGPA=soup.find(id="ContentPlaceHolder1_lblSGPA").text
            roww=[name,roll_no,'CS',str(4)]
            roww.extend(grade_list)
            roww.extend([str(result),str(SGPA)])
            print(roww)
            writer.writerow(roww)
            reset=browser.find_by_name('ctl00$ContentPlaceHolder1$btnReset')
            reset.click()
            a=a+1 
        except UnexpectedAlertPresentException:
            time.sleep(1)
            alert = browser.get_alert()
            if(alert.text=="you have entered a wrong text"):
                alert.accept()
                continue
            alert.accept()
            a=a+1
            browser.find_by_name('ctl00$ContentPlaceHolder1$btnReset').click()
            continue