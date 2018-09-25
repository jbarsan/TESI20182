# Importando os módulos necessários
from bs4 import BeautifulSoup as bs
import html5lib
from selenium import webdriver

# Setando a opção 'headless' do chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# URL da página
url = 'https://www.rottentomatoes.com/browse/opening'

driver.get(url)

html = driver.page_source
soup = bs(html, 'html5lib')
movies = soup.find_all('div', {'class': 'mb-movie'})
movie_list = []

for movie in movies:
    title = movie.find('h3', class_= 'movieTitle').text
    meter_score = movie.find('span', class_= 'tMeterScore')
    score = None
    if meter_score == None:
        score = 'No Score'
    else:
        score = meter_score.text
    info = {'Título': title, "Avaliação": score}
    movie_list.append(info)
    print(info)
    