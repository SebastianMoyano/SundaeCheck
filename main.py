#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import required modules 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
import time 
import threading
import os
import sys
#import signal
from datetime import datetime
import csv
import pickle
import requests
import wget
import zipfile
import re
import tkinter as tk
from tkinter import ttk,messagebox
from pathlib import Path
import json

link = 'https://exchange.sundaeswap.finance/#/swap?'


with open('data.json', 'r') as fp:
    dic = json.load(fp)


if hasattr(sys, "frozen"):
    main_dir = os.path.dirname(sys.executable)
    full_real_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    script_dir = os.path.dirname(__file__)
    main_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    full_real_path = os.path.dirname(os.path.realpath(sys.argv[0]))


# chrome manager
def download_chromedriver():
    def get_latestversion(version):
        url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + str(version)
        response = requests.get(url)
        version_number = response.text
        return version_number
    def download(download_url, driver_binaryname, target_name,path):
        # download the zip file using the url built above
        latest_driver_zip = wget.download(download_url, out=os.path.join(path,'temp/chromedriver.zip'))

        # extract the zip file
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall(path = os.path.join(path,'temp/')) # you can specify the destination folder path here
        # delete the zip file downloaded above
        os.remove(latest_driver_zip)
        os.rename(driver_binaryname, target_name)
        os.chmod(target_name, 0o755)
    if os.name == 'nt':
        replies = os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
        replies = replies.split('\n')
        camino = r"C:\Users\Public\Automeet"
        Path(camino).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(camino,'temp')).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(camino,'bin')).mkdir(parents=True, exist_ok=True)

        for reply in replies:
            if 'version' in reply:
                reply = reply.rstrip()
                reply = reply.lstrip()
                tokens = re.split(r"\s+", reply)
                fullversion = tokens[len(tokens) - 1]
                tokens = fullversion.split('.')
                version = tokens[0]
                break
        target_name = os.path.join(camino,'bin/chromedriver-win-' + version + '.exe')
        found = os.path.exists(target_name)
        if not found:
            version_number = get_latestversion(version)
            # build the donwload url
            download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"
            download(download_url, os.path.join(camino,'temp/chromedriver.exe'), target_name,camino)

    elif os.name == 'posix':
        reply = os.popen(r'Chrome --version').read()

        Path(os.path.join(full_real_path,'temp')).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(full_real_path,'bin')).mkdir(parents=True, exist_ok=True)
        
        if reply != '':
            reply = reply.rstrip()
            reply = reply.lstrip()
            tokens = re.split(r"\s+", reply)
            fullversion = tokens[1]
            tokens = fullversion.split('.')
            version = tokens[0]
        else:
            reply = os.popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version').read()
            reply = reply.rstrip()
            reply = reply.lstrip()
            tokens = re.split(r"\s+", reply)
            fullversion = tokens[2]
            tokens = fullversion.split('.')
            version = tokens[0]
        print("probando")
        
        target_name = os.path.join(full_real_path,'bin/chromedriver-linux-'+version)
        print('new chrome driver at ' + target_name)
        found = os.path.exists(target_name)
        if not found:
            version_number = get_latestversion(version)
            download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_mac64.zip"
            print("ya voy aca")
            download(download_url, os.path.join(full_real_path,'temp/chromedriver'), target_name,full_real_path) 
    print(target_name)
    return target_name


#
def Glogin(): 
    text = combo.get()

    driver =LoginLento()
    num = 1000

  
    # input Gmail 
    
    while True:

        limite = entry_var2.get()
        moneda = comboPair.get()
        try:
            link = 'https://exchange.sundaeswap.finance/#/swap?swap_from='+ dic[moneda] + '&swap_to=cardano.ada'
            driver.get(link) 
            WebDriverWait(driver, 20).until( EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/main/div/div/div/div/div[2]/div[3]/div[1]/div[1]/input'))) 
            driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/main/div/div/div/div/div[2]/div[3]/div[1]/div[1]/input').send_keys('1')
            WebDriverWait(driver, 20).until( EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/main/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/input'))) 
            time.sleep(1)
            val = driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/main/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/input')
           
            #
            print(val.get_attribute('value'))
            num = float(val.get_attribute('value'))
            
            total.set("Current Value: "+val.get_attribute('value'))
            
    
        except Exception as e:
            print(e)
            notify("Error", 'Ocurrio un error al conseguir valores')
            time.sleep(20)
            break

        if text == 'Less than':
            print('entre aca: '+str(num)+' '+limite)
            if num < float(limite):
                
                notify(moneda+" Price Change", "Price of "+moneda+" is lower than threshold: "+str(num))
                total.set("Finish")
                break
        else:
            if num > float(limite):
                
                notify(moneda+" Price Change", "Price of "+moneda+" is higher than threshold: "+str(num))
                total.set("Finish")
                break
        time.sleep(6)

    driver.quit()
    print('termino')
    botonmanual['state']="enable"
  
    

def notify(title, text):
    if os.name == 'nt':
        messagebox.showinfo(title, text)
        
    elif os.name == 'posix':
        os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(text, title))


    


def LoginLento():
    print("inicio lento")
    opt = Options() 
    #opt.add_experimental_option("detach", True)
    #opt.add_argument("--disable-infobars")

    opt.add_argument('ignore-certificate-errors')
    #opt.add_argument("auto-select-desktop-capture-source=Entire screen") 
    #opt.add_argument("--disable-extensions")
    #opt.add_argument('--no-sandbox')

    #opt.add_argument("--log-level=3")
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    # Pass the argument 1 to allow and 2 to block
    
    camino = download_chromedriver()
    chrome_service = ChromeService(camino)
    driver = webdriver.Chrome(service=chrome_service,options=opt)
    #driver = webdriver.Chrome(ChromeDriverManager(print_first_line=False).install(),options=opt)
    #driver.implicitly_wait(10) 	
    return driver

def relayManual():
    # se manda el proceso de conexion a segundo plano
    botonmanual['state'] = "disabled"
    total.set("Loading")
    thread = threading.Thread(target=Glogin)
    thread.setDaemon(True)
    thread.start()

def complete():
    global total,combo,comboPair,entry_var2,botonmanual
    root = tk.Tk()
    root.title("SundaeTracking")
    root.option_add("*tearOff", False)
    style = ttk.Style(root)
    root.tk.call("source", "azure.tcl")
    style.theme_use("azure")

    root.config(width=300, height=300)
    entry_var = tk.StringVar()
    entry_var2 = tk.StringVar()
    total = tk.StringVar()
    introduccion1 = tk.StringVar()
    introduccion1.set("Pair")

    Usuario = ttk.Label(root,textvariable=total)
    titulo = ttk.Label(root,textvariable=introduccion1)

    comboPair = ttk.Combobox(root,state="readonly", values=list(dic.keys()))
    comboPair.current(0)
    combo = ttk.Combobox(root,state="readonly", values=("Less than","More than"))
    combo.current(0)
    

    # Crear caja de texto.
    entry = ttk.Entry(root, textvariable=entry_var)
    entry2 = ttk.Entry(root, textvariable=entry_var2)
    botonmanual = ttk.Button(root, text="Start",command= relayManual)
    # Posicionarla en la ventana.
    titulo.place(x=50, y=30)
    
    comboPair.place(x=50, y=50)
    
    combo.place(x=50, y=90)
 
    entry2.place(x=50, y=120)
    Usuario.place(x=50, y=160)
    
    botonmanual.place(x=50, y=200)
    root.mainloop()

# assign email id and password 

#time.sleep(100) 
if __name__ == '__main__':

    complete()




