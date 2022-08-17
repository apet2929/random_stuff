import requests
from requests_html import HTMLSession

def init_session() -> HTMLSession:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'If-Modified-Since': 'Wed, 19 Jan 2022 04:17:04 GMT',
        'If-None-Match': 'e8f-5d5e7a87f1185-gzip',
        'Cache-Control': 'max-age=0',
    }   
    s = HTMLSession()
    s.headers = headers
    response = s.get('https://app.lightspeedvoice.com/auth/login')
    assert response.status_code == 200
    cookies = response.cookies.get_dict()
    for key, val in cookies:
        s.cookies.set(key, val)
    return s

def login(email, password):
    data = login_data_to_json(email, password)
    response = s.post("https://pweba.lsv.io/auth/login", data=data)
    print(response)

    response = s.get("http://app.lightspeedvoice.com/app/")
    response.html.render()
    
    print(response)
    print(response.url)
    print(response.content)
    print(response.text)

   
    # response = s.get("https://app.lightspeedvoice.com/app/")
    # print(response)
    # print(response.content)
    # print(response.text)
    # print(response.is_redirect)


def login_data_to_json(email, password):
    return '{"email":"' + email + '","password":"' + password + '"}'


def main():
    login("spetersen@allstate.com", "Genius72!")

s = init_session()
main()