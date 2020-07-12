'''
Program for checking and automatically update Chromedriver for Window
Identify the chrome version by examining the name of chrome folder
'''

from bs4 import BeautifulSoup
import requests
import os
import zipfile
import shutil

#Change path
path=r'D:\Github\chromdriver'
local_path=r'C:\Program Files (x86)\Google\Chrome\Application' 

os.chdir(path)
file_name=os.listdir(local_path)
version=file_name[0]
version_trim=version.split('.')[0]

print('Current Chrome version is {}'.format(version))

def check_current_stable_version():
    tmp=r'https://chromedriver.chromium.org/home'
    link = requests.get(tmp)
    soup = BeautifulSoup(link.content, 'html.parser')
    
    current=soup.find('td', attrs={"class":"sites-layout-tile sites-tile-name-content-1"}).find_all('a')[4].get_text()
    current=current.split(' ')[1].split('.')[0]
    return(current)

def Update_chromedriver():
    #Check the latest update base on your chrome version, even though you are using past version
    url_check=r'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'+version_trim
    version_updated = (BeautifulSoup(requests.get(url_check).content, 'html.parser').prettify()).strip()
    
    url_download=r'https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip'.format(version_updated)
    print('Chromdriver with version {} is being downloaded'.format(version_updated))
    
    download=requests.get(url_download,stream=True)
    with open('chromedriver_win32.zip','wb') as f:
        f.write(download.content)
    
    #Unzip and delete zip file
    with zipfile.ZipFile(r'{}\chromedriver_win32.zip'.format(path), 'r') as zip_ref:
        zip_ref.extractall(r'{}\chromedriver'.format(path))
        
    shutil.copy(r'{}\chromedriver\chromedriver.exe'.format(path),r'{}\chromedriver.exe'.format(path))
    os.remove(r'{}\chromedriver_win32.zip'.format(path))
    shutil.rmtree(r'{}\chromedriver'.format(path))
    
if version_trim==check_current_stable_version():
    print('No update required')
else:
    
    Update_chromedriver()    


    
    
    