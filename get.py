from bs4 import BeautifulSoup
import urllib
import shutil
from datetime import datetime

def sotd_getter():
    print('Starting the program ...')
    
    sotdUrl = "http://shed.chelseafc.com/shed_sotd.shtml"
    soup = BeautifulSoup(urllib.urlopen(sotdUrl).read())
    print('Downloaded the page ...')
    today = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)
    
    # Putting an entry in the db
    db = open('sotd_info.csv', 'a')
    content = today + ","
    for div in soup.find_all('div'):
        if div.get('id') == 'box_sotd_text':
            content += div.contents[1]
    db.write(content + '\n')
    db.close()
    print('An entry was made in the database ... ')
    
    # Downloading the image
    for img in soup.find_all('img'):
        if img.get('id') == 'sotdpic':
            urllib.urlretrieve(img.get('src'), 'images/'+today +".jpg")
    shutil.copy('images/'+today+".jpg", "today.jpg")
    print('The image was successfully downloaded ...')
    
    print('Finished running the program ...')
    
if __name__ == '__main__':
    sotd_getter()