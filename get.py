#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib
import shutil
import sys
import os
from datetime import datetime

homeDir = "/Users/sgarim1/Personal/shed_sotd/"
sotdUrl = "http://shed.chelseafc.com/shed_sotd.shtml"

def getSotdImage():
    currentTimestamp = datetime.now()
    today = str(currentTimestamp.year) + "-" + str(currentTimestamp.month) + "-" + str(currentTimestamp.day)
            
    print(currentTimestamp)
    print('Starting the program')
    
    soup = BeautifulSoup(urllib.urlopen(sotdUrl).read())
    print('Downloaded the page')
    
    # Putting an entry in the db
    db = open(homeDir+'sotd_info.csv', 'a+')
    content = today + ","
    for div in soup.find_all('div'):
        if div.get('id') == 'box_sotd_text':
            content += div.contents[1]
    db.write(content + '\n')
    db.close()
    print('An entry was made in the database')
    
    # Downloading the image
    for img in soup.find_all('img'):
        if img.get('id') == 'sotdpic':
            urllib.urlretrieve(img.get('src'), homeDir+'images/'+today +".jpg")
    shutil.copy(homeDir+'images/'+today+".jpg", homeDir+"today.jpg")
    print('The image was successfully downloaded and saved as images/'+today+'.jpg')
    
    print('Finished running the program\n')

def removeFile(fileName):
    try:
        os.remove(fileName)
    except OSError:
        pass
        
def cleanFolder(folderPath):
    try:
        shutil.rmtree(folderPath)
    except OSError:
        pass
    os.makedirs(folderPath)

def cleanFiles():
    removeFile(homeDir+'output.log')
    removeFile(homeDir+'error.log')
    removeFile(homeDir+'today.jpg')
    removeFile(homeDir+'sotd_info.csv')
    cleanFolder(homeDir+'images/')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        getSotdImage()
    elif len(sys.argv) == 2 and sys.argv[1] == "clean":
            cleanFiles()
    else:
        print("Usage: get.py [clean]")