from bs4 import BeautifulSoup
import requests, re

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    names = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


    # get info from resourse
    parsed_array = []
    for x in names:
        r = requests.get('http://tgftp.nws.noaa.gov/data/observations/metar/decoded/%s' % names[names.index(x)])
        parsed_array.append(r.text)

    taggedlist = []
    for x in parsed_array:
        block = re.sub(r"\n", r"\nDate: ", parsed_array[parsed_array.index(x)],
                       count=1)  # find newline and add the str below once
        block = "Name: " + block
        taggedlist.append(block)

    namedlist = []
    for x in taggedlist:
        block = "\n--------"
        block = taggedlist[taggedlist.index(x)] + block
        namedlist.append(block)


    readylist = []
    for x in range(len(namedlist)):
        list = namedlist[x].split('\n')
        readylist.append(list)


    readydict = dict(zip(names, readylist))
    print(readydict)
    return names, readydict, namedlist
