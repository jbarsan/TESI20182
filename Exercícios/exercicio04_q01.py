import html5lib
from bs4 import BeautifulSoup as bs
import requests
import re
import time


def download(url, num_retries=10):
    print('Dowloading:', url)
    page = None

    try:
        response = requests.get(url)
        page = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
            time.sleep(30)
            print("Tenta de novo: " +str(num_retries))
            if num_retries != 0:
                return download(url, num_retries -1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
    return page



def busca_links(url_base,url, array_links):
    html = download(url)
    soup = bs(html, 'html5lib')
    lines = soup.find_all("tr")
    
    link = []
    links = []
    for pais in lines:
        links = links + pais.find_all("a", href=True)
    for l in links:
        link.append(l['href'])
        print(l['href'])
    
    array_links = array_links + link
    prox_botao = soup.find("div", id="pagination")
    prev_prox = prox_botao.find_all("a", href=True)
    for n in prev_prox:
        if "Next" in n.text:
            next_url = n["href"]
            return busca_links(url_base,url_base+next_url,array_links)
    return array_links


def busca_dados(url):
    html = download(url)
    soup = bs(html, 'html5lib')

    tr_nome = soup.find("tr", id="places_country__row")
    nome_p = tr_nome.find("td", class_="w2p_fw").text

    tr_area = soup.find("tr", id="places_area__row")
    area = tr_area.find("td", class_="w2p_fw").text
    area = re.sub(r'[^\d]','',area)
    area = float(area)

    tr_populacao = soup.find("tr", id="places_population__row")
    populacao = tr_populacao.find("td", class_="w2p_fw").text
    populacao = populacao.replace(',','')
    populacao = float(populacao)

    densidade = 0
    if area > 0:
        densidade = populacao/area
    
    res = """
    País: {}
    Área: {}
    Pop:  {}
    Dens: {}
    """.format(nome_p, area, populacao, densidade)
    print(res)
    # return {"Nome":nome_p,"densidade":densidade}


# Chamando as funções definidas anteriormente
def main():
    url = 'http://example.webscraping.com'
    links = busca_links(url, url, [])
    tudo = []
    for link in links:
        tudo.append(busca_dados(url + link))
    print(tudo)

# Executando o programa
if __name__=='__main__':
    main()