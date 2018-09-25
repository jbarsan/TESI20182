from crawler import download
from bs4 import BeautifulSoup as bs
import html5lib
import re
import sqlite3
from datetime import datetime

url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi'
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

# Criando uma tupla de dados para salvar no banco
dados = [(cidade, temperatura, sensacao, umidade, pressao, vento, atualizado)]

texto = """
Cidade:      {}
Temperatura: {}
Sensação:    {}
Umidade:     {}
Pressão:     {}
Vento:       {}
Atualizado:  {}
""".format(cidade, temperatura, sensacao, umidade, pressao, vento, atualizado)
print(texto)

conn = sqlite3.connect('temperaturas.db')
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
    atualizado TEXT NOT NULL
    );
""")
print('Tabela temperaturas criada com sucesso.')

# inserindo os dados na tabela
cursor.execute("""
INSERT INTO temperaturas (cidade, temperatura, sensacao, umidade, pressao, vento, atualizado, data_atualizacao)
VALUES (?,?,?,?,?,?,?,?)""", (cidade, temperatura, sensacao, umidade, pressao, vento, atualizado, datetime.now()))

conn.commit()
print('Dados inseridos com sucesso.')
conn.close()

