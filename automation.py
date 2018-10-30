from splinter import Browser
from bs4 import BeautifulSoup
from selenium.common.exceptions import UnexpectedAlertPresentException
import csv
import time
import cv2
import numpy as np
from PIL import Image
import pytesseract
from io import BytesIO
import requests
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
Grade2Point={'A+':10,'A':9,'B+':8,'B':7,'C+':6,'C':5,'D':4,'F':0,'I':0,'W':0}
url="http://ims.mitsgwalior.in/Result/Result_BE.aspx"
def Strcount(num):
    if(num<10):
        return '00'+str(num)
    elif(num<100):
        return '0'+str(num)
    else:
        return str(num)

Brach_code='CS'#input('Enter you Branch Code :-')
year='16'#input('Enter the last to digit of your admission year :- ')
sem='4'#input('Enter the sem in no. :-')
browser = Browser('chrome')
browser.visit(url)
first=1
last=129

a,LAST=first,last

semsel=browser.find_by_name('ctl00$ContentPlaceHolder1$drpSemester')
semsel.select(sem)
fieldmy=['Name','Roll No.',Brach_code,sem,'BCSL-'+sem+'01- [T]','BCSL-'+sem+'02- [T]','BCSL-'+sem+'03- [T]','BCSL-'+sem+'04- [T]','BCSL-'+sem+'05- [T]','BCSL-'+sem+'02- [P]','BCSL-'+sem+'03- [P]','BCSL-'+sem+'04- [P]' ,'BCSP-'+sem+'06- [P]','BCSS-'+sem+'07- [P]','BCSS-'+sem+'08- [P]','Result','SGPA']
with open('Result.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fieldmy)
    while(a<=LAST):
        
        try:
            browser.fill('ctl00$ContentPlaceHolder1$txtrollno', '0901'+Brach_code+year+'1'+Strcount(a))
            html=browser.html
            soup=BeautifulSoup(html,'lxml')
            img=soup.find('img',{'alt':'Captcha'})
            img_url=url+"/"+img['src']
            response = requests.get(img_url)
            img_cap = Image.open(BytesIO(response.content))
            img_cap = cv2.cvtColor(np.array(img_cap), cv2.COLOR_RGB2GRAY)
            cap= pytesseract.image_to_string(img_cap,lang = 'eng')
            cap = cap.upper()
            cap = cap.replace(" ","")
            browser.fill('ctl00$ContentPlaceHolder1$TextBox1',cap)#To fill captcha
            time.sleep(3)
            while(soup.find(id="ContentPlaceHolder1_lblNameGrading") == None):
                #print("Wait:")
                view_result=browser.find_by_name('ctl00$ContentPlaceHolder1$btnviewresult')#access result
                view_result.click()
                soup=BeautifulSoup(browser.html,'lxml')
            time.sleep(2)
            soup=BeautifulSoup(browser.html,'lxml')
            name=soup.find(id="ContentPlaceHolder1_lblNameGrading").text
            roll_no='0901'+Brach_code+year+'1'+Strcount(a)
            html_grade=soup.find_all(attrs= {"id":"ContentPlaceHolder1_pnlGrading"})
            html_grade_list=BeautifulSoup(str(BeautifulSoup(str(html_grade),'lxml').find('tbody')),'lxml').find_all('tr')
            grade_list=[None]*11
            for i in range(9,9+11):
                final=BeautifulSoup(str(html_grade_list[i]),'lxml').find_all('td')
                grade_list[i-9]=BeautifulSoup(str(final[3]),'lxml').text
                #print(final[3])
                #print(grade_list[i-9])
            #print(grade_list)
            result=soup.find(id="ContentPlaceHolder1_lblResultNewGrading").text
            SGPA=soup.find(id="ContentPlaceHolder1_lblSGPA").text
            roww=[name,roll_no,Brach_code,sem]
            roww.extend(grade_list)
            roww.extend([str(result),str(SGPA)])
            print(roww)
            writer.writerow(roww)
            #print("reset -- Start")
            reset=browser.find_by_name('ctl00$ContentPlaceHolder1$btnReset')
            reset.click()
            #print("reset -- End")
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