from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from rest_framework.decorators import api_view
import requests
# Create your views here.
@api_view(['GET'])
def home_page(request):
    logging.basicConfig(filename="scrapper_home.log" , level=logging.INFO)
    if request.method == 'GET':
        try:
            return render(request,"search.html")
        except:
            logging.info("no home page")
        

@api_view(['GET','POST'])
def comment(request):
    if request.method == 'POST':
        try:
            searchString = request.POST.get('content')
            
            driver=webdriver.Firefox()
            #driver for date,title,view
            driver.implicitly_wait(10)
            driver.get(searchString)
            try:
                title=driver.find_element(By.XPATH,'//*[@id="title"]/h1/yt-formatted-string').text
            except:
                logging.info('no title element found')
            body = driver.find_element(By.TAG_NAME,"body")
            body.send_keys(Keys.PAGE_DOWN)
            try:
                more=driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/div[1]/yt-formatted-string/span[1]')
                more.click()
            except:
                logging.info("no more box found")
            try:
                date=driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/div[1]/yt-formatted-string/span[3]').text
            except:
                logging.info("no date element found")
            try:
                view=driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/div[1]/yt-formatted-string/span[1]').text.split()[0]
            except:
                logging.info("no view element found")
            driver.quit()
            
            #driver for comment
            driver=webdriver.Firefox()
            driver.implicitly_wait(10)
            driver.get(searchString)
            for i in range(10):
                time.sleep(1)
                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
            try:
                img=driver.find_elements(By.XPATH,'//div[@id="body"]/div/a/yt-img-shadow/img[@id="img"]')
            except:
                logging.info("no img element found")
            try:
                main_box=driver.find_elements(By.XPATH,'//div[@id="main"]')
            except:
                logging.info("no main_box found")
                
            #storing img data
            d=[]
            for i in img:
                try:
                    d.append(i.get_attribute('src'))
                except:
                    logging.info("img src attribte not found")
                    
            #storing comment data
            d2=[]
            for g in main_box:
                try:
                    d2.append(((g.text)))
                except:
                    logging.info("main_box text not found")
            driver.quit()
            
            #now adding img + comment data
            d3=[]
            try:
                for j in range(len(d2)):
                    try:
                        d3.append(d2[j]+'\n'+d[j])
                    except:
                        logging.info(len(d),len(d2),'d out of range')
            except :
                        logging.info("d out of range")
                        
                
            #now giving data user,img,like,commet
            u=[]
            for i in d3:
                q=i.split('\n')
                try:
                    us=q[0].split('@')[1]
                except:
                    us=''
                    logging.info("no username found")
                try:
                    comment=q[2]
                except:
                    comment=''
                    logging.info("no comment found")
                try:
                    like=q[3]
                    if 'K' and '.' in like:
                        like=int(float(like[:-1]) * 1000)
                    elif 'K' in like:
                        like=(int(like[:-1]) * 1000)
                    else:
                        like=int(like)
                except:
                    like=0
                    logging.info("0 like found")
                try:
                    imgs=q[5]
                    if 'https' in imgs:
                        imgs=imgs
                    else:
                        imgs=''
                except IndexError as e :
                    imgs=''
                    logging.info("no images of profile found")
                
                u.append({'img':imgs,'us':us,'comment':comment,'like':like}) 
            context={
                'title':title,
                'view':view,
                'date':date,
                'u':u
            }  
            logging.info(u)
            return render(request, 'result.html',context)     
        except:
            logging.info("error choice")
            return render(request,"search.html")
            
            