from bs4 import BeautifulSoup as bs

# Usando o selenium pra ajudar a baixar as páginas
# geradas automaticamente por javascript
from selenium import webdriver

# Setando a opção 'headless' (sem cabeçalho) do chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

# URL da página
url = 'https://www.rottentomatoes.com/browse/opening'

driver.get(url)
html = driver.page_source

lista = []
dic = {}
soup = bs(html, 'html5lib')
for i in soup.find_all('div', {'class':'mb-movie'}):
    for j in i.find_all('h3', {'class': 'movieTitle'}):
        title = j.text
        for score in i.find_all('span', {'class': 'tMeterScore'}):
            s = score.text
    
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