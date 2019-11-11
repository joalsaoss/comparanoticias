import os
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup


def readnews(purl):
    html = urlopen(purl)
    soup2 = BeautifulSoup(html)
    tags = soup2('p')
    news = ''

    for tag in tags:
        if (len(tag.attrs)) == 0:
            a = tag.contents[0]
            news = news + a

    return news


def createdataframe(pnews, pContador):
    contadores = dict()
    news = pnews.replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('(', '').replace(
        ')', '')
    palabras = news.lower().split()

    for palabra in palabras:
        if len(palabra) > 3:
            contadores[palabra] = contadores.get(palabra, 0) + 1

    return pd.DataFrame(list(contadores.items()), columns=['palabra', pContador]).sort_values(pContador,
                                                                                               ascending=False)

def writedataframe(pdataframe1, pdataframe2) :
    mergedataframefull = pd.merge(pdataframe1, pdataframe2, left_on='palabra', right_on='palabra')
    mergedataframeleft = pd.merge(pdataframe1, pdataframe2, left_on='palabra', right_on='palabra', how='left')
    mergepdataframeright = pd.merge(pdataframe1, pdataframe2, left_on='palabra', right_on='palabra', how='right')

    currentDir = os.path.dirname(__file__)
    filenamefull = "newsfull.csv"
    filenameleft = "newsleft.csv"
    filenameright = "newsright.csv"
    filepathfull = os.path.join(currentDir, filenamefull)
    filepathleft = os.path.join(currentDir, filenameleft)
    filepathright = os.path.join(currentDir, filenameright)
    mergedataframefull.to_csv(filepathfull, sep='\t', encoding='utf-8')
    mergedataframeleft.to_csv(filepathleft, sep='\t', encoding='utf-8')
    mergepdataframeright.to_csv(filepathright, sep='\t', encoding='utf-8')

url1 = "https://elpais.com/internacional/2019/11/10/actualidad/1573425323_091251.html"
nws1 = readnews(url1)
df1 = createdataframe(nws1, "contador1")

url2 = "https://elpais.com/internacional/2019/11/10/actualidad/1573426533_008486.html"
nws2 = readnews(url2)
df2 = createdataframe(nws2, "contador2")

wdf = writedataframe(df1, df2)
