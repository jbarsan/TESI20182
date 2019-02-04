import requests
import requests_cache
import time
from bs4 import BeautifulSoup as bs
import html5lib
import re
import sqlite3
from datetime import datetime


def download(url, num_retries=5):
    requests_cache.install_cache()
    print('Downloading:', url)
    page = None
    try:
        response = requests.get(url)
        # print(response.status_code)
        page = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
            time.sleep(30)
            print('Tentando novamento: ' + str(num_retries))
            if num_retries and 500 <= response.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
    return page


def busca_dados(url):
    html = download(url)
    soup = bs(html, 'html5lib')
    cidade = soup.find('h1', id='momento-localidade').get_text()
    temperatura = soup.find('p', id='momento-temperatura').get_text()
    sensacao = soup.find('li', id='momento-sensacao').get_text()
    umidade = soup.find('li', id='momento-humidade').get_text()
    pressao = soup.find('li', id='momento-pressao').get_text()
    vento = soup.find('a', id='momento-vento').get_text().strip("\n")
    vento = re.sub(r'[^\dkm/h]','',vento)
    atualizado = soup.find('p', id='momento-atualizacao').get_text()
    atualizado = re.search(r'.\d\d:\d\d$',atualizado).group(0)
    dados = [(cidade, temperatura, sensacao, umidade, pressao, vento, atualizado)]
    return dados


def cria_banco(nome_banco='temp.db'):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    # Criando a tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperaturas (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        cidade TEXT NOT NULL,
        temperatura TEXT NOT NULL,
        sensacao TEXT NOT NULL,
        umidade TEXT NOT NULL,
        pressao TEXT NOT NULL,
        vento TEXT NOT NULL,
        atualizado TEXT NOT NULL,
        data_atualizacao TEXT NOT NULL
        );""")
    print('Tabela temperaturas criada com sucesso.')
    conn.close()

    
def ler_banco(banco):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * from temperaturas;""")
    
    for i in cursor.fetchall():
        texto = """
        Cidade:      {0}
        Temperatura: {1}
        Sensação:    {2}
        Umidade:     {3}
        Pressão:     {4}
        Vento:       {5}
        Atualizado:  {6}
        """.format(i[1], i[2], i[3], i[4], i[5], i[6], i[7])
    print(texto)
    conn.close()
    

def insere_dados(banco, dados):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    
    for d in dados:
        cidade = d[0]
        temperatura = d[1]
        sensacao = d[2]
        umidade = d[3]
        pressao = d[4]
        vento = d[5]
        atualizado = d[6]
    
    cursor.execute('''INSERT INTO temperaturas (cidade, temperatura, sensacao, umidade, pressao, vento, atualizado, data_atualizacao)
    VALUES (?,?,?,?,?,?,?,?)''', (cidade, temperatura, sensacao, umidade, pressao, vento, atualizado, datetime.now()))
    conn.commit()
    print('Dados inseridos com sucesso')
    conn.close()
    

def main():
    url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi'
    dados = busca_dados(url)
    banco = 'tempTHE.db'
    cria_banco(banco)
    insere_dados(banco, dados)
    ler_banco(banco)
    print()

if __name__=='__main__':
    main()