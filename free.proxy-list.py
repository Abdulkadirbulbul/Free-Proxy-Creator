import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Proxy'lerin çalışıp çalışmadığını kontrol et
def proxy_kontrol(proxy):
    try:
        test_url = 'http://httpbin.org/ip'
        proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        response = requests.get(test_url, proxies=proxy_dict, timeout=5)

        if response.status_code == 200:
            print(f"Proxy {proxy} çalışıyor!")
            return proxy

    except Exception as e:
        print(f"Proxy {proxy} çalışmıyor. Hata: {e}")
    return None


if __name__ == "__main__":
    response = requests.get("https://free-proxy-list.net/")
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    textarea = soup.find("textarea", {"class": "form-control"}).text.split("\n")
    
    for i in textarea.copy():
        if "Updated" in i or i == "" or "Free proxies" in i:
            textarea.remove(i)
    del textarea[0]

    proxies = textarea

    working_proxies = []

    # 5 adet eşzamanlı(multithread) olarak proxy'leri kontrol et
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(proxy_kontrol, proxies))

    working_proxies = [proxy for proxy in results if proxy is not None]

    # Çalışan proxy'leri bir working_proxies txt dosyasına yaz
    with open('working_proxies.txt', 'w') as file:
        for working_proxy in working_proxies:
            file.write(working_proxy + '\n')
