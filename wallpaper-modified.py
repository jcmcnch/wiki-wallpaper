import os
import requests
import wget
from bs4 import BeautifulSoup
from datetime import datetime as dt
import subprocess

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

URL = "https://commons.wikimedia.org/wiki/Main_Page"

def get_image():
    response = requests.get(URL)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    main_div = soup.find(id="mainpage-potd")
    attrs = main_div.find("img").attrs
    srcset = attrs['srcset']
    longURL = srcset.split(' ')[0]
    urlOut = ('/'.join(longURL.split('/')[:-1])).replace("thumb/","")
    return urlOut


def download_image(image_url):
    user = os.getenv('USER')
    file_name = dt.now().strftime("%Y-%m-%d") + ".jpg"
    path='/home/'+user+'/wallpapers/wikimedia'
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, file_name)
    #filename = wget.download(image_url, out=full_path)
    filename = runcmd("wget {} -O {}".format(image_url, full_path), verbose=True)
    return filename

if __name__ == "__main__":
    image = get_image()
    print(image)
    image_path = download_image(image)
