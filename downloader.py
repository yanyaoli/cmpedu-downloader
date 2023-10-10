import requests
import re

url = "http://www.cmpedu.com/ziyuans/d_ziyuan.df"
params = {"id": input("Please Enter The ID Number: ")}

headers = {
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Accept": "text/html, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest"
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    print("Request Successful!")
    download_links = re.findall(r'window\.location\.href=\'(http://[^\'"]+)\'', response.text)
    if download_links:
        download_link = download_links[0]
        print("Download Link:", download_links[0])
        try:
            import webbrowser
            webbrowser.open(download_link)
        except Exception as e:
            print("Failed To Open The Download Link:", e)
    else:
        print("Download Link Not Found!")
else:
    print("Request Failed! Status Code:", response.status_code)