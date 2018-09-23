import requests

def download(url, num_retries=2):
    print('Downloading:', url)
    page = None
    try:
        response = requests.get(url)
    except requests.exceptions.RequestsException as e:
        print('Download error:', e.reason)
    return page

page = download('http://www.google.com')
print(page)