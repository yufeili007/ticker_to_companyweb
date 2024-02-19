import os
import requests
from bs4 import BeautifulSoup

# 读取ticker.txt文件中的所有ticker
with open("ticker.txt", "r") as file:
    tickers = file.read().splitlines()

# 创建一个CSV文件用于保存结果
with open("company_websites.csv", "w", encoding="utf-8") as csv_file:
    csv_file.write("Ticker,官网链接\n")

# 设置请求头信息，模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36'
}

# 遍历每个ticker并获取官网链接
for ticker in tickers:
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all("a")

        phone_number = None
        website = None

        for i in range(len(link_elements) - 1):
            current_link = link_elements[i]["href"]
            next_link = link_elements[i + 1]["href"]

            if current_link.startswith("tel:") and (next_link.startswith("http://") or next_link.startswith("https://")):
                phone_number = current_link
                website = next_link
                break

        with open("company_websites.csv", "a", encoding="utf-8") as csv_file:
            csv_file.write(f"{ticker},{website}\n")

    else:
        print(f"{url}: 无法获取网页内容。")

print("链接已保存到company_websites.csv文件。")
