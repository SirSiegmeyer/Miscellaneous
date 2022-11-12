# Website url: http://research.ics.aalto.fi/cog/data/udhr/
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

    hrefs = []
    names = []

    for a in soup.find_all('a', href=True, text="pdf"):
        hrefs.append(a['href'])
        names.append(soup.find('a', href=re.compile("LangID=" + a['href'][4:7])).text)

    url = "http://research.ics.aalto.fi/cog/data/udhr/"

    myDict = {}

    for name, a in zip(names, hrefs):
        response = requests.get(url + a)
        pdf_file = io.BytesIO(response.content)  # response being a requests Response object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        myDict[name] = num_pages

    print(sorted(myDict.items(), key=lambda item: item[1]))
