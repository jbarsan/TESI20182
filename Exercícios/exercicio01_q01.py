# Importando os módulos necessários
from bs4 import BeautifulSoup as bs
import html5lib
from selenium import webdriver


def download(url):
    # Setando a opção 'headless' do chrome
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument('headless')
    driver = webdriver.Chrome(options=opcoes)
    driver.get(url)
    return driver.page_source


def busca_dados(url):
    html = download(url)
    soup = bs(html, 'html5lib')
    filmes = soup.find_all('div', {'class': 'mb-movie'})
    lista_filmes = []

    for filme in filmes:
        titulo = filme.find('h3', class_= 'movieTitle').text
        meta_score = filme.find('span', class_= 'tMeterScore')
        score = None
        if meta_score == None:
            score = 'Ainda não avaliado'
        else:
            score = meta_score.text
        info = {'Título': titulo, "Avaliação": score}
        lista_filmes.append(info)
    return lista_filmes

def main():
    # URL da página
    url = 'https://www.rottentomatoes.com/browse/opening'
    res = busca_dados(url)
    for i in res:
        print(i)
    

if __name__=='__main__':
    main()