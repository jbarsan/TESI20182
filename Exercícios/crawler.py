import requests
import requests_cache
import time

requests_cache.install_cache()

def download(url, num_retries=5):
    print('Downloading:', url)
    page = None
    try:
        response = requests.get(url)
        print(response.status_code)
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