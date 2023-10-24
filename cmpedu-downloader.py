import requests
from bs4 import BeautifulSoup
import re

def get_selected_resources(resource_divs, selected_resource_ids):
    selected_resources = []
    for resource_id in selected_resource_ids:
        if 1 <= resource_id <= len(resource_divs):
            resource = resource_divs[resource_id - 1]
            resource_id = resource.find("a")["href"].split("/")[-1].split(".")[0]
            download_url = f"http://www.cmpedu.com/ziyuans/d_ziyuan.df?id={resource_id}"
            selected_resources.append((resource_id, download_url))
    return selected_resources

def main():
    book_id = input("请输入BOOK_ID: ")

    url = f"http://www.cmpedu.com/ziyuans/index.htm?BOOK_ID={book_id}"

    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        resource_divs = soup.find_all("div", class_="row gjzy_list")

        if resource_divs:
            print(f"\n资源目录在线查看：{url} \n")

            for i, resource in enumerate(resource_divs, 1):
                resource_title = resource.find("div", class_="gjzy_listRTit").text.strip()
                print(f"({i}) {resource_title} \n")

            selected_resources_input = input("请输入要下载的资源编号（用逗号分隔，例如：1,2）: ")
            selected_resource_ids = [int(x) for x in selected_resources_input.split(",") if x.isnumeric()]

            if not selected_resource_ids:
                print("未选择任何资源。")
                return

            selected_resources = get_selected_resources(resource_divs, selected_resource_ids)

            headers = {
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Accept": "text/html, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                "Accept-Language": "en-US,en;q=0.9",
                "X-Requested-With": "XMLHttpRequest"
            }

            for resource_id, download_url in selected_resources:
                response = requests.get(download_url, headers=headers)
                if response.status_code == 200:
                    download_links = re.findall(r'window\.location\.href=\'(https?://[^\'"]+)\'', response.text)
                    if download_links:
                        download_link = download_links[0]
                        print(f"资源 {resource_id} 请求成功！ 下载链接: {download_link}")
                        try:
                            import webbrowser
                            webbrowser.open(download_link)
                        except Exception as e:
                            print(f"资源 {resource_id} 打开下载链接失败: {e}")
                    else:
                        print(f"资源 {resource_id} 下载链接未找到!")
                else:
                    print(f"资源 {resource_id} 下载请求失败! 状态码: {response.status_code}")

        else:
            print("没有找到资源信息。")

    except requests.exceptions.RequestException as e:
        print(f"发生请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()