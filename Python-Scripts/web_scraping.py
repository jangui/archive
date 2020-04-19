import bs4 as bs
import requests
import pandas as pd

sauce = requests.get('https://pythonprogramming.net/parsememcparseface').text
soup = bs.BeautifulSoup(sauce, 'lxml')

print(soup.title)
print(soup.p)
print(soup.find_all('p'))

for paragraph in soup.find_all('p'):
    #print(paragraph.string)
    print(paragraph.text)

print(soup.get_text())



for url in soup.find_all('a'): #gets all urls
    print(url.get('href'))

nav = soup.nav #gets first nav it comes across (navigation bar most likely)
for url in nav.find_all('a'): #gets all links in nav bar
    print(url.get('href'))



body = soup.body #if only one body this should be good
for paragraph in body.find_all('p'): #only finds stuff in paragraph tags
    print(paragraph.text)

for div in soup.find_all('div', class_='body'):
    print(div.text)



#parsing tables with beautiful soup
table = soup.table #this gets first occurance of table
table = soup.find("table")
print(table)

table_rows = table.find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)



#parsing tables with pandas
dfs = pd.read_html('https://pythonprogramming.net/parsememcparseface', header= 0)
for df in dfs:
    print(df)

sauce = requests.get('https://pythonprogramming.net/sitemap.xml').text
soup = bs.BeautifulSoup(sauce, 'xml')

for url in soup.find_all('loc'):
    print(url.text)
