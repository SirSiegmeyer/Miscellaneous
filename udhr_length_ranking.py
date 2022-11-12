# Import libraries
import requests
from bs4 import BeautifulSoup
import PyPDF2, io, requests
import re



if __name__ == "__main__":
    # Create an URL object
    url = 'http://research.ics.aalto.fi/cog/data/udhr/'
    # Create object page
    page = requests.get(url)

    # parser-lxml = Change html to Python friendly format
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')
    soup

    #print(soup)

    hrefs = []
    names = []

    for a in soup.find_all('a', href=True, text="pdf"):
        hrefs.append(a['href'])

    for href in hrefs:
        names.append(soup.find('a', href=re.compile("LangID=" + href[4:7])).text)

    fullURL = "http://research.ics.aalto.fi/cog/data/udhr/"

    myDict = {}
    i = 0

    for a in hrefs:
        response = requests.get(fullURL + a)
        pdf_file = io.BytesIO(response.content)  # response being a requests Response object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        myDict[names[i]] = num_pages
        i += 1

    print(sorted(myDict.items(), key=lambda item: item[1]))
