from crawler import download
from bs4 import BeautifulSoup as bs

url = 'https://www.imdb.com/movies-in-theaters/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2413b25e-e3f6-4229-9efd-599bb9ab1f97&pf_rd_r=Q1TFJX31HT776KQN0TY6&pf_rd_s=right-2&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_otw_hd'

html = download(url)
soup = bs(html, 'html5lib')

lista = []
dic = {}
for div in soup.find_all('div', {'class':'list_item'}):
    for a in div.select('h4 a'):
        title = a.get_text().strip()
    for score in div.find_all('span', {'class': 'metascore'}):
        s = score.get_text().strip()
        
    dic[title] = s
    lista.append(dic)
    s = None # Zerando o score
    dic = {} # Zerando o dict

# Exibindo a lista de filmes e os scores
for i in lista:
    score = i.keys()
    title = i.values()
    texto = """
    Title: {}
    Score: {}""".format(title, score)
    print(texto)