import requests

def download(url, num_retries=2):
    print('Downloading:', url)
    page = None
    try:
        response = requests.get(url)
        page = response.text
        if response.status_code >= 400:
            print('Downloadin error:', response.text)
            if num_retries and 500 <= response.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
    return page

# Testando
# Expressões regulares
import re

url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
page = download(url)
area = re.findall(r'<td class="w2p_fw">(.*?)</td>',page)[1]
print(area)